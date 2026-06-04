import asyncio
from subprocess import PIPE, STDOUT, Popen

import pytest

from api.playground import read_until_prompt


def test_read_until_prompt_raises_when_process_exits_before_prompt():
    process = Popen(
        ["printf", "ghci failed to start"],
        stdout=PIPE,
        stderr=STDOUT,
        text=True,
    )

    with pytest.raises(Exception) as exc_info:
        asyncio.run(read_until_prompt(process, timeout=1))

    assert "EOF reached while reading from GHCi before prompt" in str(exc_info.value)
    assert "ghci failed to start" in str(exc_info.value)
