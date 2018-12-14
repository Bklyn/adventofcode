#!/usr/bin/env python3
'''--- Day 13: Mine Cart Madness ---

A crop of this size requires significant logistics to transport
produce, soil, fertilizer, and so on. The Elves are very busy pushing
things around in carts on some kind of rudimentary system of tracks
they've come up with.

Seeing as how cart-and-track systems don't appear in recorded history
for another 1000 years, the Elves seem to be making this up as they go
along. They haven't even figured out how to avoid collisions yet.

You map out the tracks (your puzzle input) and see where you can help.

Tracks consist of straight paths (| and -), curves (/ and \), and
intersections (+). Curves connect exactly two perpendicular pieces of
track; for example, this is a closed loop:

/----\
|    |
|    |
\----/

Intersections occur when two perpendicular paths cross. At an
intersection, a cart is capable of turning left, turning right, or
continuing straight. Here are two loops connected by two
intersections:

/-----\
|     |
|  /--+--\
|  |  |  |
\--+--/  |
   |     |
   \-----/

Several carts are also on the tracks. Carts always face either up (^),
down (v), left (<), or right (>). (On your initial map, the track
under each cart is a straight path matching the direction the cart is
facing.)

Each time a cart has the option to turn (by arriving at any
intersection), it turns left the first time, goes straight the second
time, turns right the third time, and then repeats those directions
starting again with left the fourth time, straight the fifth time, and
so on. This process is independent of the particular intersection at
which the cart has arrived - that is, the cart has no per-intersection
memory.

Carts all move at the same speed; they take turns moving a single step
at a time. They do this based on their current location: carts on the
top row move first (acting from left to right), then carts on the
second row move (again from left to right), then carts on the third
row, and so on. Once each cart has moved one step, the process
repeats; each of these loops is called a tick.

For example, suppose there are two carts on a straight track:

|  |  |  |  |
v  |  |  |  |
|  v  v  |  |
|  |  |  v  X
|  |  ^  ^  |
^  ^  |  |  |
|  |  |  |  |

First, the top cart moves. It is facing down (v), so it moves down one
square. Second, the bottom cart moves. It is facing up (^), so it
moves up one square. Because all carts have moved, the first tick
ends. Then, the process repeats, starting with the first cart. The
first cart moves down, then the second cart moves up - right into the
first cart, colliding with it! (The location of the crash is marked
with an X.) This ends the second and last tick.

Here is a longer example:

/->-\
|   |  /----\
| /-+--+-\  |
| | |  | v  |
\-+-/  \-+--/
  \------/

/-->\
|   |  /----\
| /-+--+-\  |
| | |  | |  |
\-+-/  \->--/
  \------/

/---v
|   |  /----\
| /-+--+-\  |
| | |  | |  |
\-+-/  \-+>-/
  \------/

/---\
|   v  /----\
| /-+--+-\  |
| | |  | |  |
\-+-/  \-+->/
  \------/

/---\
|   |  /----\
| /->--+-\  |
| | |  | |  |
\-+-/  \-+--^
  \------/

/---\
|   |  /----\
| /-+>-+-\  |
| | |  | |  ^
\-+-/  \-+--/
  \------/

/---\
|   |  /----\
| /-+->+-\  ^
| | |  | |  |
\-+-/  \-+--/
  \------/

/---\
|   |  /----<
| /-+-->-\  |
| | |  | |  |
\-+-/  \-+--/
  \------/

/---\
|   |  /---<\
| /-+--+>\  |
| | |  | |  |
\-+-/  \-+--/
  \------/

/---\
|   |  /--<-\
| /-+--+-v  |
| | |  | |  |
\-+-/  \-+--/
  \------/

/---\
|   |  /-<--\
| /-+--+-\  |
| | |  | v  |
\-+-/  \-+--/
  \------/

/---\
|   |  /<---\
| /-+--+-\  |
| | |  | |  |
\-+-/  \-<--/
  \------/

/---\
|   |  v----\
| /-+--+-\  |
| | |  | |  |
\-+-/  \<+--/
  \------/

/---\
|   |  /----\
| /-+--v-\  |
| | |  | |  |
\-+-/  ^-+--/
  \------/

/---\
|   |  /----\
| /-+--+-\  |
| | |  X |  |
\-+-/  \-+--/
  \------/

After following their respective paths for a while, the carts
eventually crash. To help prevent crashes, you'd like to know the
location of the first crash. Locations are given in X,Y coordinates,
where the furthest left column is X=0 and the furthest top row is Y=0:

           111
 0123456789012
0/---\
1|   |  /----\
2| /-+--+-\  |
3| | |  X |  |
4\-+-/  \-+--/
5  \------/

In this example, the location of the first crash is 7,3.

--- Part Two ---

There isn't much you can do to prevent crashes in this ridiculous
system. However, by predicting the crashes, the Elves know where to be
in advance and instantly remove the two crashing carts the moment any
crash occurs.

They can proceed like this for a while, but eventually, they're going
to run out of carts. It could be useful to figure out where the last
cart that hasn't crashed will end up.

For example:

/>-<\  
|   |  
| /<+-\
| | | v
\>+</ |
  |   ^
  \<->/

/---\  
|   |  
| v-+-\
| | | |
\-+-/ |
  |   |
  ^---^

/---\  
|   |  
| /-+-\
| v | |
\-+-/ |
  ^   ^
  \---/

/---\  
|   |  
| /-+-\
| | | |
\-+-/ ^
  |   |
  \---/

After four very expensive crashes, a tick ends with only one cart
remaining; its final location is 6,4.

What is the location of the last cart at the end of the first tick
where it is the only cart left?
'''

