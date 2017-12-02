#!/usr/bin/env python3
'''--- Day 25: Clock Signal ---

You open the door and find yourself on the roof. The city sprawls away
from you for miles and miles.

There's not much time now - it's already Christmas, but you're nowhere
near the North Pole, much too far to deliver these stars to the sleigh
in time.

However, maybe the huge antenna up here can offer a solution. After
all, the sleigh doesn't need the stars, exactly; it needs the timing
data they provide, and you happen to have a massive signal generator
right here.

You connect the stars you have to your prototype computer, connect
that to the antenna, and begin the transmission.

Nothing happens.

You call the service number printed on the side of the antenna and
quickly explain the situation. "I'm not sure what kind of equipment
you have connected over there," he says, "but you need a clock
signal." You try to explain that this is a signal for a clock.

"No, no, a clock signal - timing information so the antenna computer
knows how to read the data you're sending it. An endless, alternating
pattern of 0, 1, 0, 1, 0, 1, 0, 1, 0, 1...." He trails off.

You ask if the antenna can handle a clock signal at the frequency you
would need to use for the data from the stars. "There's no way it can!
The only antenna we've installed capable of that is on top of a
top-secret Easter Bunny installation, and you're definitely not-" You
hang up the phone.

You've extracted the antenna's clock signal generation assembunny code
(your puzzle input); it looks mostly compatible with code you worked
on just recently.

This antenna code, being a signal generator, uses one extra
instruction:

- out x transmits x (either an integer or the value of a register) as
  the next value for the clock signal.

The code takes a value (via register a) that describes the signal to
generate, but you're not sure how it's used. You'll have to find the
input to produce the right signal through experimentation.

What is the lowest positive integer that can be used to initialize
register a and cause the code to output a clock signal of 0, 1, 0,
1... repeating forever?
'''

def parse(line):
    "Split line into words, and convert to int where appropriate."
    return [(x if x.isalpha() else int(x))
            for x in line.split()]

def toggle(code, i):
    if 0 <= i < len (code):
        inst = code[i]
        orig = inst[0]
        inst[0] = ('dec' if inst[0] == 'inc' else
                   'inc' if len(inst) == 2 else
                   'cpy' if inst[0] == 'jnz' else
                   'jnz')

def run(code, regs, steps=10**10):
    def val(x): return (regs[x] if x in regs else x)
    pc = 0
    for _ in range(steps):
        if not (0 <= pc <= len(code)):
            return
        inst = code[pc]
        op, x, y = inst[0], inst[1], inst[-1]
        pc += 1
        if   op == 'cpy' and y in regs: regs[y] = val(x)
        elif op == 'inc':               regs[x] += 1
        elif op == 'dec':               regs[x] -= 1
        elif op == 'jnz' and val(x):    pc += val(y) - 1
        elif op == 'tgl':               toggle (code, pc - 1 + val(x))
        elif op == 'out':               yield val(x)

x = '''
cpy a d
cpy 15 c
cpy 170 b
inc d
dec b
jnz b -2
dec c
jnz c -5
cpy d a
jnz 0 0
cpy a b
cpy 0 a
cpy 2 c
jnz b 2
jnz 1 6
dec b
dec c
jnz c -4
inc a
jnz 1 -7
cpy 2 b
jnz c 2
jnz 1 4
dec b
dec c
jnz 1 -4
jnz 0 0
out b
jnz a -19
jnz 1 -21
'''.strip()

code = [parse(line) for line in x.splitlines()]

import itertools

def repeats(a, code, steps=10**6, minsignals=100):
    signals = run(code, dict(a=a, b=0, c=0, d=0), steps)
    expecteds = itertools.cycle ((0, 1))
    for (i, (signal, expected)) in enumerate(zip(signals, expecteds)):
        if signal != expected:
            return False
    return i >= minsignals

def first(iterable): return next(iter(iterable))

print (first(a for a in range(1, 10**100) if repeats(a, code)))
