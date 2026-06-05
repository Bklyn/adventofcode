"""Local input helper for 2021 solvers: file-like access backed by aocd."""

import io

from aoc import Puzzle


def Input(day):
    """Return year-2021 puzzle input as a file-like object (read()/iterate lines)."""
    return io.StringIO(Puzzle(day=day, year=2021).input_data)
