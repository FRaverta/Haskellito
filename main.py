import atexit
import asyncio
import fcntl
import logging
import os
import resource
import select
import time
import uvicorn
from fastapi import FastAPI, APIRouter, Query
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from subprocess import Popen, PIPE, STDOUT
from typing import Dict, List, Optional
from uuid import uuid4


from challenges import CHALLENGES
from pydantic import BaseModel


class TestResult(BaseModel):
    passed: bool
    test_code: str
    expected: str
    actual: str


class SubmitRequest(BaseModel):
    code: str
    session_id: Optional[str] = None  # ignored; kept for backward compatibility


def set_resource_limits():
    """
    Set resource limits for GHCi child processes.
    These limits prevent resource exhaustion attacks.
    Tuned for first-year students learning basic Haskell.
    
    Note: We don't use RLIMIT_AS (virtual memory) because GHC 9.6+ requires
    ~400MB+ just to load shared libraries, plus ~8MB per OS thread for stacks.
    Instead, we limit the Haskell heap via RTS options in the ghci command.
    """
    # Max 60 seconds CPU time (prevents infinite loops)
    resource.setrlimit(resource.RLIMIT_CPU, (60, 60))

app = FastAPI()

# API router with /api prefix
api_router = APIRouter(prefix="/api")

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173", 
        "http://127.0.0.1:5173",
        "*",  # Allow all origins in production (nginx handles this)
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Store sessions: session_id -> process info
sessions: Dict[str, Dict] = {}

# Input model for evaluation
class EvalRequest(BaseModel):
    code: str

    def formatted(self) -> str:
        """Format code for GHCi evaluation."""
        stripped = self.code.strip()
        if "\n" in stripped:
            return ":{\n" + stripped + "\n:}\n"
        return stripped + "\n"


# Dangerous GHCi commands that could escape the sandbox
DANGEROUS_COMMANDS = [
    ':!',           # Shell command execution
    ':shell',       # Open shell
    ':cd',          # Change directory
    ':script',      # Run script file
    ':edit',        # Open editor
    ':e ',          # Short for :edit
    ':add',         # Add modules (could load malicious code)
    ':load',        # Load modules
    ':l ',          # Short for :load
    ':module',      # Change module context
    ':reload',      # Reload modules
    ':r',           # Short for :reload (when at start)
]


def is_dangerous_command(code: str) -> tuple[bool, str]:
    """
    Check if the code contains dangerous GHCi commands.
    Returns (is_dangerous, matched_command).
    """
    # Check each line for dangerous commands
    for line in code.split('\n'):
        line_stripped = line.strip().lower()
        for cmd in DANGEROUS_COMMANDS:
            # Check if line starts with the dangerous command
            if line_stripped.startswith(cmd.lower()):
                return True, cmd
            # Also check for :r specifically (must be exact or followed by space/newline)
            if cmd == ':r' and (line_stripped == ':r' or line_stripped.startswith(':r ')):
                return True, cmd
    return False, ""

GHCI_PROMPT = "ghci> "


def drain_pipe(pipe) -> str:
    """
    Drain any pending data from a pipe without blocking.
    Returns whatever data was available.
    """
    if pipe is None:
        return ""
    
    drained = []
    fd = pipe.fileno()
    
    # Set non-blocking mode
    flags = fcntl.fcntl(fd, fcntl.F_GETFL)
    fcntl.fcntl(fd, fcntl.F_SETFL, flags | os.O_NONBLOCK)
    
    try:
        while True:
            # Check if there's data available
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
        # Restore blocking mode
        fcntl.fcntl(fd, fcntl.F_SETFL, flags)
    
    return ''.join(drained)


@api_router.post("/sessions/")
async def start_session():
    session_id = str(uuid4())
    
    # Start GHCi process with resource limits
    # RTS options: -M64m limits Haskell heap to 64MB (sufficient for learning)
    process = Popen(
        ["timeout", "3600", "ghci", "-XSafe", "+RTS", "-M64m", "-RTS"],
        stdin=PIPE,
        stdout=PIPE,
        stderr=STDOUT,
        text=True,
        bufsize=1,
        preexec_fn=set_resource_limits  # Apply resource limits before exec
    )
    
    # Store process info
    sessions[session_id] = {
        "process": process,
        "last_used": time.time()
    }
    
    # Set a known prompt so we can reliably detect when GHCi is ready
    process.stdin.write(f':set prompt "{GHCI_PROMPT}"\n')
    process.stdin.flush()
    
    # Read and discard the initial banner until we see our prompt
    await read_until_prompt(process)
    return {"session_id": session_id}

