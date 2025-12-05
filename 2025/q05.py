#!/usr/bin/env python3

from aocd import data


def freshness(input: str) -> int:
    fr, ingredients = input.strip().split("\n\n")
    fresh_ranges = [line.split("-", 1) for line in fr.splitlines()]
    fresh_ranges = sorted([(int(x), int(y)) for x, y in fresh_ranges])
    num_fresh = 0
    for line in ingredients.splitlines():
        i = int(line)
        for lo, hi in fresh_ranges:
            assert lo <= hi
            if lo <= i <= hi:
                num_fresh += 1
                break
            if lo > i:
                break
    collapsed = []
    for lo, hi in fresh_ranges:
        if not collapsed or lo > collapsed[-1][1] + 1:
            collapsed.append([lo, hi])
        else:
            collapsed[-1][1] = max(hi, collapsed[-1][1])
    covered = sum(hi - lo + 1 for lo, hi in collapsed)
    return num_fresh, covered


def test_ingredients():
    ex = """3-5
10-14
16-20
12-18

1
5
8
11
17
32"""
    assert (3, 14) == freshness(ex)


if __name__ == "__main__":
    print(freshness(data))
