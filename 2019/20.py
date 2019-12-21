#!/usr/bin/env python3
"""--- Day 20: Donut Maze ---

You notice a strange pattern on the surface of Pluto and land nearby
to get a closer look. Upon closer inspection, you realize you've come
across one of the famous space-warping mazes of the long-lost Pluto
civilization!

Because there isn't much space on Pluto, the civilization that used to
live here thrived by inventing a method for folding
spacetime. Although the technology is no longer understood, mazes like
this one provide a small glimpse into the daily life of an ancient
Pluto citizen.

This maze is shaped like a donut. Portals along the inner and outer
edge of the donut can instantly teleport you from one side to the
other. For example:

         A
         A
  #######.#########
  #######.........#
  #######.#######.#
  #######.#######.#
  #######.#######.#
  #####  B    ###.#
BC...##  C    ###.#
  ##.##       ###.#
  ##...DE  F  ###.#
  #####    G  ###.#
  #########.#####.#
DE..#######...###.#
  #.#########.###.#
FG..#########.....#
  ###########.#####
             Z
             Z

This map of the maze shows solid walls (#) and open passages
(.). Every maze on Pluto has a start (the open tile next to AA) and an
end (the open tile next to ZZ). Mazes on Pluto also have portals; this
maze has three pairs of portals: BC, DE, and FG. When on an open tile
next to one of these labels, a single step can take you to the other
tile with the same label. (You can only walk on . tiles; labels and
empty space are not traversable.)

One path through the maze doesn't require any portals. Starting at AA,
you could go down 1, right 8, down 12, left 4, and down 1 to reach ZZ,
a total of 26 steps.

However, there is a shorter path: You could walk from AA to the inner
BC portal (4 steps), warp to the outer BC portal (1 step), walk to the
inner DE (6 steps), warp to the outer DE (1 step), walk to the outer
FG (4 steps), warp to the inner FG (1 step), and finally walk to ZZ (6
steps). In total, this is only 23 steps.

Here is a larger example:

                   A
                   A
  #################.#############
  #.#...#...................#.#.#
  #.#.#.###.###.###.#########.#.#
  #.#.#.......#...#.....#.#.#...#
  #.#########.###.#####.#.#.###.#
  #.............#.#.....#.......#
  ###.###########.###.#####.#.#.#
  #.....#        A   C    #.#.#.#
  #######        S   P    #####.#
  #.#...#                 #......VT
  #.#.#.#                 #.#####
  #...#.#               YN....#.#
  #.###.#                 #####.#
DI....#.#                 #.....#
  #####.#                 #.###.#
ZZ......#               QG....#..AS
  ###.###                 #######
JO..#.#.#                 #.....#
  #.#.#.#                 ###.#.#
  #...#..DI             BU....#..LF
  #####.#                 #.#####
YN......#               VT..#....QG
  #.###.#                 #.###.#
  #.#...#                 #.....#
  ###.###    J L     J    #.#.###
  #.....#    O F     P    #.#...#
  #.###.#####.#.#####.#####.###.#
  #...#.#.#...#.....#.....#.#...#
  #.#####.###.###.#.#.#########.#
  #...#.#.....#...#.#.#.#.....#.#
  #.###.#####.###.###.#.#.#######
  #.#.........#...#.............#
  #########.###.###.#############
           B   J   C
           U   P   P

Here, AA has no direct path to ZZ, but it does connect to AS and
CP. By passing through AS, QG, BU, and JO, you can reach ZZ in 58
steps.

In your maze, how many steps does it take to get from the open tile
marked AA to the open tile marked ZZ?

--- Part Two ---

Strangely, the exit isn't open when you reach it. Then, you remember:
the ancient Plutonians were famous for building recursive spaces.

The marked connections in the maze aren't portals: they physically
connect to a larger or smaller copy of the maze. Specifically, the
labeled tiles around the inside edge actually connect to a smaller
copy of the same maze, and the smaller copy's inner labeled tiles
connect to yet a smaller copy, and so on.

When you enter the maze, you are at the outermost level; when at the
outermost level, only the outer labels AA and ZZ function (as the
start and end, respectively); all other outer labeled tiles are
effectively walls. At any other level, AA and ZZ count as walls, but
the other outer labeled tiles bring you one level outward.

Your goal is to find a path through the maze that brings you back to
ZZ at the outermost level of the maze.

In the first example above, the shortest path is now the loop around
the right side. If the starting level is 0, then taking the
previously-shortest path would pass through BC (to level 1), DE (to
level 2), and FG (back to level 1). Because this is not the outermost
level, ZZ is a wall, and the only option is to go back around to BC,
which would only send you even deeper into the recursive maze.

In the second example above, there is no path that brings you to ZZ at
the outermost level.

Here is a more interesting example:

             Z L X W       C
             Z P Q B       K
  ###########.#.#.#.#######.###############
  #...#.......#.#.......#.#.......#.#.#...#
  ###.#.#.#.#.#.#.#.###.#.#.#######.#.#.###
  #.#...#.#.#...#.#.#...#...#...#.#.......#
  #.###.#######.###.###.#.###.###.#.#######
  #...#.......#.#...#...#.............#...#
  #.#########.#######.#.#######.#######.###
  #...#.#    F       R I       Z    #.#.#.#
  #.###.#    D       E C       H    #.#.#.#
  #.#...#                           #...#.#
  #.###.#                           #.###.#
  #.#....OA                       WB..#.#..ZH
  #.###.#                           #.#.#.#
CJ......#                           #.....#
  #######                           #######
  #.#....CK                         #......IC
  #.###.#                           #.###.#
  #.....#                           #...#.#
  ###.###                           #.#.#.#
XF....#.#                         RF..#.#.#
  #####.#                           #######
  #......CJ                       NM..#...#
  ###.#.#                           #.###.#
RE....#.#                           #......RF
  ###.###        X   X       L      #.#.#.#
  #.....#        F   Q       P      #.#.#.#
  ###.###########.###.#######.#########.###
  #.....#...#.....#.......#...#.....#.#...#
  #####.#.###.#######.#######.###.###.#.#.#
  #.......#.......#.#.#.#.#...#...#...#.#.#
  #####.###.#####.#.#.#.#.###.###.#.###.###
  #.......#.....#.#...#...............#...#
  #############.#.#.###.###################
               A O F   N
               A A D   M

One shortest path through the maze is the following:

Walk from AA to XF (16 steps)
Recurse into level 1 through XF (1 step)
Walk from XF to CK (10 steps)
Recurse into level 2 through CK (1 step)
Walk from CK to ZH (14 steps)
Recurse into level 3 through ZH (1 step)
Walk from ZH to WB (10 steps)
Recurse into level 4 through WB (1 step)
Walk from WB to IC (10 steps)
Recurse into level 5 through IC (1 step)
Walk from IC to RF (10 steps)
Recurse into level 6 through RF (1 step)
Walk from RF to NM (8 steps)
Recurse into level 7 through NM (1 step)
Walk from NM to LP (12 steps)
Recurse into level 8 through LP (1 step)
Walk from LP to FD (24 steps)
Recurse into level 9 through FD (1 step)
Walk from FD to XQ (8 steps)
Recurse into level 10 through XQ (1 step)
Walk from XQ to WB (4 steps)
Return to level 9 through WB (1 step)
Walk from WB to ZH (10 steps)
Return to level 8 through ZH (1 step)
Walk from ZH to CK (14 steps)
Return to level 7 through CK (1 step)
Walk from CK to XF (10 steps)
Return to level 6 through XF (1 step)
Walk from XF to OA (14 steps)
Return to level 5 through OA (1 step)
Walk from OA to CJ (8 steps)
Return to level 4 through CJ (1 step)
Walk from CJ to RE (8 steps)
Return to level 3 through RE (1 step)
Walk from RE to IC (4 steps)
Recurse into level 4 through IC (1 step)
Walk from IC to RF (10 steps)
Recurse into level 5 through RF (1 step)
Walk from RF to NM (8 steps)
Recurse into level 6 through NM (1 step)
Walk from NM to LP (12 steps)
Recurse into level 7 through LP (1 step)
Walk from LP to FD (24 steps)
Recurse into level 8 through FD (1 step)
Walk from FD to XQ (8 steps)
Recurse into level 9 through XQ (1 step)
Walk from XQ to WB (4 steps)
Return to level 8 through WB (1 step)
Walk from WB to ZH (10 steps)
Return to level 7 through ZH (1 step)
Walk from ZH to CK (14 steps)
Return to level 6 through CK (1 step)
Walk from CK to XF (10 steps)
Return to level 5 through XF (1 step)
Walk from XF to OA (14 steps)
Return to level 4 through OA (1 step)
Walk from OA to CJ (8 steps)
Return to level 3 through CJ (1 step)
Walk from CJ to RE (8 steps)
Return to level 2 through RE (1 step)
Walk from RE to XQ (14 steps)
Return to level 1 through XQ (1 step)
Walk from XQ to FD (8 steps)
Return to level 0 through FD (1 step)
Walk from FD to ZZ (18 steps)

This path takes a total of 396 steps to move from AA at the outermost
layer to ZZ at the outermost layer.

In your maze, when accounting for recursion, how many steps does it
take to get from the open tile marked AA to the open tile marked ZZ,
both at the outermost layer?

"""

