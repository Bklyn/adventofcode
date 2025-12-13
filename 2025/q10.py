#!/usr/bin/env python3

from aoc import vector
from aocd import data

import time
import collections
from heapq import heappush, heappop
import numpy as np


def parse_lights(lights: str) -> int:
    lcb = "".join(reversed(lights[1:-1]))
    return int(lcb.replace("#", "1").replace(".", "0"), 2)


def parse_buttons(buttons: str) -> int:
    val = 0
    for b in vector(buttons):
        val |= 1 << b
    return val


def solve_joltages(buttons, joltages) -> int:
    print(f"solve: {joltages} {buttons}")
    goal = tuple(joltages)
    todo = [(0, tuple([0] * len(joltages)))]
    seen = set()
    buttons = [[1 * (i in b) for i in range(len(joltages))] for b in buttons]
    print(buttons)
    assert all(len(b) == len(joltages) for b in buttons)

    while todo:
        presses, power = heappop(todo)
        if power == goal:
            return presses

        for b in buttons:
            new_power = tuple(v + dv for v, dv in zip(power, b))
            if any(new_power[i] > joltages[i] for i in range(len(joltages))):
                continue
            if new_power in seen:
                continue
            heappush(todo, (presses + 1, new_power))
            seen.add(new_power)

        # print(f"{len(todo)} {presses} {power} {goal} {len(seen)}")

    # solve: (231, 230, 190, 221, 241, 24, 24)
    # A = [0, 0, 0, 0, 1, 1, 1],
    # B = [1, 1, 0, 1, 1, 0, 0],
    # C = [1, 0, 0, 0, 1, 1, 1],
    # D = [1, 1, 0, 1, 0, 0, 0],
    # E = [1, 1, 1, 1, 1, 0, 0],
    # F = [0, 1, 0, 0, 1, 0, 0]
    # sum(B, C, D, E) = 231
    # sum(B, D, E, F) = 230
    # sum(E) = 190
    assert False, f"Cannot solve {buttons} {joltages}"


def solve_joltages2(buttons, joltages) -> int:
    # buttons = [[1 * (i in b) for i in range(len(joltages))] for b in raw_buttons]
    print(f"solve: {joltages=} {buttons=} {buttons=}")
    mtx = np.array(
        [[(1 if ji in b else 0) for b in buttons] for ji in range(len(joltages))]
    )
    print(mtx, joltages)
    return np.linalg.solve(mtx, joltages)


def factory(input: str) -> int:
    part1, part2 = 0, 0
    for line in input.strip().splitlines():
        line_start = time.time()
        lights, *buttons, joltages = (
            line.replace("(", "")
            .replace(")", "")
            .replace("{", "")
            .replace("}", "")
            .split(" ")
        )
        goal = parse_lights(lights)
        raw_buttons = [vector(b) for b in buttons]
        buttons = [parse_buttons(b) for b in buttons]
        joltages = vector(joltages)
        print(f"{goal:6}/{bin(goal):<10} {raw_buttons} {joltages} ", end="")
        todo = collections.deque()
        todo.append((0, 0))
        while todo:
            presses, lit = todo.popleft()
            if lit == goal:
                break
            for b in buttons:
                lit_now = lit ^ b
                todo.append((presses + 1, lit_now))
        else:
            assert False, "Cannot find any combination of buttons to reach {goal}"
        part1 += presses
        print(f"{presses} -> {time.time() - line_start:.3}s [{part1}]")
        presses = solve_joltages2(raw_buttons, joltages)
        part2 += presses
        print(f"{raw_buttons} -> {joltages}: {presses} [{part2}]")
    return part1, part2


def test_factory():
    ex = """[.##.] (3) (1,3) (2) (2,3) (0,2) (0,1) {3,5,4,7}
[...#.] (0,2,3,4) (2,3) (0,4) (0,1,2) (1,2,3,4) {7,5,12,7,2}
[.###.#] (0,1,2,3,4) (0,3,4) (0,1,2,4,5) (1,2) {10,11,11,5,10,5}"""
    assert 10 == solve_joltages2(
        [(0, 1, 2, 3, 4), (0, 3, 4), (0, 1, 2, 4, 5), (1, 2)], (10, 11, 11, 5, 10, 5)
    )
    assert (7, 33) == factory(ex)


if __name__ == "__main__":
    print(factory(data))
