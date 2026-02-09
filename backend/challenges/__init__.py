"""Challenges package: models and challenge data."""

from .data import CHALLENGES as _base_challenges, Challenge, TestCase
from .c1 import CHAPTER_1_CHALLENGES as _ch1_challenges

CHALLENGES = {**_base_challenges, **_ch1_challenges}

__all__ = ["CHALLENGES", "Challenge", "TestCase"]
