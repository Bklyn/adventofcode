"""Local input helper for 2020: file-like access backed by aocd."""

import io

from aoc import Puzzle


def Input(day):
    """Return year-2020 puzzle input as a file-like object (read()/iterate lines)."""
    return io.StringIO(Puzzle(day=day, year=2020).input_data)
