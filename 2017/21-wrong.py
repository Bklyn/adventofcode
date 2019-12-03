#!/usr/bin/env python3
'''--- Day 21: Fractal Art ---

You find a program trying to generate some art. It uses a strange
process that involves repeatedly enhancing the detail of an image
through a set of rules.

The image consists of a two-dimensional square grid of pixels that are
either on (#) or off (.). The program always begins with this pattern:

.#.
..#
###

Because the pattern is both 3 pixels wide and 3 pixels tall, it is
said to have a size of 3.

Then, the program repeats the following process:

If the size is evenly divisible by 2, break the pixels up into 2x2
squares, and convert each 2x2 square into a 3x3 square by following
the corresponding enhancement rule.

Otherwise, the size is evenly divisible by 3; break the pixels up into
3x3 squares, and convert each 3x3 square into a 4x4 square by
following the corresponding enhancement rule.

Because each square of pixels is replaced by a larger one, the image
gains pixels and so its size increases.

The artist's book of enhancement rules is nearby (your puzzle input);
however, it seems to be missing rules. The artist explains that
sometimes, one must rotate or flip the input pattern to find a
match. (Never rotate or flip the output pattern, though.) Each pattern
is written concisely: rows are listed as single units, ordered
top-down, and separated by slashes. For example, the following rules
correspond to the adjacent patterns:

../.#  =  ..
          .#

                .#.
.#./..#/###  =  ..#
                ###

                        #..#
#..#/..../#..#/.##.  =  ....
                        #..#
                        .##.

When searching for a rule to use, rotate and flip the pattern as
necessary. For example, all of the following patterns match the same
rule:

.#.   .#.   #..   ###
..#   #..   #.#   ..#
###   ###   ##.   .#.

Suppose the book contained the following two rules:

../.# => ##./#../...

.#./..#/### => #..#/..../..../#..#

As before, the program begins with this pattern:

.#.
..#
###

The size of the grid (3) is not divisible by 2, but it is divisible by
3. It divides evenly into a single square; the square matches the
second rule, which produces:

#..#
....
....
#..#

The size of this enhanced grid (4) is evenly divisible by 2, so that
rule is used. It divides evenly into four squares:

#.|.#
..|..
--+--
..|..
#.|.#

Each of these squares matches the same rule (../.# => ##./#../...),
three of which require some flipping and rotation to line up with the
rule. The output for the rule is the same in all four cases:

##.|##.
#..|#..
...|...
---+---
##.|##.
#..|#..
...|...

Finally, the squares are joined into a new grid:

##.##.
#..#..
......
##.##.
#..#..
......

Thus, after 2 iterations, the grid contains 12 pixels that are on.

How many pixels stay on after 5 iterations?
'''

from aoc2017 import *

def mstr(m, sep='/'):
    return sep.join([''.join (map (lambda x: '#' if x else '.', l)) for l in m])

def forms(m):
    seen = set()
    for i in range(4):
        tpl = tuple(m.flatten())
        if not tpl in seen:
            yield m
        seen.add (tpl)
        m = np.rot90(m)
    m = np.flip(m, axis=1)
    for i in range(4):
        tpl = tuple(m.flatten())
        if not tpl in seen:
            yield m
        seen.add (tpl)
        m = np.rot90(m)

def toarray(s):
    return np.array (
        [['.#'.index(c) for c in line]
         for line in s.split ('/')], dtype=np.bool_)

def parse_rules(inp):
    rules = {}
    num_rules = 0
    for line in inp:
        num_rules += 1
        i, ostr = line.strip().split (' => ')
        a, o = toarray(i), toarray(ostr)
        print ('RULE', num_rules, i, a.shape, set_bits(a), '=>', ostr, o.shape, set_bits(o))
        idx = 0
        for m in forms(a):
            assert set_bits(m) == set_bits(a)
            tpl = tuple(m.flatten())
            idx += 1
            print ('\tRULE', num_rules, idx, mstr(m))
            rules[tpl] = (o, num_rules)
    return rules

Start = toarray('.#./..#/###')

def evolve(rules, a):
    key = tuple(a.flatten())
    out, idx = rules[key]
    print ('EVOLVE', (mstr(a), set_bits(a)), '=>', (idx, mstr(out), set_bits (out)))
    return out

def generate_art(rules, rounds):
    Art = Start.copy()
    print (mstr (Art, sep='\n'))
    for cycle in range(rounds):
        dim = Art.shape[0]
        if dim % 3 == 0:
            # Three Dee
            stride = 3
        else:
            assert dim % 2 == 0
            stride = 2
        rows = []
        for y in range(0, dim, stride):
            row = [evolve (Rules, Art[y:y+stride,x:x+stride])
                   for x in range (0, dim, stride)]
            rows.append (np.concatenate (row, axis=1))
        Art = np.concatenate (rows, axis=0)
        print ('ROUND', cycle + 1, Art.shape, '\n\t' + mstr (Art, sep='\n\t'))
        pass
    return Art

def set_bits(art):
    return art.flatten().tolist().count (True)

Rules = parse_rules (['../.# => ##./#../...',
                      '.#./..#/### => #..#/..../..../#..#'])

assert set_bits (generate_art (Rules, 2)) == 12

Rules = parse_rules(Input(21))

print (set_bits (generate_art (Rules, 5)))