from aoc import *
import sys
import string
from collections import defaultdict


sys.setrecursionlimit(10 ** 6)


def open_square(maze, pos):
    for p in neighbors4(pos):
        if maze.get(p) == ".":
            return p


def parse(lines, debug=False):
    maze = {}
    doors = defaultdict(list)
    half_doors = {}
    for y, line in enumerate(l for l in lines if l.strip()):
        for x, c in enumerate(line):
            if c in "#.":
                maze[(x, y)] = c
                continue
            if not c.strip():
                continue
            assert c in string.ascii_uppercase
            if x - 1 in half_doors:
                door = half_doors.pop(x - 1) + c
                coord, dtype = (x, y), "DOOR>"
                if maze.get((x - 2, y)) == ".":
                    coord, dtype = (x - 1, y), "<DOOR"
                if debug:
                    print(dtype, coord, door)
                maze[coord] = door
                doors[door].append(coord)
            elif x in half_doors:
                door = half_doors.pop(x) + c
                coord, dtype = (x, y), "vDOOR"
                if maze.get((x, y - 2)) == ".":
                    coord, dtype = (x, y - 1), "^DOOR"
                if debug:
                    print(dtype, coord, door)
                maze[coord] = door
                doors[door].append(coord)
            else:
                half_doors[x] = c
    assert not half_doors, half_doors
    return maze


