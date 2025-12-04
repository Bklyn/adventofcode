#!/usr/bin/env python3


def joltage(bank: str, digits: int = 2) -> int:
    best = 0
    start = 0
    while digits:
        end = len(bank) - digits + 1
        slice = bank[start:end]
        d = max(slice)
        i = slice.index(d)
        start += i + 1
        digits -= 1
        best = 10 * best + int(d)
    return best


def total_joltage(input: str, digits: int = 2) -> int:
    return sum(joltage(line, digits) for line in input.strip().splitlines())


def test_joltage():
    assert 357 == total_joltage(
        """987654321111111
811111111111119
234234234234278
818181911112111"""
    )
    assert 3121910778619 == total_joltage(
        """987654321111111
811111111111119
234234234234278
818181911112111""",
        12,
    )


if __name__ == "__main__":
    from aocd import data

    print(total_joltage(data))
    print(total_joltage(data, 12))
