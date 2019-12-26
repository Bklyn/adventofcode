#!/usr/bin/env python3
import itertools

PRELUDE = """
west
take fixed point
north
take sand
south
east
east
take asterisk
north
north
take hypercube
north
take coin
north
take easter egg
south
south
south
west
north
take spool of cat6
north
take shell
west
inv
"""

ITEMS = [
    "easter egg",
    "sand",
    "fixed point",
    "coin",
    "spool of cat6",
    "shell",
    "hypercube",
    "asterisk",
]


if __name__ == "__main__":
    print(PRELUDE.strip())
    for item in ITEMS:
        print("drop", item)
    inv = set()
    for len in range(2, len(ITEMS)):
        for combo in itertools.combinations(ITEMS, len):
            print("#", inv, combo)
            for item in set(combo) - inv:
                print("take", item)
                inv.add(item)
            for item in inv - set(combo):
                print("drop", item)
                inv.remove(item)
            print("inv")
            print("north")
