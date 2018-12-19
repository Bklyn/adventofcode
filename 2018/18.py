#!/usr/bin/env python3
'''--- Day 18: Settlers of The North Pole ---

On the outskirts of the North Pole base construction project, many
Elves are collecting lumber.

The lumber collection area is 50 acres by 50 acres; each acre can be
either open ground (.), trees (|), or a lumberyard (#). You take a
scan of the area (your puzzle input).

Strange magic is at work here: each minute, the landscape looks
entirely different. In exactly one minute, an open acre can fill with
trees, a wooded acre can be converted to a lumberyard, or a lumberyard
can be cleared to open ground (the lumber having been sent to other
projects).

The change to each acre is based entirely on the contents of that acre
as well as the number of open, wooded, or lumberyard acres adjacent to
it at the start of each minute. Here, "adjacent" means any of the
eight acres surrounding that acre. (Acres on the edges of the lumber
collection area might have fewer than eight adjacent acres; the
missing acres aren't counted.)

In particular:

* An open acre will become filled with trees if three or more adjacent
acres contained trees. Otherwise, nothing happens.

* An acre filled with trees will become a lumberyard if three or more
adjacent acres were lumberyards. Otherwise, nothing happens.

* An acre containing a lumberyard will remain a lumberyard if it was
adjacent to at least one other lumberyard and at least one acre
containing trees. Otherwise, it becomes open.

These changes happen across all acres simultaneously, each of them
using the state of all acres at the beginning of the minute and
changing to their new form by the end of that same minute. Changes
that happen during the minute don't affect each other.

For example, suppose the lumber collection area is instead only 10 by
10 acres with this initial configuration:

Initial state:

.#.#...|#.
.....#|##|
.|..|...#.
..|#.....#
#.#|||#|#|
...#.||...
.|....|...
||...#|.#|
|.||||..|.
...#.|..|.

After 1 minute:
.......##.
......|###
.|..|...#.
..|#||...#
..##||.|#|
...#||||..
||...|||..
|||||.||.|
||||||||||
....||..|.

After 2 minutes:
.......#..
......|#..
.|.|||....
..##|||..#
..###|||#|
...#|||||.
|||||||||.
||||||||||
||||||||||
.|||||||||

After 3 minutes:
.......#..
....|||#..
.|.||||...
..###|||.#
...##|||#|
.||##|||||
||||||||||
||||||||||
||||||||||
||||||||||

After 4 minutes:
.....|.#..
...||||#..
.|.#||||..
..###||||#
...###||#|
|||##|||||
||||||||||
||||||||||
||||||||||
||||||||||

After 5 minutes:
....|||#..
...||||#..
.|.##||||.
..####|||#
.|.###||#|
|||###||||
||||||||||
||||||||||
||||||||||
||||||||||

After 6 minutes:
...||||#..
...||||#..
.|.###|||.
..#.##|||#
|||#.##|#|
|||###||||
||||#|||||
||||||||||
||||||||||
||||||||||

After 7 minutes:
...||||#..
..||#|##..
.|.####||.
||#..##||#
||##.##|#|
|||####|||
|||###||||
||||||||||
||||||||||
||||||||||

After 8 minutes:
..||||##..
..|#####..
|||#####|.
||#...##|#
||##..###|
||##.###||
|||####|||
||||#|||||
||||||||||
||||||||||

After 9 minutes:
..||###...
.||#####..
||##...##.
||#....###
|##....##|
||##..###|
||######||
|||###||||
||||||||||
||||||||||

After 10 minutes:
.||##.....
||###.....
||##......
|##.....##
|##.....##
|##....##|
||##.####|
||#####|||
||||#|||||
||||||||||

After 10 minutes, there are 37 wooded acres and 31
lumberyards. Multiplying the number of wooded acres by the number of
lumberyards gives the total resource value after ten minutes: 37 * 31
= 1147.

What will the total resource value of the lumber collection area be after 10 minutes?
'''

from aoc2018 import *
import collections


class Point(collections.namedtuple('Point', ['y', 'x'])):
    def __add__(self, other):
        return type(self)(self.y + other.y, self.x + other.x)

    @property
    def neighbors(self):
        return [self + step for step in [Point(-1, -1), Point(0, -1), Point(1, -1),
                                         Point(-1, 0), Point(1, 0),
                                         Point(-1, 1), Point(0, 1), Point(1, 1)]]


OPEN, TREE, YARD = '.', '|', '#'


class Forest(dict):
    def __init__(self, lines):
        super().__init__(self)
        if isinstance(lines, str):
            lines = lines.splitlines()
        rows, cols = (0, 0)
        for y, row in enumerate(lines):
            rows += 1
            row = row.strip()
            cols = max(cols, len(row))
            for x, c in enumerate(row):
                p = Point(y, x)
                self[Point(y, x)] = c
        self.shape = (rows, cols)

    def dump(self):
        rows, cols = self.shape
        for y in range(rows):
            line = [self.get(Point(y, x), '%') for x in range(cols)]
            print(''.join(line))

    def score(self):
        count = Counter(t for p, t in self.items())
        return count.get(TREE, 0) * count.get(YARD, 0)

    def tick(self):
        snap = dict((k, v) for k, v in self.items())
        for point, glyph in snap.items():
            neighbors = Counter(snap[n] for n in point.neighbors if n in snap)
            if glyph == OPEN and neighbors.get(TREE, 0) >= 3:
                glyph = TREE
            elif glyph == TREE and neighbors.get(YARD, 0) >= 3:
                glyph = YARD
            elif glyph == YARD and not (
                    neighbors.get(YARD, 0) >= 1
                    and neighbors.get(TREE, 0) >= 1):
                glyph = OPEN
            self[point] = glyph

    def solve(self, ticks=10, verbose=False):
        if verbose:
            self.dump()
        for tick in range(ticks):
            self.tick()
            if verbose:
                self.dump()


f = Forest(Input(18))
f.solve()
print(f.score())
