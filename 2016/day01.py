#!/usr/bin/env python

import fileinput

INPUT = '''L3, R1, L4, L1, L2, R4, L3, L3, R2, R3, L5, R1, R3, L4, L1, L2, R2, R1, L4, L4, R2, L5, R3, R2, R1, L1, L2, R2, R2, L1, L1, R2, R1, L3, L5, R4, L3, R3, R3, L5, L190, L4, R4, R51, L4, R5, R5, R2, L1, L3, R1, R4, L3, R1, R3, L5, L4, R2, R5, R2, L1, L5, L1, L1, R78, L3, R2, L3, R5, L2, R2, R4, L1, L4, R1, R185, R3, L4, L1, L1, L3, R4, L4, L1, R5, L5, L1, R5, L1, R2, L5, L2, R4, R3, L2, R3, R1, L3, L5, L4, R3, L2, L4, L5, L4, R1, L1, R5, L2, R4, R2, R3, L1, L1, L4, L3, R4, L3, L5, R2, L5, L1, L1, R2, R3, L5, L3, L2, L1, L4, R4, R4, L2, R3, R1, L2, R1, L2, L2, R3, R3, L1, R4, L5, L3, R4, R4, R1, L2, L5, L3, R1, R4, L2, R5, R4, R2, L5, L3, R4, R1, L1, R5, L3, R1, R5, L2, R1, L5, L2, R2, L2, L3, R3, R3, R1'''
DIRS = [(0, 1), (1, 0), (0, -1), (-1, 0)]
DIR = 0
x, y = (0, 0)
VISITED = set ([(x, y)])
FINAL = None

for op in INPUT.split (', '):
    dir = op[0]
    len = int (op[1:])
    if dir == 'R':
        DIR = (DIR + 1) % 4
    else:
        DIR = (DIR + 3) % 4
    vec = DIRS[DIR]
    for hop in range (1, len + 1):
        x = x + vec[0]
        y = y + vec[1]
        if FINAL is None:
            if (x, y) in VISITED:
                FINAL = (x, y)
            else:
                VISITED.add ((x, y))

print abs(x) + abs(y)
print abs(FINAL[0]) + abs(FINAL[1])
