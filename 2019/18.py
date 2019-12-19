#!/usr/bin/env python3
"""--- Day 18: Many-Worlds Interpretation ---

As you approach Neptune, a planetary security system detects you and
activates a giant tractor beam on Triton! You have no choice but to
land.

A scan of the local area reveals only one interesting feature: a
massive underground vault. You generate a map of the tunnels (your
puzzle input). The tunnels are too narrow to move diagonally.

Only one entrance (marked @) is present among the open passages
(marked .) and stone walls (#), but you also detect an assortment of
keys (shown as lowercase letters) and doors (shown as uppercase
letters). Keys of a given letter open the door of the same letter: a
opens A, b opens B, and so on. You aren't sure which key you need to
disable the tractor beam, so you'll need to collect all of them.

For example, suppose you have the following map:

#########
#b.A.@.a#
#########

Starting from the entrance (@), you can only access a large door (A)
and a key (a). Moving toward the door doesn't help you, but you can
move 2 steps to collect the key, unlocking A in the process:

#########
#b.....@#
#########

Then, you can move 6 steps to collect the only other key, b:

#########
#@......#
#########

So, collecting every key took a total of 8 steps.

Here is a larger example:

########################
#f.D.E.e.C.b.A.@.a.B.c.#
######################.#
#d.....................#
########################

The only reasonable move is to take key a and unlock door A:

########################
#f.D.E.e.C.b.....@.B.c.#
######################.#
#d.....................#
########################

Then, do the same with key b:

########################
#f.D.E.e.C.@.........c.#
######################.#
#d.....................#
########################

...and the same with key c:

########################
#f.D.E.e.............@.#
######################.#
#d.....................#
########################

Now, you have a choice between keys d and e. While key e is closer,
collecting it now would be slower in the long run than collecting key
d first, so that's the best choice:

########################
#f...E.e...............#
######################.#
#@.....................#
########################

Finally, collect key e to unlock door E, then collect key f, taking a grand total of 86 steps.

Here are a few more examples:

########################
#...............b.C.D.f#
#.######################
#.....@.a.B.c.d.A.e.F.g#
########################

Shortest path is 132 steps: b, a, c, d, f, e, g

#################
#i.G..c...e..H.p#
########.########
#j.A..b...f..D.o#
########@########
#k.E..a...g..B.n#
########.########
#l.F..d...h..C.m#
#################

Shortest paths are 136 steps;
one is: a, f, b, j, g, n, h, d, l, o, e, p, c, i, k, m

########################
#@..............ac.GI.b#
###d#e#f################
###A#B#C################
###g#h#i################
########################

Shortest paths are 81 steps; one is: a, c, f, i, d, g, b, e, h

How many steps is the shortest path that collects all of the keys?
"""

import string
from aoc import *
from collections import deque


def parse(lines):
    maze = {}
    y = 0
    for line in [l.strip() for l in lines]:
        for x, c in enumerate(line):
            pos = (x, y)
            maze[pos] = c
        y = y + 1
    return maze


accessible = set([".", "@"] + list(string.ascii_lowercase))


def solve_one(maze, key, start, open_doors):
    def goal(pos):
        return 0 if pos == key else 1

    def moves(pos):
        for n in neighbors4(pos):
            glyph = maze.get(n)
            if glyph not in accessible and glyph not in open_doors:
                continue
            yield n

    solved = Astar(start, moves, goal)
    return solved


def calc_opened(maze, keys, path):
    seen = set()
    result = []
    for p in path:
        if p in seen:
            continue
        if p in keys and p not in seen:
            result.append(maze[p].upper())
            seen.add(p)
    return result


def solve(maze, debug=False):
    keys = set(p for p, k in maze.items() if k in string.ascii_lowercase)
    doors = set(p for p, k in maze.items() if k in string.ascii_uppercase)
    start = next(p for p, k in maze.items() if k == "@")
    p_to_p = {}
    for k in keys | set([start]):
        for j in keys | set([start]):
            if k == j:
                continue
            p_to_p[(k, j)] = len(solve_one(maze, k, j, string.ascii_uppercase))

    # State consists of (start point, remaining keys, full path)
    todo = [(start, keys, [], [])]
    best = None
    blen = 10 ** 9
    while todo:
        begin, remain, path, opened = todo.pop()
        if len(path) > blen:
            continue
        if not remain and len(path) < blen:
            print("BEST", len(path), "".join(opened))
            best = path
            blen = len(path)
            continue
        for key in sorted(remain, key=lambda p: p_to_p[(begin, p)], reverse=True):
            key_path = solve_one(maze, key, begin, opened)
            if key_path is None:
                continue
            if debug > 1:
                print(
                    blen,
                    len(todo),
                    maze[key],
                    len(remain),
                    len(path),
                    len(key_path),
                    "".join(opened),
                )
            todo.append(
                (
                    key_path[-1],
                    remain - set([key]),
                    path + key_path[1:],
                    opened + [maze[key].upper()],
                )
            )
    return best


EX0 = parse(
    """
########################
#f.D.E.e.C.b.A.@.a.B.c.#
######################.#
#d.....................#
########################
""".strip().splitlines()
)

assert len(solve(EX0)) == 86

EX1 = parse(
    """
########################
#...............b.C.D.f#
#.######################
#.....@.a.B.c.d.A.e.F.g#
########################
""".strip().splitlines()
)
assert len(solve(EX1)) == 132

if __name__ == "__main__":
    maze = parse(Input(18).read().strip().splitlines())
    print(len(solve(maze, debug=2)))