from aoc2018 import *

UP, DOWN, LEFT, RIGHT = (0, -1), (0, 1), (-1, 0), (1, 0)
DIRECTIONS = {'^': UP, 'v': DOWN, '<': LEFT, '>': RIGHT, 'X': 'X'}
GLYPHS = dict((v, k) for k, v in DIRECTIONS.items())
TURNS = [-1, 0, 1]
CORNERS = {'/': {UP: RIGHT, DOWN: LEFT, LEFT: DOWN, RIGHT: UP},
           '\\': {UP: LEFT, DOWN: RIGHT, LEFT: UP, RIGHT: DOWN}}


def turn(v, direction):
    if direction < 0:
        v = (Y(v), -X(v))
    elif direction > 0:
        v = (-Y(v), X(v))
    return v


def fixtrack(c):
    if c in '^v':
        return '|'
    elif c in '<>':
        return '-'
    return c


def parse(lines):
    if isinstance(lines, str):
        lines = lines.splitlines()
    track = [list(line.rstrip('\n')) for line in lines]
    # Find carts
    carts = {}
    for row, line in enumerate(track):
        for col, c in enumerate(line):
            direction = DIRECTIONS.get(c, None)
            if direction is not None:
                carts[(col, row)] = (direction, 0)
        track[row] = line = [fixtrack(c) for c in line]
        # print ('{:4} {}'.format(row, ''.join(line)))
    return track, carts


def dump(track, carts):
    for row, line in enumerate(track):
        out = []
        for col, c in enumerate(line):
            pos = (col, row)
            if pos in carts:
                direction, nextturn = carts[pos]
                out.append(GLYPHS[direction])
            else:
                out.append(c)
        print (''.join(out))


def tick(track, carts):
    result = {}
    collisions = []
    # Coordinates are X, Y but need to sort by Y, X
    for pos in sorted(carts, key=lambda pos: (Y(pos), X(pos))):
        if not pos in carts:  # Perhaps discarded from earlier collision
            continue
        direction, nextturn = carts.pop(pos)
        nextpos = (X(pos) + X(direction), Y(pos) + Y(direction))
        node = track[Y(nextpos)][X(nextpos)]
        assert node in r'|-+-\/', 'Cart %s direction %s: unexpected node "%s" found after %s' % (
            pos, direction, node, track[Y(pos)][X(pos)])
        if nextpos in carts or nextpos in result:
            collisions.append(nextpos)
            carts.pop(nextpos, None)
            result.pop(nextpos, None)
            continue
        if node in CORNERS:
            direction = CORNERS[node][direction]
        elif node == '+':
            direction = turn(direction, TURNS[nextturn % len(TURNS)])
            nextturn += 1
        result[nextpos] = (direction, nextturn)
    return result, collisions


def collide(track, carts, num_collisions=1):
    all_collisions = []
    while len(all_collisions) < num_collisions and len(carts) > 1:
        carts, collisions = tick(track, carts)
        all_collisions.extend(collisions)
    return carts, all_collisions


track, carts = parse(r'''/->-\
|   |  /----\
| /-+--+-\  |
| | |  | v  |
\-+-/  \-+--/
  \------/''')
assert collide(track, carts)[1][0] == (7, 3)

track, carts = parse(Input(13))
# Bail out on first collision
print (collide(track, dict(carts))[1][0])

# Run until only one cart left
print (collide(track, dict(carts), BIG)[0])
