#!/usr/bin/env python3

'''--- Day 3: No Matter How You Slice It ---

The Elves managed to locate the chimney-squeeze prototype fabric for
Santa's suit (thanks to someone who helpfully wrote its box IDs on the
wall of the warehouse in the middle of the night). Unfortunately,
anomalies are still affecting them - nobody can even agree on how to
cut the fabric.

The whole piece of fabric they're working on is a very large square -
at least 1000 inches on each side.

Each Elf has made a claim about which area of fabric would be ideal
for Santa's suit. All claims have an ID and consist of a single
rectangle with edges parallel to the edges of the fabric. Each claim's
rectangle is defined as follows:

* The number of inches between the left edge of the fabric and the
  left edge of the rectangle.
* The number of inches between the top edge of the fabric and the top
  edge of the rectangle.
* The width of the rectangle in inches.
* The height of the rectangle in inches.

A claim like #123 @ 3,2: 5x4 means that claim ID 123 specifies a
rectangle 3 inches from the left edge, 2 inches from the top edge, 5
inches wide, and 4 inches tall. Visually, it claims the square inches
of fabric represented by # (and ignores the square inches of fabric
represented by .) in the diagram below:

...........
...........
...#####...
...#####...
...#####...
...#####...
...........
...........
...........

The problem is that many of the claims overlap, causing two or more
claims to cover part of the same areas. For example, consider the
following claims:

# 1 @ 1,3: 4x4
# 2 @ 3,1: 4x4
# 3 @ 5,5: 2x2

Visually, these claim the following areas:

........
...2222.
...2222.
.11XX22.
.11XX22.
.111133.
.111133.
........

The four square inches marked with X are claimed by both 1 and
2. (Claim 3, while adjacent to the others, does not overlap either of
them.)

If the Elves all proceed with their own plans, none of them will have
enough fabric. How many square inches of fabric are within two or more
claims?

--- Part Two ---

Amidst the chaos, you notice that exactly one claim doesn't overlap by
even a single square inch of fabric with any other claim. If you can
somehow draw attention to it, maybe the Elves will be able to make
Santa's suit after all!

For example, in the claims above, only claim 3 is intact after all
claims are made.

What is the ID of the only claim that doesn't overlap?
'''

from aoc2018 import *
import numpy as np


def scrub(line):
    result = vector(line.replace(
        '#', '').replace('@', '').replace('x', ' '))
    return result


def line_overlap(l1, l2):
    return max(l1[0], l2[0]) < min(l1[0] + l1[1], l2[0] + l2[1])


def overlaps(s1, s2):
    x1, y1, dx1, dy1 = s1
    x2, y2, dx2, dy2 = s2
    return (line_overlap((x1, dx1), (x2, dx2)) and line_overlap((y1, dy1), (y2, dy2)))


swatches = [scrub(line) for line in Input(3)]
maxx = max(t[1] + t[3] for t in swatches)
maxy = max(t[2] + t[4] for t in swatches)

# print(maxx, maxy)


field = np.zeros((maxx, maxy), dtype=int)
for idx, x, y, dx, dy in swatches:
    field[x:x + dx, y:y + dy] += 1

keys, counts = np.unique(field, return_counts=True)
print(sum(counts[2:]))

swatch_dict = dict((s[0], s[1:]) for s in swatches)
passes = 0
for key, s1 in swatch_dict.items():
    for other, s2 in swatch_dict.items():
        if other == key:
            continue
        if overlaps(s1, s2):
            break
    else:
        print(key, s1, passes)
        break
