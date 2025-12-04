#!/usr/bin/env python3


def invalid_id(i: int) -> int:
    s = str(i)
    length = len(s)
    if length % 2 == 0 and s[: length // 2] == s[length // 2 :]:
        return i
    return 0


def repeated_id(val: int) -> int:
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


def invalid_ids(input: str, part2=False) -> int:
    result = 0
    input = "".join(input.strip().splitlines())
    for lo, hi in [r.split("-", 1) for r in input.split(",")]:
        for i in range(int(lo), int(hi) + 1):
            result += invalid_id(i) if not part2 else repeated_id(i)
    return result


def test_invalid_ids():
    assert 1227775554 == invalid_ids(
        """
11-22,95-115,998-1012,1188511880-1188511890,222220-222224,
1698522-1698528,446443-446449,38593856-38593862,565653-565659,
824824821-824824827,2121212118-2121212124"""
    )
    assert 4174379265 == invalid_ids(
        """
11-22,95-115,998-1012,1188511880-1188511890,222220-222224,
1698522-1698528,446443-446449,38593856-38593862,565653-565659,
824824821-824824827,2121212118-2121212124""",
        True,
    )


if __name__ == "__main__":
    from aocd import data

    print(invalid_ids(data))
    print(invalid_ids(data, True))
