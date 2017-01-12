#!/usr/bin/env python

'''
--- Day 23: Safe Cracking ---

This is one of the top floors of the nicest tower in EBHQ. The Easter
Bunny's private office is here, complete with a safe hidden behind a
painting, and who wouldn't hide a star in a safe behind a painting?

The safe has a digital screen and keypad for code entry. A sticky note
attached to the safe has a password hint on it: "eggs". The painting
is of a large rabbit coloring some eggs. You see 7.

When you go to type the code, though, nothing appears on the display;
instead, the keypad comes apart in your hands, apparently having been
smashed. Behind it is some kind of socket - one that matches a
connector in your prototype computer! You pull apart the smashed
keypad and extract the logic circuit, plug it into your computer, and
plug your computer into the safe.

Now, you just need to figure out what output the keypad would have
sent to the safe. You extract the assembunny code from the logic chip
(your puzzle input).  The code looks like it uses almost the same
architecture and instruction set that the monorail computer used! You
should be able to use the same assembunny interpreter for this as you
did there, but with one new instruction:

tgl x toggles the instruction x away (pointing at instructions like
jnz does: positive means forward; negative means backward):

- For one-argument instructions, inc becomes dec, and all other
  one-argument instructions become inc.

- For two-argument instructions, jnz becomes cpy, and all other
  two-instructions become jnz.

- The arguments of a toggled instruction are not affected.

- If an attempt is made to toggle an instruction outside the program,
  nothing happens.

- If toggling produces an invalid instruction (like cpy 1 2) and an
  attempt is later made to execute that instruction, skip it instead.

- If tgl toggles itself (for example, if a is 0, tgl a would target
  itself and become inc a), the resulting instruction is not executed
  until the next time it is reached.

For example, given this program:

cpy 2 a
tgl a
tgl a
tgl a
cpy 1 a
dec a
dec a

- cpy 2 a initializes register a to 2.

- The first tgl a toggles an instruction a (2) away from it, which
  changes the third tgl a into inc a.

- The second tgl a also modifies an instruction 2 away from it, which
  changes the cpy 1 a into jnz 1 a.

- The fourth line, which is now inc a, increments a to 3.

- Finally, the fifth line, which is now jnz 1 a, jumps a (3)
instructions ahead, skipping the dec a instructions.

In this example, the final value in register a is 3.

The rest of the electronics seem to place the keypad entry (the number
of eggs, 7) in register a, run the code, and then send the value left
in register a to the safe.

What value should be sent to the safe?

To begin, get your puzzle input.

--- Part Two ---

The safe doesn't open, but it does make several angry noises to
express its frustration.

You're quite sure your logic is working correctly, so the only other
thing is... you check the painting again. As it turns out, colored
eggs are still eggs. Now you count 12.

As you run the program with this new input, the prototype computer
begins to overheat. You wonder what's taking so long, and whether the
lack of any instruction more powerful than "add one" has anything to
do with it. Don't bunnies usually multiply?

Anyway, what value should actually be sent to the safe?
'''

import re
import signal

cpy, inc, dec, jnz, tgl = 0, 1, 2, 3, 4
inames = ['cpy', 'inc', 'dec', 'jnz', 'tgl']

def val(s, regs):
    if type(s) == int:
        return s
    return regs[s]


def run(tape, regs={'a': 0, 'b': 0, 'c': 0, 'd': 0}, trace=False):
    ip = 0
    ic = 0

    def handler(signum, frame):
        print ip, ic, inames[tape[ip][0]], tape[ip][1], regs
        signal.alarm(5)
    signal.signal(signal.SIGALRM, handler)
    signal.alarm(5)

    while ip < len(tape):
        ic += 1
        if trace:
            print ip, ic, inames[tape[ip][0]], tape[ip][1], regs, '->',
        insn, args = tape[ip]
        step = 1
        if insn == cpy:
            x, y = args
            if y in regs:
                regs[y] = val (x, regs)
        elif insn == inc:
            # Optimize multiply a*b:
            # cpy b c
            # inc a
            # dec c
            # jnz c -2
            # dec d
            # jnz d -5
            if (args[0] in regs and
                ip > 0 and ip + 4 < len(tape) and
                tape[ip-1][0] == cpy and
                tape[ip+1][0] == dec and tape[ip+1][1][0] == tape[ip-1][1][1] and
                tape[ip+2][0] == jnz and tape[ip+2][1][0] == tape[ip-1][1][1] and
                tape[ip+2][1][1] == -2 and
                tape[ip+3][0] == dec and
                tape[ip+4][0] == jnz and tape[ip+4][1][0] == tape[ip+3][1][0] and
                tape[ip+4][1][1] == -5):
                mult = (tape[ip-1][1][0], tape[ip+3][1][0])
                # print 'mult', args[0], mult, tape[ip-1:ip+5], regs,
                regs[args[0]] += (val (mult[0], regs) * val (mult[1], regs))
                regs[tape[ip+1][1][0]] = 0
                regs[tape[ip+3][1][0]] = 0
                step = 5
            elif args[0] in regs:
                regs[args[0]] += 1
        elif insn == dec:
            if args[0] in regs:
                regs[args[0]] -= 1
        elif insn == jnz:
            x, y = map (lambda s: val(s, regs), args)
            if x != 0:
                step = y
        elif insn == tgl:
            x = val(args[0], regs)
            # print 'tgl', args[0], x, regs
            refip = ip + x
            if refip >= 0 and refip < len (tape):
                insn, args = tape[refip]
                if len(args) == 1:
                    if insn == inc:
                        insn = dec
                    else:
                        insn = inc
                else:
                    if insn == jnz:
                        insn = cpy
                    else:
                        insn = jnz
                tape[refip] = (insn, args)
        else:
            assert False, 'Illegal instruction: %s' % insn
        if trace:
            print regs, ip + step
        ip += step

    signal.alarm(0)
    return regs

def read(fn):
    tape = []
    with open(fn) as f:
        for line in [line.strip() for line in f.readlines()]:
            m = re.match('cpy (-?\d+|[a-d]) ([a-d])', line)
            if m:
                x = m.group(1)
                if not x.isalpha():
                    x = int(x)
                tape.append ((cpy, (x, m.group(2))))
                continue
            m = re.match('inc ([a-d])', line)
            if m:
                tape.append((inc, (m.group(1))))
                continue
            m = re.match('dec ([a-d])', line)
            if m:
                tape.append((dec, (m.group(1))))
                continue
            m = re.match('jnz (-?\d+|[a-d]) (-?\d+|[a-d])', line)
            if m:
                x, y = m.group (1, 2)
                if not x.isalpha():
                    x = int(x)
                if not y.isalpha():
                    y = int(y)
                tape.append((jnz, (x, y)))
                continue
            m = re.match ('tgl (-?\d+|[a-d])', line)
            if m:
                x = m.group(1)
                if not x.isalpha():
                    x = int(x)
                tape.append((tgl, (x)))
                continue
            assert False, 'Unknown asm: ' + line
    return tape

tape = read('23.txt')

print run(tape[:], regs={'a': 7, 'b': 0, 'c': 0, 'd': 0}, trace=False)
# [12860, 1, 0, 0]
print run(tape[:], regs={'a': 12, 'b': 0, 'c': 0, 'd': 0}, trace=False)
