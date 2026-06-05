"""Local input helper for 2019 solvers: file-like access backed by aocd."""

import io

from aoc import Puzzle


def Input(day: int) -> io.StringIO:
    """Return year-2019 puzzle input as a file-like object (read()/iterate lines)."""
    return io.StringIO(Puzzle(day=day, year=2019).input_data)
