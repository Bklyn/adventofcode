#!/usr/bin/env python
'''--- Day 12: Leonardo's Monorail ---

You finally reach the top floor of this building: a garden with a
slanted glass ceiling. Looks like there are no more stars to be had.

While sitting on a nearby bench amidst some tiger lilies, you manage
to decrypt some of the files you extracted from the servers
downstairs.

According to these documents, Easter Bunny HQ isn't just this building
- it's a collection of buildings in the nearby area. They're all
connected by a local monorail, and there's another building not far
from here! Unfortunately, being night, the monorail is currently not
operating.

You remotely connect to the monorail control systems and discover that
the boot sequence expects a password. The password-checking logic
(your puzzle input) is easy to extract, but the code it uses is
strange: it's assembunny code designed for the new computer you just
assembled. You'll have to execute the code and get the password.

The assembunny code you've extracted operates on four registers (a, b,
c, and d) that start at 0 and can hold any integer. However, it seems
to make use of only a few instructions:

* cpy x y copies x (either an integer or the value of a register) into register y.
* inc x increases the value of register x by one.
* dec x decreases the value of register x by one.
* jnz x y jumps to an instruction y away (positive means forward;
  negative means backward), but only if x is not zero.

The jnz instruction moves relative to itself: an offset of -1 would
continue at the previous instruction, while an offset of 2 would skip
over the next instruction.

For example:

cpy 41 a
inc a
inc a
dec a
jnz a 2
dec a

The above code would set register a to 41, increase its value by 2,
decrease its value by 1, and then skip the last dec a (because a is
not zero, so the jnz a 2 skips it), leaving register a at 42. When you
move past the last instruction, the program halts.

After executing the assembunny code in your puzzle input, what value
is left in register a?

--- Part Two ---

As you head down the fire escape to the monorail, you notice it didn't
start; register c needs to be initialized to the position of the
ignition key.

If you instead initialize register c to be 1, what value is now left
in register a?

'''

import re


def reg(s):
    return ord(s[0]) - ord('a')


def icpy(regs, val, y):
    regs[y] = val
    return 1


def cpy(regs, x, y):
    regs[y] = regs[x]
    return 1


def inc(regs, a):
    regs[a] += 1
    return 1


def dec(regs, a):
    regs[a] -= 1
    return 1


def jnz(regs, a, count):
    return count if regs[a] != 0 else 1


def run(tape, regs=[0, 0, 0, 0]):
    ip = 0
    while ip < len(tape):
        # print ip, tape[ip], regs
        ip += tape[ip](regs)
    return regs

with open('12.txt') as f:
    TAPE = []
    for line in f:
        line = line.strip()
        m = re.match('cpy (-?\d+) ([a-d])', line)
        if m:
            TAPE.append(lambda x, val=int(m.group(1)),
                        r=reg(m.group(2)): icpy(x, val, r))
            continue
        m = re.match('cpy ([a-d]) ([a-d])', line)
        if m:
            TAPE.append(lambda x, src=reg(m.group(1)),
                        dest=reg(m.group(2)): cpy(x, src, dest))
            continue
        m = re.match('inc ([a-d])', line)
        if m:
            TAPE.append(lambda x, dest=reg(m.group(1)): inc(x, dest))
            continue
        m = re.match('dec ([a-d])', line)
        if m:
            TAPE.append(lambda x, dest=reg(m.group(1)): dec(x, dest))
            continue
        m = re.match('jnz ([a-d]) (-?\d+)', line)
        if m:
            TAPE.append(lambda x, r=reg(m.group(1)), count=int(m.group(2)):
                        jnz(x, r, count))
            continue
        m = re.match('jnz (-?\d+) (-?\d+)', line)
        if m:
            TAPE.append(lambda x, val=int(m.group(1)), count=int(m.group(2)):
                        count if val != 0 else 1)
            continue
        assert False, 'Unknown asm: ' + line
    print run(TAPE)
    print run(TAPE, regs=[0, 0, 1, 0])
