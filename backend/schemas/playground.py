from pydantic import BaseModel
from typing import List, Optional


# --- Pydantic models ---
class TestResult(BaseModel):
    passed: bool
    test_code: str
    expected: str
    actual: str


class SubmitRequest(BaseModel):
    code: str
    session_id: Optional[str] = None


class EvalRequest(BaseModel):
    code: str

    def formatted(self) -> str:
        """Format code for GHCi evaluation."""
        stripped = self.code.strip()
        if "\n" in stripped:
            return ":{\n" + stripped + "\n:}\n"
        return stripped + "\n"


class EvalRequestV2(BaseModel):
    history: List[str] = []
    code: str

    @staticmethod
    def format_command(cmd: str) -> str:
        """Format a single command for GHCi evaluation."""
        stripped = cmd.strip()
        if "\n" in stripped:
            return ":{\n" + stripped + "\n:}\n"
        return stripped + "\n"