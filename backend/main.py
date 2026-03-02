import logging
import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from api.playground import cleanup_playground_sessions, router as playground_router
from api.playground_v2 import cleanup_v2_workers, router as playground_v2_router

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
        "http://127.0.0.1:5173",
        "*",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

logging.basicConfig(level=logging.INFO)


@app.on_event("shutdown")
async def shutdown_event():
    """Clean up playground GHCi sessions on shutdown."""
    cleanup_playground_sessions()
    cleanup_v2_workers()


app.include_router(playground_router)
app.include_router(playground_v2_router)


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
