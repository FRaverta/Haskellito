from fastapi import FastAPI
from fastapi.testclient import TestClient

from api import playground_v2


GHCI_STARTUP_ERROR = (
    "EOF reached while reading from GHCi before prompt "
    "(returncode=126); output: timeout: failed to run command 'ghci': "
    "Permission denied"
)


class FailingWorker:
    async def execute(self, history, code):
        raise Exception(GHCI_STARTUP_ERROR)


class PoolWithFailingWorker:
    def __init__(self):
        self.worker = FailingWorker()
        self.released_workers = []

    async def acquire(self, timeout):
        return self.worker

    async def release(self, worker):
        self.released_workers.append(worker)


def make_client(*, raise_server_exceptions=True):
    app = FastAPI()
    app.include_router(playground_v2.router)
    return TestClient(
        app,
        raise_server_exceptions=raise_server_exceptions,
    )


def test_start_session_v2_returns_500_when_worker_pool_startup_fails(
    monkeypatch,
):
    async def fail_to_get_pool():
        raise Exception(GHCI_STARTUP_ERROR)

    monkeypatch.setattr(playground_v2, "get_pool", fail_to_get_pool)

    with make_client(raise_server_exceptions=False) as client:
        response = client.post("/api/v2/playground/sessions/")

    assert response.status_code == 500


def test_evaluate_v2_returns_error_when_worker_restart_fails(monkeypatch):
    pool = PoolWithFailingWorker()

    async def get_pool_with_failing_worker():
        return pool

    monkeypatch.setattr(
        playground_v2,
        "get_pool",
        get_pool_with_failing_worker,
    )

    with make_client() as client:
        response = client.post(
            "/api/v2/playground/sessions/test-session/eval",
            json={
                "history": [],
                "code": "1 + 1",
            },
        )

    assert response.status_code == 200
    assert response.json() == {"error": GHCI_STARTUP_ERROR}
    assert pool.released_workers == [pool.worker]
