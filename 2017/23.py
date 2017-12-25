#!/usr/bin/env python3

'''--- Day 23: Coprocessor Conflagration ---

You decide to head directly to the CPU and fix the printer from
there. As you get close, you find an experimental coprocessor doing so
much work that the local programs are afraid it will halt and catch
fire. This would cause serious issues for the rest of the computer, so
you head in and see what you can do.

The code it's running seems to be a variant of the kind you saw
recently on that tablet. The general functionality seems very similar,
but some of the instructions are different:

* set X Y sets register X to the value of Y.

* sub X Y decreases register X by the value of Y.

* mul X Y sets register X to the result of multiplying the value
contained in register X by the value of Y.

* jnz X Y jumps with an offset of the value of Y, but only if the value
of X is not zero. (An offset of 2 skips the next instruction, an
offset of -1 jumps to the previous instruction, and so on.)

Only the instructions listed above are used. The eight registers here,
named a through h, all start at 0.

The coprocessor is currently set to some kind of debug mode, which
allows for testing, but prevents it from doing any meaningful work.

If you run the program (your puzzle input), how many times is the mul
instruction invoked?

Your puzzle answer was 3969.

The first half of this puzzle is complete! It provides one gold star: *

--- Part Two ---

Now, it's time to fix the problem.

The debug mode switch is wired directly to register a. You flip the
switch, which makes register a now start at 1 when the program is
executed.

Immediately, the coprocessor begins to overheat. Whoever wrote this
program obviously didn't choose a very efficient
implementation. You'll need to optimize the program if it has any hope
of completing before Santa needs that printer working.

The coprocessor's ultimate goal is to determine the final value left
in register h once the program completes. Technically, if it had
that... it wouldn't even need to run the program.

After setting register a to 1, if the program were to run to
completion, what value would be left in register h?
'''

from aoc2017 import *


def run(tape, debug=False):
    regs = defaultdict(int)
    if debug:
        regs['a'] = 1

    def get(arg):
        if type(arg) == str:
            return regs[arg]
        return arg

    ip = 0
    counts = defaultdict(int)
    while ip < len(tape):
        insn, *args = tape[ip]
        if debug:
            print(ip + 1, insn, args, sorted(regs.items()))
        counts[insn] += 1
        if insn == 'set':
            regs[args[0]] = get(args[1])
        elif insn == 'sub':
            regs[args[0]] -= get(args[1])
        elif insn == 'mul':
            regs[args[0]] *= get(args[1])
        elif insn == 'jnz':
            if get(args[0]) != 0:
                ip += get(args[1]) - 1
            pass
        else:
            assert False, 'Unknown instruction: {}'.format(tape[ip])
        ip += 1
    return (regs, counts)


tape = array(Input(23))

_, counts = run(tape)
print(counts['mul'])
run(tape, debug=True)
