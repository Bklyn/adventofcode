#!/usr/bin/env python3
"""--- Day 24: Planet of Discord ---

You land on Eris, your last stop before reaching Santa. As soon as you
do, your sensors start picking up strange life forms moving around:
Eris is infested with bugs! With an over 24-hour roundtrip for
messages between you and Earth, you'll have to deal with this problem
on your own.

Eris isn't a very large place; a scan of the entire area fits into a
5x5 grid (your puzzle input). The scan shows bugs (#) and empty spaces
(.).

Each minute, The bugs live and die based on the number of bugs in the
four adjacent tiles:

* A bug dies (becoming an empty space) unless there is exactly one bug
  adjacent to it.

* An empty space becomes infested with a bug if exactly one or two
  bugs are adjacent to it.

* Otherwise, a bug or empty space remains the same. (Tiles on the
edges of the grid have fewer than four adjacent tiles; the missing
tiles count as empty space.)

This process happens in every location simultaneously; that is,
within the same minute, the number of adjacent bugs is counted for
every tile first, and then the tiles are updated.

Here are the first few minutes of an example scenario:

Initial state:
....#
#..#.
#..##
..#..
#....

After 1 minute:
#..#.
####.
###.#
##.##
.##..

After 2 minutes:
#####
....#
....#
...#.
#.###

After 3 minutes:
#....
####.
...##
#.##.
.##.#

After 4 minutes:
####.
....#
##..#
.....
##...

To understand the nature of the bugs, watch for the first time a
layout of bugs and empty spaces matches any previous layout. In the
example above, the first layout to appear twice is:

.....
.....
.....
#....
.#...

To calculate the biodiversity rating for this layout, consider each
tile left-to-right in the top row, then left-to-right in the second
row, and so on. Each of these tiles is worth biodiversity points equal
to increasing powers of two: 1, 2, 4, 8, 16, 32, and so on. Add up the
biodiversity points for tiles with bugs; in this example, the 16th
tile (32768 points) and 22nd tile (2097152 points) have bugs, a total
biodiversity rating of 2129920.

What is the biodiversity rating for the first layout that appears
twice?

--- Part Two ---

After careful analysis, one thing is certain: you have no idea where
all these bugs are coming from.

Then, you remember: Eris is an old Plutonian settlement! Clearly, the
bugs are coming from recursively-folded space.

This 5x5 grid is only one level in an infinite number of recursion
levels. The tile in the middle of the grid is actually another 5x5
grid, the grid in your scan is contained as the middle tile of a
larger 5x5 grid, and so on. Two levels of grids look like this:


     |     |         |     |
     |     |         |     |
     |     |         |     |
-----+-----+---------+-----+-----
     |     |         |     |
     |     |         |     |
     |     |         |     |
-----+-----+---------+-----+-----
     |     | | | | | |     |
     |     |-+-+-+-+-|     |
     |     | | | | | |     |
     |     |-+-+-+-+-|     |
     |     | | |?| | |     |
     |     |-+-+-+-+-|     |
     |     | | | | | |     |
     |     |-+-+-+-+-|     |
     |     | | | | | |     |
-----+-----+---------+-----+-----
     |     |         |     |
     |     |         |     |
     |     |         |     |
-----+-----+---------+-----+-----
     |     |         |     |
     |     |         |     |
     |     |         |     |

(To save space, some of the tiles are not drawn to scale.) Remember,
this is only a small part of the infinitely recursive grid; there is a
5x5 grid that contains this diagram, and a 5x5 grid that contains that
one, and so on. Also, the ? in the diagram contains another 5x5 grid,
which itself contains another 5x5 grid, and so on.

The scan you took (your puzzle input) shows where the bugs are on a
single level of this structure. The middle tile of your scan is empty
to accommodate the recursive grids within it. Initially, no other
levels contain bugs.

Tiles still count as adjacent if they are directly up, down, left, or
right of a given tile. Some tiles have adjacent tiles at a recursion
level above or below its own level. For example:

     |     |         |     |
  1  |  2  |    3    |  4  |  5
     |     |         |     |
-----+-----+---------+-----+-----
     |     |         |     |
  6  |  7  |    8    |  9  |  10
     |     |         |     |
-----+-----+---------+-----+-----
     |     |A|B|C|D|E|     |
     |     |-+-+-+-+-|     |
     |     |F|G|H|I|J|     |
     |     |-+-+-+-+-|     |
 11  | 12  |K|L|?|N|O|  14 |  15
     |     |-+-+-+-+-|     |
     |     |P|Q|R|S|T|     |
     |     |-+-+-+-+-|     |
     |     |U|V|W|X|Y|     |
-----+-----+---------+-----+-----
     |     |         |     |
 16  | 17  |    18   |  19 |  20
     |     |         |     |
-----+-----+---------+-----+-----
     |     |         |     |
 21  | 22  |    23   |  24 |  25
     |     |         |     |

Tile 19 has four adjacent tiles: 14, 18, 20, and 24.
Tile G has four adjacent tiles: B, F, H, and L.
Tile D has four adjacent tiles: 8, C, E, and I.
Tile E has four adjacent tiles: 8, D, 14, and J.
Tile 14 has eight adjacent tiles: 9, E, J, O, T, Y, 15, and 19.
Tile N has eight adjacent tiles: I, O, S, and five tiles within the sub-grid marked ?.

The rules about bugs living and dying are the same as before.

For example, consider the same initial state as above:

....#
#..#.
#.?##
..#..
#....

The center tile is drawn as ? to indicate the next recursive
grid. Call this level 0; the grid within this one is level 1, and the
grid that contains this one is level -1. Then, after ten minutes, the
grid at each level would look like this:

Depth -5:

..#..
.#.#.
..?.#
.#.#.
..#..

Depth -4:

...#.
...##
..?..
...##
...#.

Depth -3:

#.#..
.#...
..?..
.#...
#.#..

Depth -2:

.#.##
....#
..?.#
...##
.###.

Depth -1:

#..##
...##
..?..
...#.
.####

Depth 0:

.#...
.#.##
.#?..
.....
.....

Depth 1:

.##..
#..##
..?.#
##.##
#####

Depth 2:

###..
##.#.
#.?..
.#.##
#.#..

Depth 3:

..###
.....
#.?..
#....
#...#

Depth 4:

.###.
#..#.
#.?..
##.#.
.....

Depth 5:

####.
#..#.
#.?#.
####.
.....

In this example, after 10 minutes, a total of 99 bugs are present.

Starting with your scan, how many bugs are present after 200 minutes?
"""


