#!/usr/bin/env python3

from aoc import *

print(
    """
#include <cstdint>

auto monad(int64_t input) {
    int64_t place = 10000000000000L;
    auto get_input = [&place](auto input) mutable {
        int val = (input / place) % 10;
        place /= 10;
        return val;
    };
    int64_t w = 0, x = 0, y = 0, z = 0;
"""
)

with open("24.txt") as f:
    for line in f.read().splitlines():
        line = vector(line)
        if line[0] == "inp":
            print(f"    {line[1]} = get_input(input);")
            print(f"    if ({line[1]} == 0) return -1L;")
        elif line[0] == "add":
            print(f"    {line[1]} += {line[2]};")
        elif line[0] == "mul":
            print(f"    {line[1]} *= {line[2]};")
        elif line[0] == "div":
            print(f"    {line[1]} /= {line[2]};")
        elif line[0] == "mod":
            print(f"    {line[1]} %= {line[2]};")
        elif line[0] == "eql":
            print(f"    {line[1]} = {line[1]} == {line[2]} ? 1 : 0;")
        else:
            assert False, line

print(
    """
    return z;
}"""
)
