"""
Playground API: GHCi sessions and challenges under /api/playground.
"""
import atexit
import asyncio
import fcntl
import logging
import os
import resource
import select
import time
from subprocess import Popen, PIPE, STDOUT
from typing import Dict, List
from uuid import uuid4
from fastapi import APIRouter, Query

from challenges import CHALLENGES
from schemas.playground import TestResult, SubmitRequest, EvalRequest


# --- Router ---
router = APIRouter(prefix="/api/playground")

logger = logging.getLogger(__name__)

# Store sessions: session_id -> process info
sessions: Dict[str, Dict] = {}

GHCI_PROMPT = "ghci> "

# Dangerous GHCi commands that could escape the sandbox
DANGEROUS_COMMANDS = [
    ':!',
    ':shell',
    ':cd',
    ':script',
    ':edit',
    ':e ',
    ':add',
    ':load',
    ':l ',
    ':module',
    ':reload',
    ':r',
]


def set_resource_limits():
    """Set resource limits for GHCi child processes."""
    resource.setrlimit(resource.RLIMIT_CPU, (60, 60))


def is_dangerous_command(code: str) -> tuple[bool, str]:
    """Check if the code contains dangerous GHCi commands. Returns (is_dangerous, matched_command)."""
    for line in code.split('\n'):
        line_stripped = line.strip().lower()
        for cmd in DANGEROUS_COMMANDS:
            if line_stripped.startswith(cmd.lower()):
                return True, cmd
            if cmd == ':r' and (line_stripped == ':r' or line_stripped.startswith(':r ')):
                return True, cmd
    return False, ""


def drain_pipe(pipe) -> str:
    """Drain any pending data from a pipe without blocking."""
    if pipe is None:
        return ""
    drained = []
    fd = pipe.fileno()
    flags = fcntl.fcntl(fd, fcntl.F_GETFL)
    fcntl.fcntl(fd, fcntl.F_SETFL, flags | os.O_NONBLOCK)
    try:
        while True:
            ready, _, _ = select.select([fd], [], [], 0)
            if not ready:
                break
            chunk = pipe.read(1024)
            if not chunk:
                break
            drained.append(chunk)
    except (BlockingIOError, IOError):
        pass
    finally:
        fcntl.fcntl(fd, fcntl.F_SETFL, flags)
    return ''.join(drained)


async def read_until_prompt(process: Popen, timeout: float = 10.0) -> str:
    """Read from process stdout until we see the GHCi prompt."""
    start_time = time.time()
    buffer = ""
    while True:
        elapsed = time.time() - start_time
        if elapsed >= timeout:
            logger.warning(f"read_until_prompt timed out after {timeout}s")
            raise Exception(f"read_until_prompt timed out after {timeout}s")
        remaining_timeout = timeout - elapsed
        try:
            char = await asyncio.wait_for(
                asyncio.to_thread(lambda: process.stdout.read(1)),
                timeout=min(remaining_timeout, 0.5),
            )
            if not char:
                logger.warning("EOF reached while reading from GHCi")
                break
            buffer += char
            if buffer.endswith(GHCI_PROMPT):
                result = buffer[:-len(GHCI_PROMPT)].strip()
                logger.info(f"Got output before prompt: {result}")
                return result
        except asyncio.TimeoutError:
            continue
    return buffer.strip()


async def read_output(process: Popen, timeout: float = 10.0) -> str:
    """Read GHCi output after sending a command until prompt appears."""
    return await read_until_prompt(process, timeout=timeout)


def _localized_title(challenge, lang: str) -> str:
    if lang == "es" and getattr(challenge, "title_es", None):
        return challenge.title_es
    return challenge.title


def _localized_description(challenge, lang: str) -> str:
    if lang == "es" and getattr(challenge, "description_es", None):
        return challenge.description_es
    return challenge.description


def _localized_starter_code(challenge, lang: str) -> str:
    if lang == "es" and getattr(challenge, "starter_code_es", None):
        return challenge.starter_code_es
    return challenge.starter_code or ""


def _start_ghci_process() -> Popen:
    """Start a fresh GHCi process with resource limits. Caller must kill it when done."""
    process = Popen(
        ["timeout", "3600", "ghci", "-XSafe", "+RTS", "-M64m", "-RTS"],
        stdin=PIPE,
        stdout=PIPE,
        stderr=STDOUT,
        text=True,
        bufsize=1,
        preexec_fn=set_resource_limits,
    )
    process.stdin.write(f':set prompt "{GHCI_PROMPT}"\n')
    process.stdin.flush()
    return process


def cleanup_playground_sessions():
    """Clean up all GHCi processes (sessions). Call on shutdown."""
    logger.info(f"Cleaning up {len(sessions)} playground sessions...")
    for session_id, info in list(sessions.items()):
        try:
            info["process"].kill()
            info["process"].wait(timeout=5)
            logger.info(f"Cleaned up session {session_id}")
        except Exception as e:
            logger.error(f"Error cleaning up session {session_id}: {e}")
    sessions.clear()


atexit.register(cleanup_playground_sessions)


# --- Session endpoints ---
@router.post("/sessions/")
async def start_session():
    session_id = str(uuid4())
    process = Popen(
        ["timeout", "3600", "ghci", "-XSafe", "+RTS", "-M64m", "-RTS"],
        stdin=PIPE,
        stdout=PIPE,
        stderr=STDOUT,
        text=True,
        bufsize=1,
        preexec_fn=set_resource_limits,
    )
    sessions[session_id] = {"process": process, "last_used": time.time()}
    process.stdin.write(f':set prompt "{GHCI_PROMPT}"\n')
    process.stdin.flush()
    await read_until_prompt(process)
    return {"session_id": session_id}