def render(maze, path):
    ul, lr = origin, (max(X(k) for k in maze), max(Y(k) for k in maze))

    def glyph(pos):
        for p, level in path:
            if pos == p:
                return str(level)[0]
        return maze.get(pos, " ")[0]

    print("MAZE", lr, len(path))
    for y in range(0, Y(lr) + 1):
        print("".join(glyph((x, y)) for x in range(0, X(lr) + 1)))


def get_warps(maze, level=-1, debug=False):
    squares = [k for k, v in maze.items() if v in ".#"]
    assert squares
    xdims = (min(x for x, y in squares), max(x for x, y in squares))
    ydims = (min(y for x, y in squares), max(y for x, y in squares))
    doors = [(p, v) for p, v in maze.items() if v not in ".#"]
    pairs = defaultdict(list)
    for pos, door in doors:
        pairs[door].append(pos)

    def is_inside(p):
        return (
            X(p) > xdims[0] and X(p) < xdims[1] and Y(p) > ydims[0] and Y(p) < ydims[1]
        )

    warps = {}
    if level < 0:
        for door, positions in pairs.items():
            if len(positions) == 1:
                continue
            warps[positions[0]] = (open_square(maze, positions[1]), 0)
            warps[positions[1]] = (open_square(maze, positions[0]), 0)
        return warps

    for door, positions in pairs.items():
        if len(positions) == 1:
            continue
        p1, p2 = positions
        if not is_inside(p1):
            p1, p2 = p2, p1
        # p1 is the inside door
        warps[p1] = (open_square(maze, p2), 1)
        if debug:
            print("WARP-INSIDE", p1, warps[p1])
        # Outside door not a warp at topmost level
        if level > 0:
            warps[p2] = (open_square(maze, p1), -1)
            if debug:
                print("WARP-OUTSIDE", p2, warps[p2])

    if level == 0:
        assert all(is_inside(pos) for pos in warps.keys())

    return warps


