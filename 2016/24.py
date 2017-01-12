#!/usr/bin/python
'''--- Day 24: Air Duct Spelunking ---

You've finally met your match; the doors that provide access to the
roof are locked tight, and all of the controls and related electronics
are inaccessible. You simply can't reach them.

The robot that cleans the air ducts, however, can.

It's not a very fast little robot, but you reconfigure it to be able
to interface with some of the exposed wires that have been routed
through the HVAC system. If you can direct it to each of those
locations, you should be able to bypass the security controls.

You extract the duct layout for this area from some blueprints you
acquired and create a map with the relevant locations marked (your
puzzle input). 0 is your current location, from which the cleaning
robot embarks; the other numbers are (in no particular order) the
locations the robot needs to visit at least once each. Walls are
marked as #, and open passages are marked as .. Numbers behave like
open passages.

For example, suppose you have a map like the following:

###########
#0.1.....2#
#.#######.#
#4.......3#
###########

To reach all of the points of interest as quickly as possible, you
would have the robot take the following path:

0 to 4 (2 steps)
4 to 1 (4 steps; it can't move diagonally)
1 to 2 (6 steps)
2 to 3 (2 steps)

Since the robot isn't very fast, you need to find it the shortest
route. This path is the fewest steps (in the above example, a total of
14) required to start at 0 and then visit every other location at
least once.

Given your actual map, and starting from location 0, what is the
fewest number of steps required to visit every non-0 number marked on
the map at least once?
'''

import string

def readmaze(fn):
    maze = []
    locs = {}
    with open (fn) as f:
        y = 0
        for line in [line.strip() for line in f.readlines()]:
            for d in set(string.digits) - set(locs.keys()):
                x = line.find (d)
                if x >= 0:
                    locs[d] = (x, y)
            maze.append (line)
            y = y + 1
    return maze, locs

def metric (move, pois):
    result = 0
    x, y = move
    for px, py in pois:
        result += abs (x - px) + abs (y - py)
        x, y = px, py
    return result

def get_moves (loc, maze, pois):
    x, y = loc
    moves = []
    if x > 0 and maze[y][x-1] != '#':
        moves.append ((x-1, y))
    if x < len (maze[y]) and maze[y][x+1] != '#':
        moves.append ((x+1, y))
    if y > 0 and maze[y-1][x] != '#':
        moves.append ((x, y-1))
    if y < len (maze) and maze[y+1][x] != '#':
        moves.append ((x, y+1))
    return moves

def solve (maze, locs):
    start = locs.pop ('0')
    pois = set (locs.values())
    stack = [(start, pois, [start])]
    best = None
    while stack:
        (x, y), pois, path = stack.pop()
        moves = get_moves ((x, y), maze, pois)
        if not moves:
            print 'Dead-end:', path, len(stack)
        for move in sorted (set (moves) - set (path), key=lambda x: metric(x, pois)):
            if move in pois:
                pois.remove (move)
                print len(pois), move, len(path), len(stack)
            if not len (pois):
                if best is None or len (path) + 1 < len (best):
                    best = path + [move]
                    print 'Candidate:', len (best), best
            else:
                stack.append ((move, set(pois), path + [move]))
    return best

maze, locs = readmaze ('24.txt')
print 'Locations:', locs
best = solve (maze, locs)
print 'Solution:', len(best), best
