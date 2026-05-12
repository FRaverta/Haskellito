"""Challenges package: models and challenge data."""

from .data import CHALLENGES as _base_challenges, Challenge, TestCase
from .c1 import CHAPTER_1_CHALLENGES as _ch1_challenges
from .c2 import CHAPTER_2_CHALLENGES as _ch2_challenges
from .c3 import CHAPTER_3_CHALLENGES as _ch3_challenges

CHALLENGES = {
    **_base_challenges,
    **_ch1_challenges,
    **_ch2_challenges,
    **_ch3_challenges,
}

__all__ = ["CHALLENGES", "Challenge", "TestCase"]