def solve(maze, level=-1, debug=False):
    start = open_square(maze, next(p for p, d in maze.items() if d == "AA"))
    goal = open_square(maze, next(p for p, d in maze.items() if d == "ZZ"))
    if debug:
        print("SOLVE", start, goal, level)
    level_warps = [get_warps(maze, level, debug), get_warps(maze, level + 1, debug)]

    def moves(state):
        pos, level = state
        warps = level_warps[0 if level <= 0 else 1]
        for n in neighbors4(pos):
            if n in warps:
                if debug:
                    print("WARP", pos, maze[n], warps[n])
                yield (warps[n][0], level + warps[n][1])
            if maze.get(n, "#") == ".":
                yield (n, level)

    best = bfs((start, 0), moves, ((goal, 0),))
    if debug:
        assert best is not None
        print("BEST", len(best))
        render(maze, best)
    return len(best) - 1 if best is not None else 10 ** 10


EX1 = """
         A
         A
  #######.#########
  #######.........#
  #######.#######.#
  #######.#######.#
  #######.#######.#
  #####  B    ###.#
BC...##  C    ###.#
  ##.##       ###.#
  ##...DE  F  ###.#
  #####    G  ###.#
  #########.#####.#
DE..#######...###.#
  #.#########.###.#
FG..#########.....#
  ###########.#####
             Z
             Z
"""
assert solve(parse(EX1.splitlines())) == 23

EX2 = """
                   A
                   A
  #################.#############
  #.#...#...................#.#.#
  #.#.#.###.###.###.#########.#.#
  #.#.#.......#...#.....#.#.#...#
  #.#########.###.#####.#.#.###.#
  #.............#.#.....#.......#
  ###.###########.###.#####.#.#.#
  #.....#        A   C    #.#.#.#
  #######        S   P    #####.#
  #.#...#                 #......VT
  #.#.#.#                 #.#####
  #...#.#               YN....#.#
  #.###.#                 #####.#
DI....#.#                 #.....#
  #####.#                 #.###.#
ZZ......#               QG....#..AS
  ###.###                 #######
JO..#.#.#                 #.....#
  #.#.#.#                 ###.#.#
  #...#..DI             BU....#..LF
  #####.#                 #.#####
YN......#               VT..#....QG
  #.###.#                 #.###.#
  #.#...#                 #.....#
  ###.###    J L     J    #.#.###
  #.....#    O F     P    #.#...#
  #.###.#####.#.#####.#####.###.#
  #...#.#.#...#.....#.....#.#...#
  #.#####.###.###.#.#.#########.#
  #...#.#.....#...#.#.#.#.....#.#
  #.###.#####.###.###.#.#.#######
  #.#.........#...#.............#
  #########.###.###.#############
           B   J   C
           U   P   P
"""
assert solve(parse(EX2.splitlines())) == 58

EX3 = """
             Z L X W       C
             Z P Q B       K
  ###########.#.#.#.#######.###############
  #...#.......#.#.......#.#.......#.#.#...#
  ###.#.#.#.#.#.#.#.###.#.#.#######.#.#.###
  #.#...#.#.#...#.#.#...#...#...#.#.......#
  #.###.#######.###.###.#.###.###.#.#######
  #...#.......#.#...#...#.............#...#
  #.#########.#######.#.#######.#######.###
  #...#.#    F       R I       Z    #.#.#.#
  #.###.#    D       E C       H    #.#.#.#
  #.#...#                           #...#.#
  #.###.#                           #.###.#
  #.#....OA                       WB..#.#..ZH
  #.###.#                           #.#.#.#
CJ......#                           #.....#
  #######                           #######
  #.#....CK                         #......IC
  #.###.#                           #.###.#
  #.....#                           #...#.#
  ###.###                           #.#.#.#
XF....#.#                         RF..#.#.#
  #####.#                           #######
  #......CJ                       NM..#...#
  ###.#.#                           #.###.#
RE....#.#                           #......RF
  ###.###        X   X       L      #.#.#.#
  #.....#        F   Q       P      #.#.#.#
  ###.###########.###.#######.#########.###
  #.....#...#.....#.......#...#.....#.#...#
  #####.#.###.#######.#######.###.###.#.#.#
  #.......#.......#.#.#.#.#...#...#...#.#.#
  #####.###.#####.#.#.#.#.###.###.#.###.###
  #.......#.....#.#...#...............#...#
  #############.#.#.###.###################
               A O F   N
               A A D   M
"""
assert solve(parse(EX3.splitlines()), level=0, debug=True) == 396


if __name__ == "__main__":
    maze = parse(Input(20).read().splitlines())
    print(door for k, door in maze.items() if door not in ".#")
    print(solve(maze))
    print(solve(maze, level=0))
