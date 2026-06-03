#!/usr/bin/env python3
'''--- Day 16: Permutation Promenade ---

You come upon a very unusual sight; a group of programs here appear to
be dancing.

There are sixteen programs in total, named a through p. They start by
standing in a line: a stands in position 0, b stands in position 1,
and so on until p, which stands in position 15.

The programs' dance consists of a sequence of dance moves:

Spin, written sX, makes X programs move from the end to the front, but
maintain their order otherwise. (For example, s3 on abcde produces
cdeab).
Exchange, written xA/B, makes the programs at positions A and B swap
places.
Partner, written pA/B, makes the programs named A and B swap places.

For example, with only five programs standing in a line (abcde), they
could do the following dance:

s1, a spin of size 1: eabcd.
x3/4, swapping the last two programs: eabdc.
pe/b, swapping programs e and b: baedc.
After finishing their dance, the programs end up in order baedc.

You watch the dance for a while and record their dance moves (your
puzzle input). In what order are the programs standing after their
dance?

Your puzzle answer was padheomkgjfnblic.

The first half of this puzzle is complete! It provides one gold star: *

--- Part Two ---

Now that you're starting to get a feel for the dance moves, you turn
your attention to the dance as a whole.

Keeping the positions they ended up in from their previous dance, the
programs perform it again and again: including the first dance, a
total of one billion (1000000000) times.

In the example above, their second dance would begin with the order
baedc, and use the same dance moves:

s1, a spin of size 1: cbaed.
x3/4, swapping the last two programs: cbade.
pe/b, swapping programs e and b: ceadb.

In what order are the programs standing after their billion dances?
'''

from aoc2017 import *


def dance(x, steps):
    # x = [chr(c) for c for c in range(ord('a'), ord('q'))]
    if type(x) == str:
        x = list(x)
    for s, arg in [(s[0], s[1:]) for s in steps]:
        if s == 's':
            arg = int(arg) % len(x)
            x = x[-arg:] + x[:-arg]
        elif s == 'x':
            p1, p2 = map(int, arg.split('/'))
            x[p1], x[p2] = x[p2], x[p1]
            pass
        else:
            p1, p2 = map(lambda c: x.index(c), arg.split('/'))
            x[p1], x[p2] = x[p2], x[p1]
            pass
    return x


assert dance('abcde', ['s1', 'x3/4', 'pe/b']) == list('baedc')

steps = vector(Input(16).read())
line = 'abcdefghijklmnop'
first = None
stopat = None

for i in range(10**9):
    line = dance(line, steps)
    if i == 0:
        first = line[:]
        print(join(line))
    elif line == first:
        # If we repeat every N cycles, stop as soon as we hit
        # (10**9 % N) - 1
        remainder = 10**9 % i
        stopat = i + remainder - 1
    elif i == stopat:
        break
print(join(line))
