#!/usr/bin/env python3
'''--- Day 19: A Series of Tubes ---

Somehow, a network packet got lost and ended up here. It's trying to
follow a routing diagram (your puzzle input), but it's confused about
where to go.

Its starting point is just off the top of the diagram. Lines (drawn
with |, -, and +) show the path it needs to take, starting by going
down onto the only line connected to the top of the diagram. It needs
to follow this path until it reaches the end (located somewhere within
the diagram) and stop there.

Sometimes, the lines cross over each other; in these cases, it needs
to continue going the same direction, and only turn left or right when
there's no other option. In addition, someone has left letters on the
line; these also don't change its direction, but it can use them to
keep track of where it's been. For example:

     |
     |  +--+
     A  |  C
 F---|----E|--+
     |  |  |  D
     +B-+  +--+

Given this diagram, the packet needs to take the following path:

Starting at the only line touching the top of the diagram, it must go
down, pass through A, and continue onward to the first +.

Travel right, up, and right, passing through B in the process.

Continue down (collecting C), right, and up (collecting D).

Finally, go all the way left through E and stopping at F.

Following the path to the end, the letters it sees on its path are
ABCDEF.

The little packet looks up at you, hoping you can help it find the
way. What letters will it see (in the order it would see them) if it
follows the path? (The routing diagram is very wide; make sure you
view it without line wrapping.)
Your puzzle answer was RYLONKEWB.

The first half of this puzzle is complete! It provides one gold star: *

--- Part Two ---

The packet is curious how many steps it needs to go.

For example, using the same routing diagram from the example above...

     |
     |  +--+
     A  |  C
 F---|--|-E---+
     |  |  |  D
     +B-+  +--+

...the packet would go:

6 steps down (including the first line at the top of the diagram).
3 steps right.
4 steps up.
3 steps right.
4 steps down.
3 steps right.
2 steps up.
13 steps left (including the F it stops on).

This would result in a total of 38 steps.

How many steps does the packet need to go?

Although it hasn't changed, you can still get your puzzle input.
'''

from aoc2017 import *
import string


def solve(maze):
    x, y, dir = maze[-1].index('|'), 0, DOWN
    seen = []  # set()
    letters = []
    while y + dir[1] < len(maze) and x + dir[0] < len(maze[y]):
        seen.append((x, y))
        x, y = x + dir[0], y + dir[1]
        c = maze[y][x]
        # print (x, y, dir, c, len(seen), (x, y) in seen)
        if c == '+':
            # Crossroads
            if dir in (UP, DOWN):
                # Check left/right
                candidates = (LEFT, RIGHT)
            else:
                candidates = (UP, DOWN)
            for dnew in candidates:
                dx, dy = dnew
                x2, y2 = x + dx, y + dy
                if (x2, y2) and y2 < len(maze) and x2 < len(maze[y + dy]) and maze[y2][x2] != ' ':
                    dir = dnew
                    break
            else:
                assert False, 'Cannot find way out of crossroads at {}'.format(
                    x, y)
        elif c in string.ascii_letters:
            # Collect a letter, keep going
            letters.append(c)
        elif c in ('|', '-'):
            # Keep going
            pass
        else:
            break
            assert False, 'Unknown glyph when traveling {}: {}'.format(dir, c)
    return join(letters), len(seen) - 1


Maze = tuple(reversed([tuple([c for c in line.rstrip('\n')])
                       for line in Input(19)]))
print (solve(Maze))
