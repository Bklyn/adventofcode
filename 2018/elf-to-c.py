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

OPS = {'add': '+', 'mul': '*', 'ban': '&', 'bor': '|', 'gt': '>', 'eq': '=='}


def value(insn, arg, isreg=False):
    if isreg or insn.endswith('r'):
        return chr(ord('a') + arg)
    return arg


def spit(tape):
    ipreg = tape[0][1]
    assert ipreg >= 0 and ipreg < 6
    tape = tuple(tape[1:])
    ip = 0
    cycles = 0
    last_test = None
    for lineno, (insn, *args) in enumerate(tape):
        prefix = insn[:3]
        dest = value(insn, args[-1], True)
        if prefix in OPS:
            code = '{} = {} {} {}'.format(
                dest, value(insn, args[0], True), OPS[prefix], value(insn, args[1]))
        elif prefix == 'set':
            code = '{} = {}'.format(dest, value(insn, args[0]))
        elif insn[:2] in OPS:
            last_test = '{} {} {}'.format(value(
                insn[2], args[0]), OPS[insn[:2]], value(insn[3], args[1]))
            code = '{} = ({})'.format(dest, last_test)
        else:
            code = '/* NOP */'
        print ('label_{}: ++insns; e = {};\n'.format(lineno, lineno))
        if args[-1] == ipreg:
            jmp = None
            if insn == 'addr':
                assert args[1] == ipreg
                print ('\tif ({}) goto label_{};'.format(
                    value(insn, args[0], True), lineno + 2))
            elif insn == 'addi':
                assert args[0] == ipreg
                print ('\tgoto label_{};'.format(lineno + args[1] + 1))
            elif insn == 'seti':
                print ('\tgoto label_{};'.format(value(insn, args[0]) + 1))
            else:
                assert False, (insn, args)
        else:
            print ('\t{};'.format(code))
            print ('#ifdef DEBUG\n\tprintf ("%ld {} {} {} [%d, %d, %d, %d, %d, %d]\\n", insns, a, b, c, d, e, f);\n#endif'.format(
                lineno, insn, args))
    print ('label_{}:'.format(len(tape)))


tape = array(Input(21).read())
spit(tape)
