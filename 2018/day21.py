#!/usr/bin/env python3
'''--- Day 21: Chronal Conversion ---

You should have been watching where you were going, because as you
wander the new North Pole base, you trip and fall into a very deep
hole!

Just kidding. You're falling through time again.

If you keep up your current pace, you should have resolved all of the
temporal anomalies by the next time the device activates. Since you
have very little interest in browsing history in 500-year increments
for the rest of your life, you need to find a way to get back to your
present time.

After a little research, you discover two important facts about the
behavior of the device:

First, you discover that the device is hard-wired to always send you
back in time in 500-year increments. Changing this is probably not
feasible.

Second, you discover the activation system (your puzzle input) for the
time travel module. Currently, it appears to run forever without
halting.

If you can cause the activation system to halt at a specific moment,
maybe you can make the device send you so far back in time that you
cause an integer underflow in time itself and wrap around back to your
current time!

The device executes the program as specified in manual section one and
manual section two.

Your goal is to figure out how the program works and cause it to
halt. You can only control register 0; every other register begins at
0 as usual.

Because time travel is a dangerous activity, the activation system
begins with a few instructions which verify that bitwise AND (via
bani) does a numeric operation and not an operation as if the inputs
were interpreted as strings. If the test fails, it enters an infinite
loop re-running the test instead of allowing the program to execute
normally. If the test passes, the program continues, and assumes that
all other bitwise operations (banr, bori, and borr) also interpret
their inputs as numbers. (Clearly, the Elves who wrote this system
were worried that someone might introduce a bug while trying to
emulate this system with a scripting language.)

What is the lowest non-negative integer value for register 0 that
causes the program to halt after executing the fewest instructions?
(Executing the same instruction multiple times counts as multiple
instructions executed.)
'''

from aoc2018 import *

MACH = {'addr': lambda regs, args: regs[args[0]] + regs[args[1]],
        'addi': lambda regs, args: regs[args[0]] + args[1],
        'mulr': lambda regs, args: regs[args[0]] * regs[args[1]],
        'muli': lambda regs, args: regs[args[0]] * args[1],
        'banr': lambda regs, args: regs[args[0]] & regs[args[1]],
        'bani': lambda regs, args: regs[args[0]] & args[1],
        'borr': lambda regs, args: regs[args[0]] | regs[args[1]],
        'bori': lambda regs, args: regs[args[0]] | args[1],
        'setr': lambda regs, args: regs[args[0]],
        'seti': lambda regs, args: args[0],
        'gtir': lambda regs, args: 1 if args[0] > regs[args[1]] else 0,
        'gtri': lambda regs, args: 1 if regs[args[0]] > args[1] else 0,
        'gtrr': lambda regs, args: 1 if regs[args[0]] > regs[args[1]] else 0,
        'eqir': lambda regs, args: 1 if args[0] == regs[args[1]] else 0,
        'eqri': lambda regs, args: 1 if regs[args[0]] == args[1] else 0,
        'eqrr': lambda regs, args: 1 if regs[args[0]] == regs[args[1]] else 0}


def execute(tape, regs=None, debug=False):
    ipreg = tape[0][1]
    assert ipreg >= 0 and ipreg < 6
    tape = tuple(tape[1:])
    if regs is None:
        regs = [0] * 6
    ip = 0
    cycles = 0
    while ip >= 0 and ip < len(tape):
        cycles += 1
        regs[ipreg] = ip
        insn, *args = tape[ip]
        regs[args[2]] = MACH[insn](regs, args) & 0xffffffff
        if debug or cycles % 10 ** 6 == 0:
            print(cycles, ip, [], insn, args, regs)
        ip = regs[ipreg] + 1
    return regs, cycles


tape = array(Input(21).read())
result = execute(tape, regs=[37, 0, 0, 0, 0, 0], debug=True)
print(result)
