#!/usr/bin/env python3

from aoc import *
from collections import Counter


def move_robot(p, d, width, height, rounds):
    q = ((p[0] + d[0] * rounds) % height, (p[1] + d[1] * rounds) % width)
    return q, d


def print_robots(robots, width, height, sectors=False):
    grid = Counter()
    for (y, x), _ in robots:
        grid[(y, x)] += 1
    print(f"{len(robots)} robots:")
    for y in range(height):
        line = []
        for x in range(width):
            if sectors and (x == width // 2 or y == height // 2):
                line.append("X")
                continue
            c = grid.get((y, x), 0)
            line.append("." if c == 0 else str(c % 10))
        print("".join(line))


def parse_robots(input: str) -> list:
    for line in input.splitlines():
        x, y, dx, dy = [int(i) for i in re.findall(r"-?\d+", line)]
        yield ((y, x), (dy, dx))


def find_regions(robots: list) -> list:
    """Build a set of all contiguous regions"""
    seen = set()
    grid = set(r for r, _ in robots)
    regions = []
    for p in grid:
        if p in seen:
            continue
        region = set([p])
        current = [p]
        while current:
            for n in neighbors4(current.pop()):
                if n in grid and n not in region:
                    region.add(n)
                    current.append(n)
        seen.update(region)
        regions.append(region)
    return regions


def restroom_redoubt(
    input: str, width: int = 101, height: int = 103, rounds=100
) -> int:
    robots = [(r, v) for r, v in parse_robots(input)]
    robots = [move_robot(p, d, width, height, rounds) for p, d in robots]
    sectors = Counter()
    w2 = 1 + width // 2
    h2 = 1 + height // 2
    for (y, x), _ in robots:
        sx = divmod(x + 1, w2)
        sy = divmod(y + 1, h2)
        if sx == (1, 0) or sy == (1, 0):
            continue
        sector = 2 * sy[0] + sx[0]
        sectors[sector] += 1
    return multiply(sectors.values())


def play_robots(instr: str, width: int = 101, height: int = 103):
    robots = tuple((r, v) for r, v in parse_robots(instr))
    i = 0
    for i in range(10**10):
        regions = find_regions(robots)
        if any(len(r) > 100 for r in regions):
            print(f"Round {i}")
            print_robots(robots, width, height)
            return i
        robots = tuple(move_robot(p, d, width, height, 1) for p, d in robots)


def main():
    p = Puzzle(day=14)
    assert 12 == restroom_redoubt(p.examples[0].input_data, 11, 7)
    print(restroom_redoubt(p.input_data))
    print(play_robots(p.input_data))


if __name__ == "__main__":
    main()
