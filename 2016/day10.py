#!/usr/bin/env python

'''--- Day 10: Balance Bots ---

You come upon a factory in which many robots are zooming around
handing small microchips to each other.

Upon closer examination, you notice that each bot only proceeds when
it has two microchips, and once it does, it gives each one to a
different bot or puts it in a marked "output" bin. Sometimes, bots
take microchips from "input" bins, too.

Inspecting one of the microchips, it seems like they each contain a
single number; the bots must use some logic to decide what to do with
each chip. You access the local control computer and download the
bots' instructions (your puzzle input).

Some of the instructions specify that a specific-valued microchip
should be given to a specific bot; the rest of the instructions
indicate what a given bot should do with its lower-value or
higher-value chip.

For example, consider the following instructions:

value 5 goes to bot 2
bot 2 gives low to bot 1 and high to bot 0
value 3 goes to bot 1
bot 1 gives low to output 1 and high to bot 0
bot 0 gives low to output 2 and high to output 0
value 2 goes to bot 2

Initially, bot 1 starts with a value-3 chip, and bot 2 starts with a
value-2 chip and a value-5 chip.  Because bot 2 has two microchips, it
gives its lower one (2) to bot 1 and its higher one (5) to bot 0.
Then, bot 1 has two microchips; it puts the value-2 chip in output 1
and gives the value-3 chip to bot 0.  Finally, bot 0 has two
microchips; it puts the 3 in output 2 and the 5 in output 0.

In the end, output bin 0 contains a value-5 microchip, output bin 1
contains a value-2 microchip, and output bin 2 contains a value-3
microchip. In this configuration, bot number 2 is responsible for
comparing value-5 microchips with value-2 microchips.

Based on your instructions, what is the number of the bot that is
responsible for comparing value-61 microchips with value-17
microchips?

--- Part Two ---

What do you get if you multiply together the values of one chip in
each of outputs 0, 1, and 2?

'''

import re
from collections import defaultdict

bots = defaultdict (list)
rules = {}
compares = {}
outputs = defaultdict (list)

def step (bot):
    chips = sorted (bots.get (bot, []))
    if len (chips) < 2:
        return False
    compares[tuple(chips)] = bot
    for chip, dest in zip (chips, rules[bot]):
        dest.append (chip)
    bots.pop (bot)
    return True

def run ():
    while filter (step, bots.keys ()):
        pass
    pass

with open ('10.txt') as f:
    for input in f:
        input = input.strip ()
        m = re.match ('value (\d+) goes to bot (\d+)', input)
        if m:
            value, bot = map (int, m.group (1, 2))
            bots[bot].append (value)
            continue
        m = re.match ('bot (\d+) gives low to (bot|output) (\d+) and high to (bot|output) (\d+)', input)
        if m:
            bot, low, high = map (int, m.group (1, 3, 5))
            if m.group (2) == 'bot':
                low = bots[low]
            else:
                low = outputs[low]
            if m.group (4) == 'bot':
                high = bots[high]
            else:
                high = outputs[high]
            rules[bot] = (low, high)
            continue
        assert False, 'Unparsed input: ' + input
    run ()

print compares[(17, 61)]
print outputs[0][0] * outputs[1][0] * outputs[2][0]