@router.post("/sessions/{session_id}/eval")
async def evaluate_code(session_id: str, request: EvalRequest):
    if session_id not in sessions:
        return {"error": "Session not found"}
    is_dangerous, matched_cmd = is_dangerous_command(request.code)
    if is_dangerous:
        logger.warning(f"Blocked dangerous command '{matched_cmd}' in session {session_id}")
        return {"error": f"Command '{matched_cmd}' is not allowed for security reasons"}
    process = sessions[session_id]["process"]
    if process.poll() is not None:
        del sessions[session_id]
        return {"error": "GHCi process timed out. Please restart the session."}
    code = request.formatted()
    try:
        process.stdout.flush()
        drained = drain_pipe(process.stdout)
        if drained:
            logging.info(f"Drained output before command: {drained}")
        logging.info(f"Writing code to GHCi: {code}")
        process.stdin.write(code)
        process.stdin.flush()
    except Exception as e:
        return {"error": f"Failed to write to GHCi: {str(e)}"}
    try:
        output = await read_output(process, timeout=10)
        if process.poll() is not None:
            del sessions[session_id]
            return {"error": "GHCi process terminated unexpectedly"}
        sessions[session_id]["last_used"] = time.time()
        return {"output": output}
    except Exception as e:
        logging.error(f"Error reading output: {e}")
        if process.poll():
            process.kill()
            del sessions[session_id]
        return {"error": f"GHCi process terminated unexpectedly: {str(e)}"}


@router.post("/sessions/{session_id}/close")
async def close_session(session_id: str):
    if session_id not in sessions:
        return {"error": "Session not found"}
    process = sessions[session_id]["process"]
    process.kill()
    del sessions[session_id]
    return {"status": "Session closed"}


# --- Challenge endpoints ---
@router.get("/challenges")
async def list_challenges(lang: str = Query("en", description="Language code (en, es)")):
    return {
        "challenges": [
            {"id": c.id, "title": _localized_title(c, lang)}
            for c in CHALLENGES.values()
        ]
    }


@router.get("/challenges/{challenge_id}")
async def get_challenge(
    challenge_id: str,
    lang: str = Query("en", description="Language code (en, es)"),
):
    if challenge_id not in CHALLENGES:
        return {"error": "Challenge not found"}
    challenge = CHALLENGES[challenge_id]
    return {
        "id": challenge.id,
        "title": _localized_title(challenge, lang),
        "description": _localized_description(challenge, lang),
        "starter_code": _localized_starter_code(challenge, lang),
        "test_count": len(challenge.tests),
    }


@router.post("/challenges/{challenge_id}/submit")
async def submit_challenge(challenge_id: str, request: SubmitRequest):
    if challenge_id not in CHALLENGES:
        return {"error": "Challenge not found"}
    is_dangerous, matched_cmd = is_dangerous_command(request.code)
    if is_dangerous:
        logger.warning(f"Blocked dangerous command '{matched_cmd}' in challenge submission")
        return {"error": f"Command '{matched_cmd}' is not allowed for security reasons"}
    challenge = CHALLENGES[challenge_id]
    process = _start_ghci_process()
    try:
        await read_until_prompt(process, timeout=10)
    except Exception as e:
        try:
            process.kill()
            process.wait(timeout=5)
        except Exception:
            pass
        return {"error": f"Failed to start GHCi: {str(e)}", "results": []}
    try:
        results: List[TestResult] = []
        code_request = EvalRequest(code=request.code)
        formatted_code = code_request.formatted()
        logger.info(f"Loading code: {repr(formatted_code)}")
        drain_pipe(process.stdout)
        process.stdin.write(formatted_code)
        process.stdin.flush()
        load_output = await read_output(process, timeout=10)
        logger.info(f"Load output: {repr(load_output)}")
        if "error" in load_output.lower() or "not in scope" in load_output.lower():
            return {"error": f"Failed to load your code:\n{load_output}", "results": []}
        await asyncio.sleep(0.2)
        for i, test in enumerate(challenge.tests):
            try:
                logger.info(f"Running test {i+1}: {test.code}")
                process.stdout.flush()
                stale = drain_pipe(process.stdout)
                if stale:
                    logger.info(f"Drained stale output before test {i+1}: {repr(stale)}")
                process.stdin.write(test.code + "\n")
                process.stdin.flush()
                await asyncio.sleep(0.05)
                output = await read_output(process, timeout=5)
                actual = output.strip()
                logger.info(f"Test {i+1} output: {repr(actual)}, expected: {repr(test.expected)}")
                passed = actual == test.expected
                results.append(
                    TestResult(passed=passed, test_code=test.code, expected=test.expected, actual=actual)
                )
            except Exception as e:
                logger.error(f"Test {i+1} error: {e}")
                results.append(
                    TestResult(
                        passed=False,
                        test_code=test.code,
                        expected=test.expected,
                        actual=f"Error: {str(e)}",
                    )
                )
        passed_count = sum(1 for r in results if r.passed)
        return {
            "results": [r.model_dump() for r in results],
            "passed": passed_count,
            "total": len(results),
            "all_passed": passed_count == len(results),
        }
    finally:
        try:
            process.kill()
            process.wait(timeout=5)
        except Exception as e:
            logger.warning(f"Error closing GHCi process: {e}")
