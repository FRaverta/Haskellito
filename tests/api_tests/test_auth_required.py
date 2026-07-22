from fastapi import FastAPI
from fastapi.testclient import TestClient

from api import playground_v2


def auth_enabled_client(monkeypatch) -> TestClient:
    monkeypatch.setenv("COGNITO_AUTH_ENABLED", "true")
    monkeypatch.setenv("COGNITO_USER_POOL_ID", "us-east-1_TEST")
    monkeypatch.setenv("COGNITO_APP_CLIENT_ID", "test-client")

    app = FastAPI()
    app.include_router(playground_v2.router)
    return TestClient(app)


def test_execution_endpoints_require_authentication(monkeypatch):
    client = auth_enabled_client(monkeypatch)

    response = client.post("/api/v2/playground/sessions/")

    assert response.status_code == 401
    assert response.json() == {"detail": "Authentication required."}


def test_challenge_listing_stays_public(monkeypatch):
    client = auth_enabled_client(monkeypatch)

    response = client.get("/api/v2/playground/challenges")

    assert response.status_code == 200
    assert "challenges" in response.json()
