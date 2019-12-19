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


def solve_one(maze, key, start, have_keys):
    def goal(pos):
        return 0 if pos == key else 1

    def moves(pos):
        for n in neighbors4(pos):
            glyph = maze.get(n)
            if glyph not in accessible and glyph.lower() not in have_keys:
                continue
            yield n

    solved = Astar(start, moves, goal)
    return solved


def solve(maze, debug=False):
    keys = set(p for p, k in maze.items() if k in string.ascii_lowercase)
    doors = set(p for p, k in maze.items() if k in string.ascii_uppercase)
    start = next(p for p, k in maze.items() if k == "@")
    pos_by_key = dict((k, p) for p, k in maze.items() if k in string.ascii_lowercase)
    key_by_pos = dict((p, k) for p, k in maze.items() if k in string.ascii_lowercase)
    need_keys = "".join(pos_by_key.keys())

    p_to_p = {}
    for k in keys | set([start]):
        for j in keys:
            if k == j:
                continue
            p_to_p[(k, j)] = len(solve_one(maze, k, j, need_keys)) - 1

    def reachable(pos, keys, debug=False):
        have_keys = set(need_keys) - set(keys)
        for k in keys:
            kpos = pos_by_key[k]
            path = solve_one(maze, kpos, pos, have_keys)
            if path:
                if debug:
                    print("REACH", pos, k, have_keys, len(path))
                yield kpos

    def solve_keys(pos, keys, cache=None, debug=False):
        if cache is None:
            cache = {}
        if debug:
            print("SOLVE", pos, keys, len(cache))
        if not keys:
            return 0
        cache_key = (pos, keys)
        result = cache.get(cache_key)
        if result is not None:
            return result
        result = 10 ** 10
        for key in reachable(pos, keys, debug=debug):
            keys_left = "".join(set(keys) - set([key_by_pos[key]]))
            if debug:
                print(
                    "REACHABLE",
                    pos,
                    maze[pos],
                    key_by_pos[key],
                    keys_left,
                    p_to_p[(pos, key)],
                    len(cache),
                )
            d = p_to_p[(pos, key)] + solve_keys(
                key, keys_left, cache=cache, debug=debug
            )
            if debug:
                print(
                    "KEY",
                    pos,
                    key_by_pos[key],
                    keys_left,
                    p_to_p[(pos, key)],
                    d,
                    result,
                    len(cache),
                )
            result = min(result, d)
        if debug:
            print("CACHE", pos, keys, result)
        cache[cache_key] = result
        return result

    return solve_keys(start, need_keys, debug=debug)


EX0 = parse(
    """
########################
#f.D.E.e.C.b.A.@.a.B.c.#
######################.#
#d.....................#
########################
""".strip().splitlines()
)

assert solve(EX0, debug=True) == 86

EX1 = parse(
    """
########################
#...............b.C.D.f#
#.######################
#.....@.a.B.c.d.A.e.F.g#
########################
""".strip().splitlines()
)
assert solve(EX1) == 132

if __name__ == "__main__":
    maze = parse(Input(18).read().strip().splitlines())
    print(len(solve(maze, debug=True)))
