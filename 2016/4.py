#!/usr/bin/env python


'''--- Day 4: Security Through Obscurity ---

Finally, you come across an information kiosk with a list of rooms. Of
course, the list is encrypted and full of decoy data, but the
instructions to decode the list are barely hidden nearby. Better
remove the decoy data first.

Each room consists of an encrypted name (lowercase letters separated
by dashes) followed by a dash, a sector ID, and a checksum in square
brackets.

A room is real (not a decoy) if the checksum is the five most common
letters in the encrypted name, in order, with ties broken by
alphabetization. For example:

* aaaaa-bbb-z-y-x-123[abxyz] is a real room because the most common
letters are a (5), b (3), and then a tie between x, y, and z, which
are listed alphabetically.

* a-b-c-d-e-f-g-h-987[abcde] is a real room because although the
letters are all tied (1 of each), the first five are listed
alphabetically.  not-a-real-room-404[oarel] is a real room.

* totally-real-room-200[decoy] is not.

Of the real rooms from the list above, the sum of their sector IDs is
1514.

What is the sum of the sector IDs of the real rooms?'''

import re
import string
from collections import defaultdict

ROOM = re.compile (r'([-a-z]+)-(\d+)\[([a-z]{5})\]')

def sorter (x, y):
    diff = x[1] - y[1]
    if diff != 0:
        return -diff
    return cmp (x[0], y[0])

def decode (name, sector):
    shift = sector % len (string.lowercase)
    trans = string.maketrans (
        string.lowercase + '-',
        string.lowercase[shift:] + string.lowercase[:shift] + ' ')
    return string.translate (name, trans)

answer = 0

with open ('4.txt') as f:
    for line in f:
        m = ROOM.match (line.strip ())
        if not m:
            print >>sys.stderr, line
        name = m.group (1)
        freq = defaultdict (int)
        for letter in [c for c in name if c.isalpha()]:
            freq[letter] += 1
        mysum = ''.join ((map (lambda x: x[0], sorted (freq.items (), sorter)))[:5])
        sector = int (m.group (2))
        checksum = m.group (3)
        # print name, sector, checksum, mysum
        if mysum == checksum:
            answer += sector
        print sector, decode (name, sector)

print answer
