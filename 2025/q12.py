#!/usr/bin/env python3

from aocd import data
from aoc import vector


def fit_presents(input: str) -> int:
    presents = []
    answer = 0
    for section in input.split("\n\n"):
        if "x" not in section:
            # Only need to know how many bits are set
            presents.append(section.count("#"))
            continue

        # As it turns out, rotations and shape placing are not needed.  Every area is either
        # smaller than the total number of set bits for the requested presents or there are enough
        # 3x3 tiles to fit everything with no overlaps
        for line in section.splitlines():
            width, height, *counts = vector(line.replace("x", " "))
            tiles = (width // 3) * (height // 3)
            present_bits = sum(bits * count for bits, count in zip(presents, counts))
            assert present_bits > width * height or tiles >= sum(counts)
            answer += tiles >= sum(counts)

    return answer


if __name__ == "__main__":
    print(fit_presents(data))
