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
from heapq import heappop, heappush

# Utilities as per Norvig below:

# 2-D points implemented using (x, y) tuples
def X(point): return point[0]
def Y(point): return point[1]

def neighbors4(point):
    "The four neighbors (without diagonals)."
    x, y = point
    return ((x+1, y), (x-1, y), (x, y+1), (x, y-1))

def cityblock_distance(p, q=(0, 0)):
    "City block distance between two points."
    return abs(X(p) - X(q)) + abs(Y(p) - Y(q))

def astar_search(start, h_func, moves_func):
    "Find a shortest sequence of states from start to a goal state (a state s with h_func(s) == 0)."
    frontier  = [(h_func(start), start)] # A priority queue, ordered by path length, f = g + h
    previous  = {start: None}  # start state has no previous state; other states will
    path_cost = {start: 0}     # The cost of the best path to a state.
    while frontier:
        (f, s) = heappop(frontier)
        if h_func(s) == 0:
            return Path(previous, s)
        for s2 in moves_func(s):
            new_cost = path_cost[s] + 1
            if s2 not in path_cost or new_cost < path_cost[s2]:
                heappush(frontier, (new_cost + h_func(s2), s2))
                path_cost[s2] = new_cost
                previous[s2] = s
    return dict(fail=True, front=len(frontier), prev=len(previous))

def Path(previous, s):
    "Return a list of states that lead to state s, according to the previous dict."
    return ([] if (s is None) else Path(previous, previous[s]) + [s])

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

maze = None
zero = None

def metric (state):
    _, visited = state
    return 8 - len (visited)

def metric2 (state):
    pos, visited = state
    return 8 - len (visited) + cityblock_distance(pos, zero)
    pass

def moves (state):
    pos, visited = state
    for x1, y1 in neighbors4(pos):
        c = maze[y1][x1]
        if c != '#':
            visited1 = (visited if c in visited or c == '.' else ''.join(sorted(visited+c)))
            yield (x1, y1), visited1

maze, locs = readmaze ('24.txt')
print 'Locations:', locs
zero = locs.pop ('0')
path = astar_search ((zero, '0'), metric, moves)
print len(path)-1
path = astar_search ((zero, '0'), metric2, moves)
print len(path)-1
