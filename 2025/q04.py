#!/usr/bin/env python3

from aoc import *
from aocd import data


def forklift(input: str, rounds: int = 1) -> int:
    grid = parse_grid(input)
    result = 0
    for _ in range(rounds):
        can_clear = [
            pos
            for pos, c in grid.items()
            if c == "@" and sum(1 for n in neighbors8(pos) if grid.get(n) == "@") < 4
        ]
        if not can_clear:
            break
        result += len(can_clear)
        for pos in can_clear:
            grid[pos] = "."
    return result


def test_forklift():
    ex = """..@@.@@@@.
@@@.@.@.@@
@@@@@.@.@@
@.@@@@..@.
@@.@@@@.@@
.@@@@@@@.@
.@.@.@.@@@
@.@@@.@@@@
.@@@@@@@@.
@.@.@@@.@."""
    assert 13 == forklift(ex)
    assert 43 == forklift(ex, 10**10)


if __name__ == "__main__":
    print(forklift(data))
    print(forklift(data, 10**10))
