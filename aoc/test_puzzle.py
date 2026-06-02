"""The shared Puzzle wrapper requires an explicit year."""

import pytest

import aoc


def test_puzzle_requires_year():
    with pytest.raises(TypeError):
        aoc.Puzzle(day=1)  # no year -> must error


def test_puzzle_accepts_year():
    # Construction must not raise when year is supplied (no network: just build it).
    p = aoc.Puzzle(day=1, year=2025)
    assert p.year == 2025 and p.day == 1
