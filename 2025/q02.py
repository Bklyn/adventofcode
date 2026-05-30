#!/usr/bin/env python3

from bisect import bisect_left, bisect_right
from itertools import accumulate

from aoc import solver


def invalid_id(i: int) -> int:
    """Reference predicate (part 1): ID whose digits are two equal halves, else 0."""
    s = str(i)
    length = len(s)
    if length % 2 == 0 and s[: length // 2] == s[length // 2 :]:
        return i
    return 0


def repeated_id(val: int) -> int:
    """Reference predicate (part 2): ID whose digits are a block repeated >=2x, else 0."""
    s = str(val)
    for i in range(1, len(s) // 2 + 1):
        ntokens, remainder = divmod(len(s), i)
        if remainder:
            continue
        prefix = s[:i]
        for j in range(1, ntokens):
            if s[i * j : i * (j + 1)] != prefix:
                break
        else:
            return val
    return 0


def _parse_ranges(input: str) -> list[tuple[int, int]]:
    """Parse the comma-separated 'lo-hi' ranges (which may wrap across lines)."""
    joined = "".join(input.strip().splitlines())
    return [
        (int(lo), int(hi)) for lo, hi in (r.split("-", 1) for r in joined.split(","))
    ]


def _special_ids(part2: bool, max_len: int) -> list[int]:
    """Distinct matching IDs up to max_len digits, sorted ascending.

    Both predicates select *periodic* numbers -- a digit block repeated. Part 1
    wants exactly two equal halves (period length // 2, repeated twice); part 2
    wants any block repeated >=2 times (any proper-divisor period). Generating
    these directly is vastly cheaper than testing every integer in the ranges.
    """
    values: set[int] = set()
    for length in range(2, max_len + 1):
        if part2:
            periods = [p for p in range(1, length) if length % p == 0]
        elif length % 2 == 0:
            periods = [length // 2]
        else:
            continue
        for p in periods:
            reps = length // p
            for block in range(10 ** (p - 1), 10**p):
                values.add(int(str(block) * reps))
    return sorted(values)


@solver(part=1)
@solver(part=2, args=(True,))
def invalid_ids(input: str, part2=False) -> int:
    ranges = _parse_ranges(input)
    ids = _special_ids(part2, len(str(max(hi for _, hi in ranges))))
    prefix = [0, *accumulate(ids)]
    total = 0
    for lo, hi in ranges:
        total += prefix[bisect_right(ids, hi)] - prefix[bisect_left(ids, lo)]
    return total


EXAMPLE = """
11-22,95-115,998-1012,1188511880-1188511890,222220-222224,
1698522-1698528,446443-446449,38593856-38593862,565653-565659,
824824821-824824827,2121212118-2121212124"""


def _brute(input: str, part2: bool) -> int:
    """O(range) reference scan, used only to validate the fast invalid_ids."""
    total = 0
    for lo, hi in _parse_ranges(input):
        for i in range(lo, hi + 1):
            total += repeated_id(i) if part2 else invalid_id(i)
    return total


def test_invalid_ids():
    assert invalid_ids(EXAMPLE) == 1227775554
    assert invalid_ids(EXAMPLE, True) == 4174379265


def test_invalid_ids_matches_brute():
    import random

    random.seed(0)
    for _ in range(40):
        lo = random.randint(1, 2_000_000)
        inp = f"{lo}-{lo + random.randint(0, 4000)}"
        assert invalid_ids(inp) == _brute(inp, False)
        assert invalid_ids(inp, True) == _brute(inp, True)


if __name__ == "__main__":
    from aocd import data

    print(invalid_ids(data))
    print(invalid_ids(data, True))
