#!/usr/bin/env python3

'''--- Day 11: Hex Ed ---

Crossing the bridge, you've barely reached the other side of the
stream when a program comes up to you, clearly in distress. "It's my
child process," she says, "he's gotten lost in an infinite grid!"

Fortunately for her, you have plenty of experience with infinite
grids.

Unfortunately for you, it's a hex grid.

The hexagons ("hexes") in this grid are aligned such that adjacent
hexes can be found to the north, northeast, southeast, south,
southwest, and northwest:

  \ n  /
nw +--+ ne
  /    \
-+      +-
  \    /
sw +--+ se
  / s  \

You have the path the child process took. Starting where he started,
you need to determine the fewest number of steps required to reach
him. (A "step" means to move from the hex you are in to any adjacent
hex.)

For example:

ne,ne,ne is 3 steps away.
ne,ne,sw,sw is 0 steps away (back where you started).
ne,ne,s,s is 2 steps away (se,se).
se,sw,se,sw,sw is 3 steps away (s,s,sw).

'''

from aoc2017 import *

# Using axial coordinates.  See https://www.redblobgames.com/grids/hexagons/
HexSteps = { 'n': (0, -1), 'ne': (1, -1), 'se': (1, 0),
             's': (0,  1), 'sw': (-1, 1), 'nw': (-1, 0) }

def move_hex(point, steps):
    q, r = point
    if type(steps) is str:
        steps = steps.strip ().split (',')
    for step in steps:
        dq, dr = HexSteps[step]
        q, r = q+dq, r+dr
    return (q, r)

def to_cube(point):
    p, q = point
    return (p, q, -p-q)

def hex_distance (p, q=(0,0)):
    p, q = to_cube (p), to_cube (q)
    return max (abs (X(p)-X(q)), abs(Y(p)-Y(q)), abs(p[2]-q[2]))

assert hex_distance (move_hex((0,0), ['ne', 'ne', 'ne'])) == 3
assert hex_distance (move_hex((0,0), 'ne,ne,sw,sw')) == 0
assert hex_distance (move_hex((0,0), 'ne,ne,s,s')) == 2
assert hex_distance (move_hex((0,0), 'se,sw,se,sw,sw')) == 3

steps = Input(11).read().strip().split (',')

# Part 1 + 2
farthest = 0
loc = (0,0)
for step in steps:
    loc = move_hex (loc, step)
    farthest = max (farthest, hex_distance (loc))
print (hex_distance (loc))
print (farthest)
