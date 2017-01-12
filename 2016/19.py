#!/usr/bin/python

'''--- Day 19: An Elephant Named Joseph ---

The Elves contact you over a highly secure emergency channel. Back at
the North Pole, the Elves are busy misunderstanding White Elephant
parties.

Each Elf brings a present. They all sit in a circle, numbered starting
with position 1. Then, starting with the first Elf, they take turns
stealing all the presents from the Elf to their left. An Elf with no
presents is removed from the circle and does not take turns.

For example, with five Elves (numbered 1 to 5):

  1
5   2
 4 3

- Elf 1 takes Elf 2's present.
- Elf 2 has no presents and is skipped.
- Elf 3 takes Elf 4's present.
- Elf 4 has no presents and is also skipped.
- Elf 5 takes Elf 1's two presents.
- Neither Elf 1 nor Elf 2 have any presents, so both are skipped.
- Elf 3 takes Elf 5's three presents.

So, with five Elves, the Elf that sits starting in position 3 gets all
the presents.

With the number of Elves given in your puzzle input, which Elf gets
all the presents?

Your puzzle input is 3001330.

Four elves:
1 2 3 4
1 x 3 x
1 x x x

Five
1 2 3 4 5
1 x 3 x 5
Seven
1 2 3 4 5 6 7
1 x 3 x 5 x 7
1 x x
'''

from math import log

# Josephus problem
def part1(val):
    l = val - (1 << int(log(val,2)))
    return 2 * l + 1

def part2(n):
    p = 3**int(log(n-1,3))
    return n-p+max(n-2*p,0)

assert part1(5) == 3

print part1(3001330)
print part2(3001330)
