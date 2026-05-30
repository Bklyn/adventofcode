#!/usr/bin/env python3
"""Advent of Code 2025, Day 10.

Each line describes one machine:
    [.##.] (3) (1,3) (2) (2,3) (0,2) (0,1) {3,5,4,7}
      |      \\------- buttons (index sets) -------/    \\-- joltages --/
    lights

A button refers to a set of positions. The two parts reuse the same buttons
but with different algebra:

  Part 1 (lights): pressing a button TOGGLES its positions (mod 2). Find the
    fewest presses to turn the lights into the target pattern. Toggles cancel,
    so each button is pressed 0 or 1 times -> smallest subset whose XOR matches.

  Part 2 (joltages): pressing a button ADDS 1 to each of its positions. Find
    the fewest presses to reach the exact joltage targets.

Both answers sum the per-line cost across every line.
"""

from functools import cache
from itertools import combinations

import pytest

from aoc import solver


def parse(line: str):
    """Return (light_goal_bitmask, buttons_as_index_tuples, joltage_goal)."""
    lights, *buttons, joltages = line.split()
    light_goal = sum(1 << i for i, ch in enumerate(lights[1:-1]) if ch == "#")
    buttons = [tuple(int(n) for n in b[1:-1].split(",")) for b in buttons]
    joltage_goal = tuple(int(n) for n in joltages[1:-1].split(","))
    return light_goal, buttons, joltage_goal


def min_toggles(light_goal: int, button_masks: list[int]) -> int:
    """Part 1: smallest number of buttons whose XOR equals the light goal.

    We try subsets in increasing size and return the first match, so the very
    first hit is provably minimal. With <=13 buttons this is instant.
    """
    n = len(button_masks)
    for size in range(n + 1):
        for combo in combinations(range(n), size):
            lit = 0
            for i in combo:
                lit ^= button_masks[i]
            if lit == light_goal:
                return size
    raise ValueError(f"light goal {light_goal:b} is unreachable")


def patterns_by_parity(buttons, num_vars: int):
    """Group every 'press each of a subset once' pattern by its parity vector.

    Returns dict[parity_vector -> list[(pattern, cost)]], where cost is the
    cheapest subset size producing that pattern (sizes are visited ascending,
    so the first occurrence wins). Bucketing by parity lets the recursion scan
    only the patterns whose parity can possibly match the goal, instead of all
    2**n of them.
    """
    buckets: dict[tuple[int, ...], dict[tuple[int, ...], int]] = {}
    n = len(buttons)
    for size in range(n + 1):
        for combo in combinations(range(n), size):
            counts = [0] * num_vars
            for i in combo:
                for position in buttons[i]:
                    counts[position] += 1
            counts = tuple(counts)
            parity = tuple(c & 1 for c in counts)
            buckets.setdefault(parity, {}).setdefault(counts, size)
    return {parity: list(patterns.items()) for parity, patterns in buckets.items()}


def min_presses(joltage_goal: tuple[int, ...], buttons) -> int:
    """Part 2: fewest presses to reach the joltage goal.

    Parity-halving recursion: pick a subset to press once so every variable's
    parity matches the goal; the remainder is then even, so halve it and recurse
    (each deeper press counts double). Memoised over the (shrinking) goal.
    """
    buckets = patterns_by_parity(buttons, len(joltage_goal))

    @cache
    def solve(goal: tuple[int, ...]) -> int:
        if not any(goal):
            return 0
        parity = tuple(g & 1 for g in goal)
        best = float("inf")
        # Parity already matches by construction, so only check the magnitude.
        for pattern, cost in buckets.get(parity, ()):
            if all(p <= g for p, g in zip(pattern, goal)):
                residual = tuple((g - p) // 2 for p, g in zip(pattern, goal))
                best = min(best, cost + 2 * solve(residual))
        return best

    return solve(joltage_goal)


@solver(part=1)
def part_one(raw: str) -> int:
    total = 0
    for line in raw.strip().splitlines():
        light_goal, buttons, _ = parse(line)
        masks = [sum(1 << position for position in b) for b in buttons]
        total += min_toggles(light_goal, masks)
    return total


@solver(part=2)
def part_two(raw: str) -> int:
    total = 0
    for line in raw.strip().splitlines():
        _, buttons, joltage_goal = parse(line)
        total += min_presses(joltage_goal, buttons)
    return total


EXAMPLE = """[.##.] (3) (1,3) (2) (2,3) (0,2) (0,1) {3,5,4,7}
[...#.] (0,2,3,4) (2,3) (0,4) (0,1,2) (1,2,3,4) {7,5,12,7,2}
[.###.#] (0,1,2,3,4) (0,3,4) (0,1,2,4,5) (1,2) {10,11,11,5,10,5}"""


def test_q10_example():
    assert part_one(EXAMPLE) == 7
    assert part_two(EXAMPLE) == 33


@pytest.mark.real
def test_q10_real(puzzle):
    raw = puzzle.input_data
    assert part_one(raw) == 417
    assert part_two(raw) == 16765


def main():
    from aocd import data

    print(part_one(data))
    print(part_two(data))


if __name__ == "__main__":
    main()