@api_router.post("/sessions/{session_id}/eval")
async def evaluate_code(session_id: str, request: EvalRequest):
    if session_id not in sessions:
        return {"error": "Session not found"}
    
    # Security check: block dangerous GHCi commands
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
        # Drain any leftover output from previous commands
        process.stdout.flush()
        drained = drain_pipe(process.stdout)
        if drained:
            logging.info(f"Drained output before command: {drained}")
        
        logging.info(f"Writing code to GHCi: {code}")
        process.stdin.write(code)
        process.stdin.flush()
    except Exception as e:
        return {"error": f"Failed to write to GHCi: {str(e)}"}
    
    # Read output until we see the prompt again
    try:
        output = await read_output(process, timeout=10)
        
        # Check if the process is still alive
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



@api_router.post("/sessions/{session_id}/close")
async def close_session(session_id: str):
    if session_id not in sessions:
        return {"error": "Session not found"}
    
    process = sessions[session_id]["process"]
    process.kill()
    del sessions[session_id]
    
    return {"status": "Session closed"}


# Challenge endpoints
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


@api_router.get("/challenges")
async def list_challenges(lang: str = Query("en", description="Language code (en, es)")):
    """List all available challenges (without solutions). Returns localized title per lang."""
    return {
        "challenges": [
            {
                "id": c.id,
                "title": _localized_title(c, lang),
            }
            for c in CHALLENGES.values()
        ]
    }


@api_router.get("/challenges/{challenge_id}")
async def get_challenge(
    challenge_id: str,
    lang: str = Query("en", description="Language code (en, es)"),
):
    """Get a specific challenge (without solution). Returns localized content per lang."""
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


@api_router.post("/challenges/{challenge_id}/submit")
async def submit_challenge(challenge_id: str, request: SubmitRequest):
    """Submit a solution for a challenge. Spawns a GHCi process, runs tests, then closes it."""
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
            return {
                "error": f"Failed to load your code:\n{load_output}",
                "results": [],
            }

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
                    TestResult(
                        passed=passed,
                        test_code=test.code,
                        expected=test.expected,
                        actual=actual,
                    )
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

async def read_until_prompt(process: Popen, timeout: float = 10.0) -> str:
    """
    Read from process stdout until we see the GHCi prompt.
    Returns all output before the prompt.
    """
    start_time = time.time()
    buffer = ""
    
    while True:
        elapsed = time.time() - start_time
        if elapsed >= timeout:
            logging.warning(f"read_until_prompt timed out after {timeout}s")
            raise Exception(f"read_until_prompt timed out after {timeout}s")
        
        remaining_timeout = timeout - elapsed
        try:
            # Read one character at a time to handle prompts that don't end with newline
            char = await asyncio.wait_for(
                asyncio.to_thread(lambda: process.stdout.read(1)),
                timeout=min(remaining_timeout, 0.5)
            )
            
            if not char:  # EOF
                logging.warning("EOF reached while reading from GHCi")
                break
            
            buffer += char
            
            # Check if buffer ends with our prompt
            if buffer.endswith(GHCI_PROMPT):
                # Remove the prompt from buffer and return the rest
                result = buffer[:-len(GHCI_PROMPT)].strip()
                logging.info(f"Got output before prompt: {result}")
                logging.info(f"Buffer: {buffer}")
                return result
                
        except asyncio.TimeoutError:
            # Short timeout on individual read, continue waiting
            continue
    
    # If we got here, we timed out - return what we have
    logging.info(f"Timed out reading from GHCi: {buffer}")
    return buffer.strip()


async def read_output(process: Popen, timeout: float = 10.0) -> str:
    """
    Read GHCi output after sending a command.
    Waits until the prompt appears, then returns everything before it.
    Since stderr is merged into stdout, all output (including errors) comes through here.
    """
    return await read_until_prompt(process, timeout=timeout)


def cleanup_all_sessions():
    """Clean up all GHCi processes on shutdown."""
    logger.info(f"Cleaning up {len(sessions)} sessions...")
    for session_id, info in list(sessions.items()):
        try:
            info["process"].kill()
            info["process"].wait(timeout=5)
            logger.info(f"Cleaned up session {session_id}")
        except Exception as e:
            logger.error(f"Error cleaning up session {session_id}: {e}")
    sessions.clear()


# Register cleanup handlers
atexit.register(cleanup_all_sessions)


@app.on_event("shutdown")
async def shutdown_event():
    """FastAPI shutdown event handler."""
    cleanup_all_sessions()


# Include the API router
app.include_router(api_router)


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
