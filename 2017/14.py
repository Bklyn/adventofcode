#!/usr/bin/env python3

'''
--- Day 14: Disk Defragmentation ---

Suddenly, a scheduled job activates the system's disk
defragmenter. Were the situation different, you might sit and watch it
for a while, but today, you just don't have that kind of time. It's
soaking up valuable system resources that are needed elsewhere, and so
the only option is to help it finish its task as soon as possible.

The disk in question consists of a 128x128 grid; each square of the
grid is either free or used. On this disk, the state of the grid is
tracked by the bits in a sequence of knot hashes.

A total of 128 knot hashes are calculated, each corresponding to a
single row in the grid; each hash contains 128 bits which correspond
to individual grid squares. Each bit of a hash indicates whether that
square is free (0) or used (1).

The hash inputs are a key string (your puzzle input), a dash, and a
number from 0 to 127 corresponding to the row. For example, if your
key string were flqrgnkx, then the first row would be given by the
bits of the knot hash of flqrgnkx-0, the second row from the bits of
the knot hash of flqrgnkx-1, and so on until the last row,
flqrgnkx-127.

The output of a knot hash is traditionally represented by 32
hexadecimal digits; each of these digits correspond to 4 bits, for a
total of 4 * 32 = 128 bits. To convert to bits, turn each hexadecimal
digit to its equivalent binary value, high-bit first: 0 becomes 0000,
1 becomes 0001, e becomes 1110, f becomes 1111, and so on; a hash that
begins with a0c2017... in hexadecimal would begin with
10100000110000100000000101110000... in binary.

Continuing this process, the first 8 rows and columns for key flqrgnkx
appear as follows, using # to denote used squares, and . to denote
free ones:

##.#.#..-->
.#.#.#.#
....#.#.
#.#.##.#
.##.#...
##..#..#
.#...#..
##.#.##.-->
|      |
V      V

In this example, 8108 squares are used across the entire 128x128 grid.

Given your actual key string, how many squares are used?

Your puzzle input is ugkiagan.

Your puzzle answer was 8292.

The first half of this puzzle is complete! It provides one gold star: *

--- Part Two ---

Now, all the defragmenter needs to know is the number of regions. A
region is a group of used squares that are all adjacent, not including
diagonals. Every used square is in exactly one region: lone used
squares form their own isolated regions, while several adjacent
squares all count as a single region.

In the example above, the following nine regions are visible, each
marked with a distinct digit:

11.2.3..-->
.1.2.3.4
....5.6.
7.8.55.9
.88.5...
88..5..8
.8...8..
88.8.88.-->
|      |
V      V

Of particular interest is the region marked 8; while it does not
appear contiguous in this small view, all of the squares marked 8 are
connected when considering the whole 128x128 grid. In total, in this
example, 1242 regions are present.

How many regions are present given your key string?

Your puzzle input is still ugkiagan.
'''

import operator
from functools import reduce
from aoc2017 import *

def tie_knots(steps, length=256, rounds=64):
    l = [x for x in range(length)]
    pos = 0
    skip = 0
    for r in range(rounds):
        for step in steps:
            for x in range (step // 2):
                i = (pos + x) % length
                j = (pos + step - x - 1) % length
                # print 'pos=%d skip=%d step=%d i=%d j=%d swap=[%d <-> %d]' % (
                # pos, skip, step, i, j, l[i], l[j]),
                l[i], l[j] = l[j], l[i]
                # print l
            pos = (pos + step + skip) % length
            skip += 1
            pass
    return l

assert tie_knots ([3, 4, 1, 5], 5, 1) == [3, 4, 2, 1, 0]

SUFFIX = [17, 31, 73, 47, 23]

def knot_hash (steps):
    if type(steps) == str:
        steps = [ord(x) for x in steps] + SUFFIX
    l = tie_knots (steps)
    return l

def dense_hash(l, fmt='{:08b}'):
    result = []
    for i in range (0, len(l), 16):
        val = reduce (operator.xor, l[i:i+16])
        result.append (val)
    return ''.join ([fmt.format (x) for x in result])

# Part 1
key='ugkiagan'
lines = [dense_hash(knot_hash('{}-{}'.format (key, i)))
         for i in range(128)]
used = sum([x.count('1') for x in lines])
print (used)

# Part 2
# Graph contains the (x,y) coordinates of all '1' points
graph = set([(x, y)
             for y, l in enumerate(lines)
             for x, c in enumerate(l)
             if c == '1'])

# I'm struggling to figure out the more Pythonic way to do this.
def calc_regions(graph):
    to_visit = set(graph)
    regions = []
    while len(to_visit):
        point = to_visit.pop ()
        region = set([point]);
        stack = [point]
        while stack:
            point = stack.pop()
            neigh = set(neighbors4(point)) & to_visit
            region |= neigh
            to_visit -= neigh
            stack.extend (neigh)
        regions.append (region)
    return len(regions)

print (calc_regions (graph))