from collections import defaultdict


def parse(input):
    bits = 0
    bval = 1
    for y, line in enumerate(input):
        for x, c in enumerate(line.strip()):
            bits += bval if c == "#" else 0
            bval *= 2
    return bits


def make_neighbors():
    nb = defaultdict(set)
    for idx in range(25):
        if idx == 12:
            continue
        x, y = idx % 5, idx // 5
        for dx, dy in ((-1, 0), (0, -1), (1, 0), (0, 1)):
            xx, yy = x + dx, y + dy
            if xx >= 0 and xx < 5 and yy >= 0 and yy < 5 and (xx, yy) != (2, 2):
                oidx = 5 * yy + xx
                nb[idx].add((oidx, 0))
        if x == 0:
            nb[idx].add((11, -1))
            nb[11].add((idx, 1))
        if y == 0:
            nb[idx].add((7, -1))
            nb[7].add((idx, 1))
        if x == 4:
            nb[idx].add((13, -1))
            nb[13].add((idx, 1))
        if y == 4:
            nb[idx].add((17, -1))
            nb[17].add((idx, 1))
    for idx in sorted(nb):
        # x, y = idx % 5, idx // 5
        # print("NB", idx, (x, y), sorted(nb[idx]), n2)
        pass
    return nb


NEIGH = make_neighbors()


def neighbors(idx):
    x, y = idx % 5, idx // 5
    for x, y in ((x - 1, y), (x, y - 1), (x + 1, y), (x, y + 1)):
        if x >= 0 and x < 5 and y >= 0 and y < 5:
            yield 5 * y + x


def evolve(bits):
    result = 0
    for idx in range(25):
        mask = 1 << idx
        n = sum((bits & (1 << x)) != 0 for x in neighbors(idx))
        if bits & mask:
            if n == 1:
                result |= mask
        else:
            if n in (1, 2):
                result |= mask
    return result


def count_bits(bits):
    result = 0
    while bits:
        if bits & 1:
            result += 1
        bits >>= 1
    return result


def evolve_recursive(bits, rounds=200, debug=False):
    world = defaultdict(int)
    world[0] = bits
    for r in range(rounds):
        result = defaultdict(int)
        levels = list(world.keys())
        levels += [min(levels) - 1, max(levels) + 1]
        for level in sorted(levels):
            bits = world[level]
            for idx in range(25):
                n = sum(world[level + dl] & (1 << x) != 0 for x, dl in NEIGH[idx])
                mask = 1 << idx
                out = 0
                if bits & mask:
                    if n == 1:
                        out = mask
                elif n in (1, 2):
                    out = mask
                result[level] |= out
            if debug and r == rounds - 1 and result[level]:
                render(result[level], "LEVEL:{}:{}".format(level, r + 1))
        world = result
    return world
    count = sum(count_bits(bits) for bits in world.values())
    return count


def render(bits, label):
    assert bits & (1 << 12) == 0
    for y in range(5):
        if label:
            print(label, end=" ")
        print(
            "".join(
                "#" if bits & 1 << (5 * y + x) else "." if (x, y) != (2, 2) else "?"
                for x in range(5)
            )
        )


EXAMPLE = [
    parse(ex.strip().splitlines())
    for ex in [
        """
....#
#..#.
#..##
..#..
#....""",
        """
#..#.
####.
###.#
##.##
.##..""",
        """
#####
....#
....#
...#.
#.###""",
        """
#....
####.
...##
#.##.
.##.#""",
        """
####.
....#
##..#
.....
##...
""",
    ]
]

EX2 = """
....#
#..#.
#.?##
..#..
#....
"""

R2 = evolve_recursive(parse(EX2.strip().splitlines()), 10)
assert sum(count_bits(b) for b in R2.values()) == 99, R2

state = EXAMPLE[0]
for expect in EXAMPLE[1:]:
    state = evolve(state)
    if state != expect:
        render(state, "BAD")
        print("")
        render(expect, "EXP")
        assert False

if __name__ == "__main__":
    bits = parse(open("24.txt").read().splitlines())
    seen = set()
    while bits not in seen:
        seen.add(bits)
        bits = evolve(bits)
    print(bits)
    # Solve the recursive problem
    bits = parse(open("24.txt").read().splitlines())
    world = evolve_recursive(bits, rounds=200)
    print(sum(count_bits(b) for b in world.values()))
