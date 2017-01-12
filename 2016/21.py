#!/usr/bin/python
'''--- Day 21: Scrambled Letters and Hash ---

The computer system you're breaking into uses a weird scrambling
function to store its passwords. It shouldn't be much trouble to
create your own scrambled password so you can add it to the system;
you just have to implement the scrambler.

The scrambling function is a series of operations (the exact list is
provided in your puzzle input). Starting with the password to be
scrambled, apply each operation in succession to the string. The
individual operations behave as follows:

- swap position X with position Y means that the letters at indexes X
  and Y (counting from 0) should be swapped.

- swap letter X with letter Y means that the letters X and Y should be
  swapped (regardless of where they appear in the string).

- rotate left/right X steps means that the whole string should be
  rotated; for example, one right rotation would turn abcd into dabc.

- rotate based on position of letter X means that the whole string
  should be rotated to the right based on the index of letter X
  (counting from 0) as determined before this instruction does any
  rotations. Once the index is determined, rotate the string to the
  right one time, plus a number of times equal to that index, plus one
  additional time if the index was at least 4.

- reverse positions X through Y means that the span of letters at
  indexes X through Y (including the letters at X and Y) should be
  reversed in order.

- move position X to position Y means that the letter which is at
  index X should be removed from the string, then inserted such that
  it ends up at index Y.

For example, suppose you start with abcde and perform the following
operations:

- swap position 4 with position 0 swaps the first and last letters,
  producing the input for the next step, ebcda.

- swap letter d with letter b swaps the positions of d and b: edcba.

- reverse positions 0 through 4 causes the entire string to be reversed, producing abcde.

- rotate left 1 step shifts all letters left one position, causing the
  first letter to wrap to the end of the string: bcdea.

- move position 1 to position 4 removes the letter at position 1 (c),
  then inserts it at position 4 (the end of the string): bdeac.

- move position 3 to position 0 removes the letter at position 3 (a),
  then inserts it at position 0 (the front of the string): abdec.

- rotate based on position of letter b finds the index of letter b
  (1), then rotates the string right once plus a number of times equal
  to that index (2): ecabd.

- rotate based on position of letter d finds the index of letter d
  (4), then rotates the string right once, plus a number of times
  equal to that index, plus an additional time because the index was
  at least 4, for a total of 6 right rotations: decab.

After these steps, the resulting scrambled password is decab.

Now, you just need to generate a new scrambled password and you can
access the system. Given the list of scrambling operations in your
puzzle input, what is the result of scrambling abcdefgh?

To begin, get your puzzle input.
'''

import re

def swap(input, x, y):
    if y < x:
        x, y = y, x
    # print 'Swap: (%d, %d) %s' % (x, y, input),
    input = input[:x] + input[y] + input[x+1:y] + input[x] + input[y+1:]
    # print input
    return input

def rotate(input, x):
    # print 'Rot: %s %d' % (input, x),
    if x < 0:
        x = len (input) + x
    x = x % len(input)
    input = input[-x:] + input[:-x]
    # print input
    return input

assert rotate('food', 3) == 'oodf'
assert rotate('food', 12) == 'food'
assert rotate('food', -1) == 'oodf'
assert rotate('food', -2) == 'odfo'
assert rotate('food', -3) == 'dfoo'
assert rotate('food', -15) == 'dfoo'

def solve(input, f, reverse=False, debug=False):
    ilen = len (input)
    prevline = None
    if reverse:
        f = reversed (f)
    for line in f:
        assert len (input) == ilen, 'Logic error parsing %s: input=%s len=%d expect=%d' % (
            prevline, input, len(input), ilen)
        if debug and prevline:
            print '>> %s -> %s' % (prevline, input)
        line = line.strip()
        prevline = line
        m = re.match ('swap position (\d+) with position (\d+)', line)
        if m:
            x, y = map (int, m.group (1, 2))
            input = swap (input, x, y)
            continue
        m = re.match ('swap letter (\w) with letter (\w)', line)
        if m:
            x, y = m.group (1, 2)
            input = swap (input, input.index (x), input.index (y))
            continue
        m = re.match ('rotate (left|right) (\d+) steps?', line)
        if m:
            lr, steps = m.group (1, 2)
            input = rotate (input, int(steps) * (-1 if lr == "left" else 1) *
                            (-1 if reverse else 1))
            continue
        m = re.match ('rotate based on position of letter (\w)', line)
        if m:
            x = input.index (m.group (1))
            if reverse:
                howfar = (7 - x / 2) if x & 1 else (3 - x / 2) + (4 if x == 0 else 0)
            else:
                howfar = 1 + x + (1 if x >= 4 else 0)
            input = rotate (input, howfar)
            continue
        m = re.match ('reverse positions (\d+) through (\d+)', line)
        if m:
            x, y = map (int, m.group (1, 2))
            input = input[:x] + input[x:y+1][::-1] + input[y+1:]
            continue
        m = re.match ('move position (\d+) to position (\d+)', line)
        if m:
            x, y = map (int, m.group (1,2))
            c = input[x]
            # print 'Move: %d -> %d: %s = [%s][%s][%s]' % (
            # x, y, input, input[:x], input[x], input[x+1:])
            input = input[:x] + input[x+1:]
            if y == 0:
                input = c + input
            else:
                input = input[:y] + c + input[y:]
            continue
        assert False, 'Unparsed input: ' + line
    return input

# import sys
#
# for x in range (8):
#     s = '_' * x + 'a' + '_' * (7 - x)
#     x = s.index ('a')
#     howfar = 1 + x + (1 if x >= 4 else 0)
#     t = rotate (s, howfar)
#     idx = t.index ('a')
#     # fixup = [-1, -2, -3, -4, 3, 2, 1, -1][x]
#     fixup = (7 - idx / 2) if idx & 1 else (3 - idx / 2) + (4 if idx == 0 else 0)
#     print s, x, howfar, t, idx, fixup, rotate (t, fixup)

# sys.exit (0)

assert solve ('abcde', [
    'swap position 4 with position 0',
    'swap letter d with letter b',
    'reverse positions 0 through 4',
    'rotate left 1 step',
    'move position 1 to position 4',
    'move position 3 to position 0',
    'rotate based on position of letter b',
    'rotate based on position of letter d']) == 'decab'

with open ('21.txt') as f:
    print solve ('abcdefgh', f)

import itertools

with open ('21.txt') as f:
    insns = f.readlines ()
    for input in itertools.permutations ('abcdefgh'):
        input = ''.join (input)
        if solve (input, insns) == 'fbgdceah':
            print input
            break
