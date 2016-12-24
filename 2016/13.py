#!/usr/bin/python
'''--- Day 13: A Maze of Twisty Little Cubicles ---

You arrive at the first floor of this new building to discover a much
less welcoming environment than the shiny atrium of the last
one. Instead, you are in a maze of twisty little cubicles, all alike.

Every location in this area is addressed by a pair of non-negative
integers (x,y). Each such coordinate is either a wall or an open
space. You can't move diagonally. The cube maze starts at 0,0 and
seems to extend infinitely toward positive x and y; negative values
are invalid, as they represent a location outside the building. You
are in a small waiting area at 1,1.

While it seems chaotic, a nearby morale-boosting poster explains, the
layout is actually quite logical. You can determine whether a given
x,y coordinate will be a wall or an open space using a simple system:

Find x*x + 3*x + 2*x*y + y + y*y.
Add the office designer's favorite number (your puzzle input).
Find the binary representation of that sum; count the number of bits that are 1.
If the number of bits that are 1 is even, it's an open space.
If the number of bits that are 1 is odd, it's a wall.

For example, if the office designer's favorite number were 10, drawing
walls as # and open spaces as ., the corner of the building containing
0,0 would look like this:

  0123456789
0 .#.####.##
1 ..#..#...#
2 #....##...
3 ###.#.###.
4 .##..#..#.
5 ..##....#.
6 #...##.###

Now, suppose you wanted to reach 7,4. The shortest route you could
take is marked as O:

  0123456789
0 .#.####.##
1 .O#..#...#
2 #OOO.##...
3 ###O#.###.
4 .##OO#OO#.
5 ..##OOO.#.
6 #...##.###

Thus, reaching 7,4 would take a minimum of 11 steps (starting from
your current location, 1,1).

What is the fewest number of steps required for you to reach 31,39?

Your puzzle input is 1352.'''

MAGIC = 1352
START = (1, 1)
GOAL = (31, 39)

def is_open (pos):
    x, y = pos
    n = x*x + 3*x + 2*x*y + y + y*y + MAGIC
    ones = bin (n).count ("1")
    return ones % 2 == 0

assert is_open (START), "Start is not open"
assert is_open (GOAL), "Goal is not open"

def dfs_paths(start, goal):
    stack = [(start, [start])]
    best = 99999999
    while stack:
        (vertex, path) = stack.pop()
        x, y = vertex
        up, down, left, right = [None] * 4
        if y > 0:
            up = (x, y-1)
        down = (x, y+1)
        if x > 0:
            left = (x-1, y)
        right = (x+1, y)
        # print vertex, path, [up, down, left, right]
        for next in set ([up, down, left, right]) - set(path):
            if next is None or not is_open (next):
                continue
            if next == goal:
                if len (path) < best:
                    yield path + [next]
                    best = len (path)
            else:
                # print len (path), vertex, next, path + [next]
                if len (path) < best:
                    stack.append((next, path + [next]))

def all_steps(start, maxlen):
    stack = [(start, [start])]
    seen = set ([start])
    while stack:
        (vertex, path) = stack.pop()
        x, y = vertex
        up, down, left, right = [None] * 4
        if y > 0:
            up = (x, y-1)
        down = (x, y+1)
        if x > 0:
            left = (x-1, y)
        right = (x+1, y)
        for next in set ([up, down, left, right]) - set (path):
            if next is None or not is_open (next):
                continue
            if len (path) <= maxlen:
                seen.add (next)
                stack.append ((next, path + [next]))
    return seen

for path in dfs_paths (START, GOAL):
    print len (path) - 1, path

print len (all_steps (START, 50))
