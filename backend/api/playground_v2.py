"""
Playground V2 API: Worker-pool multiplexed GHCi under /api/v2/playground.

Instead of one GHCi process per session, a fixed pool of workers is shared
across all users.  Each request carries its command history; the worker
resets GHCi state via :load Empty.hs, replays the history, then executes
the new command.  The process is only restarted if it dies.
"""
import asyncio
import atexit
import logging
import os
from typing import List, Optional
from uuid import uuid4
from subprocess import Popen

from fastapi import APIRouter

from api.playground import (
    _start_ghci_process,
    read_until_prompt,
    read_output,
    drain_pipe,
    is_dangerous_command,
)
from schemas.playground import EvalRequestV2

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/api/v2/playground")

NUM_GHCI_SESSIONS = int(os.environ.get("NUM_GHCI_SESSIONS", "3"))
ACQUIRE_TIMEOUT = float(os.environ.get("WORKER_ACQUIRE_TIMEOUT", "30"))
HISTORY_CMD_TIMEOUT = float(os.environ.get("HISTORY_CMD_TIMEOUT", "5"))
EVAL_CMD_TIMEOUT = float(os.environ.get("EVAL_CMD_TIMEOUT", "10"))
# GHCi can be slow to start on production (limited CPU); default 30s
GHCI_STARTUP_TIMEOUT = float(os.environ.get("GHCI_STARTUP_TIMEOUT", "30"))

EMPTY_MODULE_PATH = os.path.join(
    os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
    "ghci", "Empty.hs",
)


class HistoryReplayError(Exception):
    """Raised when replaying a command from the history fails."""


class Worker:
    """
    Owns a single GHCi process that is reused across requests.

    Each request: reset state via :load Empty.hs, replay the
    full history, execute the new command.  Only restarts the
    process if it's dead.
    """

    def __init__(self, worker_id: int):
        self.worker_id = worker_id
        self.process: Optional[Popen] = None

    def _is_alive(self) -> bool:
        return (
            self.process is not None
            and self.process.poll() is None
        )

    def _kill_process(self):
        if self.process is not None:
            try:
                self.process.kill()
                self.process.wait(timeout=5)
            except Exception:
                pass
            self.process = None

    async def _start_fresh(self):
        """Kill any existing process and start a new GHCi."""
        self._kill_process()
        self.process = _start_ghci_process()
        await read_until_prompt(self.process, timeout=GHCI_STARTUP_TIMEOUT)
        logger.info(
            f"Worker {self.worker_id}: started fresh "
            f"GHCi (pid={self.process.pid})"
        )

    async def _reset_state(self):
        """Reset GHCi scope by loading the empty module."""
        drain_pipe(self.process.stdout)
        self.process.stdin.write(
            f':load {EMPTY_MODULE_PATH}\n'
        )
        self.process.stdin.flush()
        await read_output(self.process, timeout=5)

    async def _replay_commands(self, commands: List[str]):
        """Replay a list of commands, raising on failure."""
        for i, cmd in enumerate(commands):
            is_dangerous, matched = is_dangerous_command(cmd)
            if is_dangerous:
                raise HistoryReplayError(
                    f"History command blocked "
                    f"('{matched}'): {cmd}"
                )

            fmt = EvalRequestV2.format_command(cmd)
            try:
                drain_pipe(self.process.stdout)
                self.process.stdin.write(fmt)
                self.process.stdin.flush()
                await read_output(
                    self.process,
                    timeout=HISTORY_CMD_TIMEOUT,
                )
            except Exception as e:
                raise HistoryReplayError(
                    f"History replay failed at "
                    f"command {i + 1}: {e}"
                )

            if self.process.poll() is not None:
                raise HistoryReplayError(
                    f"GHCi died replaying "
                    f"command {i + 1}"
                )

    async def execute(
        self, history: List[str], code: str,
    ) -> str:
        """
        1) Ensure the process is alive (restart if dead).
        2) Reset state via :load Empty.hs.
        3) Replay history.
        4) Execute code and return its output.
        """
        if not self._is_alive():
            await self._start_fresh()

        try:
            await self._reset_state()
        except Exception:
            await self._start_fresh()

        if history:
            logger.info(
                f"Worker {self.worker_id}: "
                f"replaying {len(history)} cmds"
            )
            await self._replay_commands(history)

        is_dangerous, matched = is_dangerous_command(code)
        if is_dangerous:
            return (
                f"Command '{matched}' is not allowed"
                " for security reasons"
            )

        fmt = EvalRequestV2.format_command(code)
        try:
            drain_pipe(self.process.stdout)
            self.process.stdin.write(fmt)
            self.process.stdin.flush()
            output = await read_output(
                self.process, timeout=EVAL_CMD_TIMEOUT,
            )
        except Exception as e:
            self._kill_process()
            raise Exception(
                "GHCi process terminated "
                f"unexpectedly: {e}"
            )

        if self.process.poll() is not None:
            self._kill_process()
            raise Exception(
                "GHCi process terminated unexpectedly"
            )

        return output


class WorkerPool:
    """Fixed-size pool of GHCi workers backed by asyncio.Queue."""

    def __init__(self, size: int):
        self.size = size
        self._queue: asyncio.Queue[Worker] = (
            asyncio.Queue(maxsize=size)
        )
        self._workers: List[Worker] = []

    async def start(self):
        """Create workers and start their GHCi processes."""
        logger.info(
            f"Starting worker pool with {self.size} workers"
        )
        for i in range(self.size):
            w = Worker(worker_id=i)
            await w._start_fresh()
            self._workers.append(w)
            await self._queue.put(w)
        logger.info("Worker pool ready")

    async def acquire(self, timeout: float = ACQUIRE_TIMEOUT):
        return await asyncio.wait_for(
            self._queue.get(), timeout=timeout,
        )

    async def release(self, worker: Worker):
        """Return the worker to the pool immediately."""
        await self._queue.put(worker)

    def shutdown(self):
        """Kill every worker's GHCi process."""
        logger.info(
            "Shutting down worker pool "
            f"({len(self._workers)} workers)"
        )
        for w in self._workers:
            w._kill_process()


pool: Optional[WorkerPool] = None


async def get_pool() -> WorkerPool:
    """Lazy-init the global worker pool on first use."""
    global pool
    if pool is None:
        pool = WorkerPool(size=NUM_GHCI_SESSIONS)
        await pool.start()
    return pool


def cleanup_v2_workers():
    """Kill all v2 worker processes. Call on shutdown."""
    if pool is not None:
        pool.shutdown()


atexit.register(cleanup_v2_workers)


# ---------- Endpoints ----------

@router.post("/sessions/")
async def start_session_v2():
    """Return a session ID. No GHCi process is allocated."""
    await get_pool()
    return {"session_id": str(uuid4())}


@router.post("/sessions/{session_id}/eval")
async def evaluate_v2(session_id: str, request: EvalRequestV2):
    wp = await get_pool()

    try:
        worker = await wp.acquire(timeout=ACQUIRE_TIMEOUT)
    except asyncio.TimeoutError:
        return {"error": "Server busy, please try again later"}

    try:
        output = await worker.execute(request.history, request.code)
        return {"output": output}
    except HistoryReplayError as e:
        logger.warning(f"History replay error for session {session_id}: {e}")
        return {"error": str(e), "history_failed": True}
    except Exception as e:
        logger.error(f"Eval error for session {session_id}: {e}")
        return {"error": str(e)}
    finally:
        await wp.release(worker)


@router.post("/sessions/{session_id}/close")
async def close_session_v2(session_id: str):
    """No-op for v2 — workers are shared, not per-session."""
    return {"status": "Session closed"}
