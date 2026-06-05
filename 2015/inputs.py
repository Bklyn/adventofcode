"""Local input helper for 2015: file-like access backed by aocd."""

import io

from aoc import Puzzle


def Input(day):
    """Return year-2015 puzzle input as a file-like object (read()/iterate lines)."""
    return io.StringIO(Puzzle(day=day, year=2015).input_data)
