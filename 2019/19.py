#!/usr/bin/env python3
"""--- Day 19: Tractor Beam ---

Unsure of the state of Santa's ship, you borrowed the tractor beam
technology from Triton. Time to test it out.

When you're safely away from anything else, you activate the tractor
beam, but nothing happens. It's hard to tell whether it's working if
there's nothing to use it on. Fortunately, your ship's drone system
can be configured to deploy a drone to specific coordinates and then
check whether it's being pulled. There's even an Intcode program (your
puzzle input) that gives you access to the drone system.

The program uses two input instructions to request the X and Y
position to which the drone should be deployed. Negative numbers are
invalid and will confuse the drone; all numbers should be zero or
positive.

Then, the program will output whether the drone is stationary (0) or
being pulled by something (1). For example, the coordinate X=0, Y=0 is
directly in front of the tractor beam emitter, so the drone control
program will always report 1 at that location.

To better understand the tractor beam, it is important to get a good
picture of the beam itself. For example, suppose you scan the 10x10
grid of points closest to the emitter:

       X
  0->      9
 0#.........
 |.#........
 v..##......
  ...###....
  ....###...
Y .....####.
  ......####
  ......####
  .......###
 9........##

In this example, the number of points affected by the tractor beam in
the 10x10 area closest to the emitter is 27.

However, you'll need to scan a larger area to understand the shape of
the beam. How many points are affected by the tractor beam in the
50x50 area closest to the emitter? (For each of X and Y, this will be
0 through 49.)

--- Part Two ---

You aren't sure how large Santa's ship is. You aren't even sure if
you'll need to use this thing on Santa's ship, but it doesn't hurt to
be prepared. You figure Santa's ship might fit in a 100x100 square.

The beam gets wider as it travels away from the emitter; you'll need
to be a minimum distance away to fit a square of that size into the
beam fully. (Don't rotate the square; it should be aligned to the same
axes as the drone grid.)

For example, suppose you have the following tractor beam readings:

#.......................................
.#......................................
..##....................................
...###..................................
....###.................................
.....####...............................
......#####.............................
......######............................
.......#######..........................
........########........................
.........#########......................
..........#########.....................
...........##########...................
...........############.................
............############................
.............#############..............
..............##############............
...............###############..........
................###############.........
................#################.......
.................########OOOOOOOOOO.....
..................#######OOOOOOOOOO#....
...................######OOOOOOOOOO###..
....................#####OOOOOOOOOO#####
.....................####OOOOOOOOOO#####
.....................####OOOOOOOOOO#####
......................###OOOOOOOOOO#####
.......................##OOOOOOOOOO#####
........................#OOOOOOOOOO#####
.........................OOOOOOOOOO#####
..........................##############
..........................##############
...........................#############
............................############
.............................###########

In this example, the 10x10 square closest to the emitter that fits
entirely within the tractor beam has been marked O. Within it, the
point closest to the emitter (the only highlighted O) is at X=25,
Y=20.

Find the 100x100 square closest to the emitter that fits entirely
within the tractor beam; within that square, find the point closest to
the emitter. What value do you get if you take that point's X
coordinate, multiply it by 10000, then add the point's Y coordinate?
(In the example above, this would be 250020.)
"""

from aoc import *
from intcode import Intcode


class Tractor(Intcode):
    def __init__(self, tape, input):
        super(Tractor, self).__init__(tape, input=input)

    def print(self):
        print(self.output)
        idx = 0
        while idx < len(self.output):
            print(
                "".join("." if val == 0 else "#" for val in self.output[idx : idx + 50])
            )
            idx += 50


def part1(tape, debug=False):
    total = 0
    for y in range(50):
        line = ""
        for x in range(50):
            result = Tractor(tape, input=[x, y]).run()
            line += "#" if result == 1 else "."
        if debug:
            print(line)
        total += sum(c == "#" for c in line)
    return total


if __name__ == "__main__":
    tape = list(vector(Input(19).read().strip()))
    # print(part1(tape, debug=True))

    def in_beam(x, y, debug=False):
        result = Tractor(tape, input=[x, y]).run() == 1
        if debug:
            print("\r", x, y, result, end="")
        return result

    def beam_width(x, y, debug=False):
        low, high = x, 10 ** 10
        while low < high:
            x = (low + high) // 2
            result = in_beam(x, y)
            if debug > 1:
                print("WIDTH", y, low, high, x, result)
            if result and low != x:
                low = x
            else:
                high = x - 1
        return low

    def lower_bound(y, first=0, last=10 ** 10, comp=identity, debug=False):
        count = last - first
        while count > 0:
            step = count // 2
            mid = first + step
            value = in_beam(mid, y)
            if debug:
                print("LB", first, last, mid, value, comp(value))
            if comp(value):
                first = mid + 1
                count -= step + 1
            else:
                count = step
        return first

    x, y = 4, 3
    slen = 100 - 1
    lines = {}

    while True:
        while not in_beam(x, y):
            x += 1
        if not in_beam(x + slen, y):
            y += 1
            continue
        lb = x
        ub = lower_bound(y, first=x)
        if ub - lb < slen:
            continue
        # print(
        #     "LINE",
        #     (x, y),
        #     lb,
        #     ub,
        #     # " " * lb
        #     # + "".join(
        #     #    ("#" if in_beam(x, y) else ".") for x in range(max(0, lb - 1), ub + 1)
        #     # ),
        # )
        width = ub - lb + 1  # beam_width(x, y, debug=True)
        for dx in range(x, width):
            if (
                in_beam(dx, y - slen)
                and in_beam(dx + slen, y - slen)
                and in_beam(dx + slen, y)
            ):
                x = dx
                break
        if all(
            in_beam(x, y)
            for x, y in ((x + slen, y), (x, y - slen), (x + slen, y - slen))
        ):
            y -= slen
            break
        x, y = x + 1, y + 1
    print(
        x,
        y,
        [
            in_beam(x, y)
            for x, y in [(x, y), (x + slen, y), (x, y + slen), (x + slen, y + slen)]
        ],
    )
    print(10000 * x + y)
