#!/usr/bin/env python3

'''--- Day 11: Chronal Charge ---

You watch the Elves and their sleigh fade into the distance as they
head toward the North Pole.

Actually, you're the one fading. The falling sensation returns.

The low fuel warning light is illuminated on your wrist-mounted
device. Tapping it once causes it to project a hologram of the
situation: a 300x300 grid of fuel cells and their current power
levels, some negative. You're not sure what negative power means in
the context of time travel, but it can't be good.

Each fuel cell has a coordinate ranging from 1 to 300 in both the X
(horizontal) and Y (vertical) direction. In X,Y notation, the top-left
cell is 1,1, and the top-right cell is 300,1.

The interface lets you select any 3x3 square of fuel cells. To
increase your chances of getting to your destination, you decide to
choose the 3x3 square with the largest total power.

The power level in a given fuel cell can be found through the
following process:

Find the fuel cell's rack ID, which is its X coordinate plus 10.
Begin with a power level of the rack ID times the Y coordinate.
Increase the power level by the value of the grid serial number (your puzzle input).
Set the power level to itself multiplied by the rack ID.
Keep only the hundreds digit of the power level (so 12345 becomes 3; numbers with no hundreds digit become 0).
Subtract 5 from the power level.

For example, to find the power level of the fuel cell at 3,5 in a grid
with serial number 8:

The rack ID is 3 + 10 = 13.
The power level starts at 13 * 5 = 65.
Adding the serial number produces 65 + 8 = 73.
Multiplying by the rack ID produces 73 * 13 = 949.
The hundreds digit of 949 is 9.
Subtracting 5 produces 9 - 5 = 4.
So, the power level of this fuel cell is 4.

Here are some more example power levels:

Fuel cell at  122,79, grid serial number 57: power level -5.
Fuel cell at 217,196, grid serial number 39: power level  0.
Fuel cell at 101,153, grid serial number 71: power level  4.

Your goal is to find the 3x3 square which has the largest total
power. The square must be entirely within the 300x300 grid. Identify
this square using the X,Y coordinate of its top-left fuel cell. For
example:

For grid serial number 18, the largest total 3x3 square has a top-left
corner of 33,45 (with a total power of 29); these fuel cells appear in
the middle of this 5x5 region:

-2  -4   4   4   4
-4   4   4   4  -5
 4   3   3   4  -4
 1   1   2   4  -3
-1   0   2  -5  -2

For grid serial number 42, the largest 3x3 square's top-left is 21,61
(with a total power of 30); they are in the middle of this region:

-3   4   2   2   2
-4   4   3   3   4
-5   3   3   4  -4
 4   3   3   4  -3
 3   3   3  -5  -1

What is the X,Y coordinate of the top-left fuel cell of the 3x3 square
with the largest total power?

Your puzzle input is 2694.

--- Part Two ---

You discover a dial on the side of the device; it seems to let you
select a square of any size, not just 3x3. Sizes from 1x1 to 300x300
are supported.

Realizing this, you now must find the square of any size with the
largest total power. Identify this square by including its size as a
third parameter after the top-left coordinate: a 9x9 square with a
top-left corner of 3,5 is identified as 3,5,9.

For example:

For grid serial number 18, the largest total square (with a total
power of 113) is 16x16 and has a top-left corner of 90,269, so its
identifier is 90,269,16.

For grid serial number 42, the largest total square (with a total
power of 119) is 12x12 and has a top-left corner of 232,251, so its
identifier is 232,251,12.

What is the X,Y,size identifier of the square with the largest total power?
'''

from aoc2018 import *
import numpy as np


def power_level(p, serial):
    rack = 10 + X(p)
    power = rack * (Y(p) * rack + serial)
    power = ((power // 100) % 10) - 5
    return power


def power_grid(serial, dim=300):
    grid = np.array([
        [power_level((x + 1, y + 1), serial) for x in range(dim)] for y in range(dim)])
    return grid


def solve1(serial):
    grid = dict(((x, y), power_level((x, y), serial))
                for y in range(1, 301) for x in range(1, 301))
    max_score = 0
    for y in range(2, 300):
        for x in range(2, 300):
            center = (x, y)
            score = sum(grid[p] for p in neighbors8(center)) + grid[center]
            if score > max_score:
                max_score = score
                answer = (x - 1, y - 1)
    return answer, max_score


def gridrow(grid, x, y, size):
    return grid[y, x:x + size]


def gridcol(grid, x, y, size):
    return grid[y:y + size, x]


def solve2(grid, limit=None, debug=False):
    maxx, maxy = grid.shape
    if limit is None:
        limit = maxy
    answer = (0, 0, 0, 0)
    for y in range(maxy):
        for x in range(maxx):
            maxlen = min(limit, maxy - max(x, y))
            total = 0
            for size in range(1, maxlen + 1):
                row = gridrow(grid, x, y + size - 1, size)
                col = gridcol(grid, x + size - 1, y, size)
                total += row.sum() + col.sum() - col[-1]
                if total > answer[-1]:
                    if debug:
                        print('BEST', (x + 1, y + 1), size, total)
                    answer = (x + 1, y + 1, size, total)
    return answer


assert power_level((3, 5), 8) == 4
assert power_level((122, 79), 57) == -5
assert power_level((217, 196), 39) == 0
assert power_level((101, 153), 71) == 4

assert solve1(18) == ((33, 45), 29)
assert solve1(42) == ((21, 61), 30)

Input = power_grid(2694)
# print(solve1(2694))  # Input, lowlimit=3, limit=3, debug=True))
print(solve2(Input, limit=3))
print(solve2(Input))
