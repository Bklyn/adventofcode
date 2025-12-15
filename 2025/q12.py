#!/usr/bin/env python3

from aocd import data
from aoc import vector

# 0 ... -> ... 0
# 1 ..# -> #.. 4
# 2 .#. -> .#. 2
# 3 .## -> ##. 6
# 4 #.. -> ..# 1
# 5 #.# -> #.# 5
# 6 ##. -> .## 3
# 7 ### -> ### 7

REFLECT = [0, 4, 2, 6, 1, 5, 3, 7]


def reflect_bits(present: tuple):
    return tuple(REFLECT[bits] for bits in present)


def reflect_shape(present: tuple) -> tuple:
    return tuple("".join(reversed(line)) for line in present)


def rotate_shape(shape: tuple):
    # Rows -> columns
    return tuple(
        ("".join(shape[r][c] for r in reversed(range(len(shape)))))
        for c in range(len(shape[0]))
    )


def rotations(present: tuple):
    seen = set()
    for shape in tuple(present), reflect_shape(present):
        if shape not in seen:
            yield shape
            seen.add(shape)
        # Three clockwise rotations
        for _ in range(4):
            shape = rotate_shape(shape)
            if shape not in seen:
                yield shape
                seen.add(shape)


def present_bits(lines):
    return tuple(int(line.replace("#", "1").replace(".", "0"), 2) for line in lines)


def fit_presents(input: str) -> int:
    presents = []
    bit_counts = []
    rotated = dict()
    areas = []
    answer = 0
    for section in input.split("\n\n"):
        if "x" not in section:
            key, *present = section.splitlines()
            num_bits = sum(x.bit_count() for x in present_bits(present))
            assert 0 < num_bits < 8
            key = int(key[:-1])
            presents.append(present)
            bit_counts.append(num_bits)
            rotated[key] = list(rotations(present))
            print(
                key,
                present_bits(presents[-1]),
                num_bits,
                rotated[key],
            )
            continue

        # As it turns out, tiling is not needed.  In every case where the presents can "fit", the number
        # of 3x3 regions under the tree is not less than the total present count
        for line in section.splitlines():
            width, height, *counts = vector(line.replace("x", " "))
            areas.append(((width, height), counts))
            # see if a fit is even possible
            tiles = divmod(width, 3)[0] * divmod(height, 3)[0]
            answer += tiles >= sum(counts)
            print(
                areas[-1],
                width * height,
                tiles >= sum(counts),
            )

    return answer


def test_presents():
    ex = """0:
###
##.
##.

1:
###
##.
.##

2:
.##
###
##.

3:
##.
###
##.

4:
###
#..
###

5:
###
.#.
###

4x4: 0 0 0 0 2 0
12x5: 1 0 1 0 2 2
12x5: 1 0 1 0 3 2"""

    assert 2 == fit_presents(ex)


if __name__ == "__main__":
    print(fit_presents(data))
