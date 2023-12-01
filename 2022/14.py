#!/usr/bin/env python3.9

from aoc import *


def cavern(input, part_b=False):
    cave = set()
    maxy = 0
    for line in input.splitlines():
        prev = None
        for p in line.split(" -> "):
            p = tuple(int(a) for a in p.split(","))
            if prev is not None:
                x0, x1 = min(X(prev), X(p)), max(X(prev), X(p))
                y0, y1 = min(Y(prev), Y(p)), max(Y(prev), Y(p))
                maxy = max(maxy, y1 + (2 if part_b else 0))
                points = set(
                    (x, y) for y in range(y0, y1 + 1) for x in range(x0, x1 + 1)
                )
                cave |= points
            prev = p

    def moves(p):
        for x, y in ((0, 1), (-1, 1), (1, 1)):
            yield (X(p) + x, Y(p) + y)

    grains = set()
    done = False
    while (p := (500, 0)) not in grains and not done:
        move = 0
        while p not in grains and not done:
            for q in moves(p):
                if q in cave or q in grains:
                    continue
                if part_b and Y(q) == maxy:
                    grains.add(p)
                    break
                if not part_b and Y(q) >= maxy:
                    done = True
                p = q
                break
            else:
                grains.add(p)
                break
            move += 1
            if move > 1000:
                done = True
                break

    return len(grains)


p = Puzzle(day=14)
assert cavern(p.example_data) == 24
assert cavern(p.example_data, True) == 93

# p.answer_a = cavern(p.input_data)
assert cavern(p.input_data, True) == 27426
