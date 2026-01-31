import atexit
import asyncio
import fcntl
import logging
import os
import select
import time
import uvicorn
from fastapi import FastAPI, APIRouter
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from subprocess import Popen, PIPE, STDOUT
from typing import Dict
from uuid import uuid4

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
    
    # Start GHCi process - merge stderr into stdout so we capture errors
    process = Popen(["timeout", "3600", "ghci", "-XSafe"], stdin=PIPE, stdout=PIPE, stderr=STDOUT, text=True, bufsize=1)
    
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
