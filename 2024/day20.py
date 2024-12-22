#!/usr/bin/env python

from aoc import *
import itertools

NORTH, SOUTH, EAST, WEST = (-1, 0), (1, 0), (0, -1), (0, 1)


def is_node(grid, p):
    """Interesting nodes have turns"""
    if grid[p] in "SE":
        return True
    exits = set()
    for d in (NORTH, SOUTH, EAST, WEST):
        dy, dx = d
        q = p[0] + dy, p[1] + dx
        if grid.get(q) in ".E":
            exits.add(d)
    if len(exits) > 1 and (
        (exits - set([NORTH, SOUTH])) or (exits - set([EAST, WEST]))
    ):
        return True
    return False


def can_reach(grid, p, q):
    if p == q:
        return False
    p, q = min(p, q), max(p, q)
    px, py = p
    qx, qy = q
    if px == qx:
        assert py < qy
        return all(grid[(px, y)] in ".E" for y in range(py, qy))
    if py == qy:
        assert px < qx
        return all(grid[(x, py)] in ".E" for x in range(px, qx))
    return False


def race_condition(input: str, cheat_duration=2, atleast=2, debug=False) -> int:
    grid = parse_grid(input)
    start = next(p for p, c in grid.items() if c == "S")
    finish = next(p for p, c in grid.items() if c == "S")
    nodes = [p for p, c in grid.items() if c in ".SE"]  #  and is_node(grid, p)]
    assert all(n in nodes for n in (start, finish))

    neighbors = defaultdict(set)
    # for p, q in itertools.combinations(nodes, 2):
    #     if can_reach(grid, p, q):
    #         neighbors[p].add(q)
    #         neighbors[q].add(p)
    for p in nodes:
        for n in neighbors4(p):
            if grid.get(n) in ".SE":
                neighbors[p].add(n)

    slow_path = Astar(
        start,
        moves_func=lambda p: neighbors[p],
        cost_func=cityblock_distance,
        h_func=lambda p: 0 if grid[p] == "E" else 1,
    )

    assert slow_path is not None
    slow_path_cost = [
        c
        for c in itertools.accumulate(
            cityblock_distance(p, q) for p, q in itertools.pairwise(slow_path)
        )
    ]

    cheat_saves = defaultdict(set)
    for i, p in enumerate(slow_path):
        for j in range(i + 1, len(slow_path)):
            q = slow_path[j]
            cheat_distance = cityblock_distance(p, q)
            if cheat_distance <= cheat_duration:
                saved = j - i - cheat_distance
                if saved < atleast:
                    continue
                # print(
                #     f"{i}/{p} -> {j}/{q} dist={cityblock_distance(p,q)} saved={saved}"
                # )
                cheat_saves[saved].add((p, q))

    if debug:
        for k, v in sorted(cheat_saves.items()):
            print(f"{k}: {len(v)}")
    return cheat_saves


def count_saves(saves, atleast=0) -> int:
    return sum(len(v) for c, v in saves.items() if c >= atleast)


def main():
    p = Puzzle(year=2024, day=20)
    assert 44 == count_saves(race_condition(p.examples[0].input_data))
    assert {
        50: 32,
        52: 31,
        54: 29,
        56: 39,
        58: 25,
        60: 23,
        62: 20,
        64: 19,
        66: 12,
        68: 14,
        70: 12,
        72: 22,
        74: 4,
        76: 3,
    } == dict(
        (saved, len(cheats))
        for saved, cheats in race_condition(
            p.examples[0].input_data, cheat_duration=20, atleast=50
        ).items()
    )

    p.answer_a = count_saves(race_condition(p.input_data, 2, 100))
    p.answer_b = count_saves(race_condition(p.input_data, 20, 100))
    print(p.answers)


if __name__ == "__main__":
    import sys
    import threading

    threading.stack_size(67108864)  # 64MB stack
    sys.setrecursionlimit(2**20)  # something real big
    # you actually hit the 64MB limit first
    # going by other answers, could just use 2**32-1

    # only new threads get the redefined stack size
    thread = threading.Thread(target=main)
    thread.start()
