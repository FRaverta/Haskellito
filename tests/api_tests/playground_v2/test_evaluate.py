from dataclasses import dataclass
from shutil import which
from textwrap import dedent
from uuid import UUID

import pytest
from fastapi import FastAPI
from fastapi.testclient import TestClient

from api import playground_v2


pytestmark = pytest.mark.skipif(
    which("ghci") is None or which("timeout") is None,
    reason="evaluate_v2 integration tests require ghci and timeout",
)


@dataclass(frozen=True)
class HaskellEvalCase:
    name: str
    history: list[str]
    code: str
    expected_response: dict[str, str]


def haskell(source: str) -> str:
    return dedent(source).strip()


HASKELL_EVAL_CASES = [
    HaskellEvalCase(
        name="simple arithmetic expression",
        history=[],
        code="1 + 2",
        expected_response={"output": "3"},
    ),
    HaskellEvalCase(
        name="function defined in command history",
        history=[
            haskell(
                """
                double :: Int -> Int
                double n = n * 2
                """
            ),
        ],
        code="double 21",
        expected_response={"output": "42"},
    ),
    HaskellEvalCase(
        name="recursive function defined in command history",
        history=[
            haskell(
                """
                factorial :: Int -> Int
                factorial 0 = 1
                factorial n = n * factorial (n - 1)
                """
            ),
        ],
        code="factorial 5",
        expected_response={"output": "120"},
    ),
    HaskellEvalCase(
        name="list transformation with a named helper",
        history=[
            'greet name = "hello " ++ name',
        ],
        code='map greet ["ada", "grace"]',
        expected_response={"output": '["hello ada","hello grace"]'},
    ),
    HaskellEvalCase(
        name="list transformation with a named helper",
        history="""
            data BTree a = Leaf | Node a (BTree a) (BTree a) deriving Show
            t1 = Node 2 Leaf Leaf
            """.split("\n"),
        code='t1',
        expected_response={"output": 'Node 2 Leaf Leaf'},
    ),
]


@pytest.fixture(scope="module")
def client():
    app = FastAPI()
    app.include_router(playground_v2.router)

    playground_v2.cleanup_v2_workers()
    playground_v2.pool = None

    with TestClient(app) as test_client:
        yield test_client

    playground_v2.cleanup_v2_workers()
    playground_v2.pool = None


def start_session(client: TestClient) -> str:
    response = client.post("/api/v2/playground/sessions/")

    assert response.status_code == 200
    session_id = response.json()["session_id"]
    UUID(session_id)
    return session_id


def evaluate(client: TestClient, session_id: str, history: list[str], code: str):
    response = client.post(
        f"/api/v2/playground/sessions/{session_id}/eval",
        json={
            "history": history,
            "code": code,
        },
    )

    assert response.status_code == 200
    return response.json()


@pytest.mark.parametrize(
    "case",
    HASKELL_EVAL_CASES,
    ids=[case.name for case in HASKELL_EVAL_CASES],
)
def test_evaluate_v2_runs_haskell_programs(client, case):
    session_id = start_session(client)

    result = evaluate(
        client=client,
        session_id=session_id,
        history=case.history,
        code=case.code,
    )

    assert result == case.expected_response


def test_evaluate_v2_resets_worker_state_between_requests(client):
    session_id = start_session(client)

    first_result = evaluate(
        client=client,
        session_id=session_id,
        history=["temporaryValue = 99"],
        code="temporaryValue",
    )
    second_result = evaluate(
        client=client,
        session_id=session_id,
        history=[],
        code="temporaryValue",
    )

    assert first_result == {"output": "99"}
    assert "output" in second_result
    assert "Variable not in scope: temporaryValue" in second_result["output"]


def test_evaluate_v2_blocks_dangerous_eval_commands(client):
    session_id = start_session(client)

    result = evaluate(
        client=client,
        session_id=session_id,
        history=[],
        code=":load Secret.hs",
    )

    assert result == {
        "output": "Command ':load' is not allowed for security reasons",
    }


def test_evaluate_v2_reports_dangerous_history_replay_failure(client):
    session_id = start_session(client)

    result = evaluate(
        client=client,
        session_id=session_id,
        history=[":load Secret.hs"],
        code="1 + 1",
    )

    assert result == {
        "error": "History command blocked (':load'): :load Secret.hs",
        "history_failed": True,
    }
