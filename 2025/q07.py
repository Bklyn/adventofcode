#!/usr/bin/env python3

from aoc import parse_grid, first
from aocd import data

from collections import Counter


def tachyon_beams(input: str):
    grid = parse_grid(input)
    maxy = max(y for y, _ in grid.keys())
    start = first(pos for pos, c in grid.items() if c == "S")
    assert start is not None
    frontier = set([start])
    splits = 0
    while frontier:
        new_frontier = set()
        for by, bx in frontier:
            by += 1
            if by == maxy:
                continue  # end
            if grid[(by, bx)] == "^":  # split
                splits += 1
                for pos in ((by, bx - 1), (by, bx + 1)):
                    if pos in grid:
                        new_frontier.add(pos)
                continue
            new_frontier.add((by, bx))
        frontier = new_frontier
    return splits


def tachyon_timelines(input: str):
    grid = parse_grid(input)
    maxy = max(y for y, _ in grid.keys())
    start = first(pos for pos, c in grid.items() if c == "S")
    assert start is not None
    beams = Counter([start])
    while first(beams.elements())[0] < maxy - 1:
        new_beams = Counter()
        for (by, bx), count in beams.items():
            by += 1
            if grid[(by, bx)] == "^":  # split
                new_beams.update({(by, bx - 1): count, (by, bx + 1): count})
            else:
                new_beams.update({(by, bx): count})
        beams = new_beams
    return sum(beams.values())


def test_tachyon_beams():
    ex = """.......S.......
...............
.......^.......
...............
......^.^......
...............
.....^.^.^.....
...............
....^.^...^....
...............
...^.^...^.^...
...............
..^...^.....^..
...............
.^.^.^.^.^...^.
..............."""
    assert 21 == tachyon_beams(ex)
    assert 40 == tachyon_timelines(ex)


if __name__ == "__main__":
    print(tachyon_beams(data))
    print(tachyon_timelines(data))
