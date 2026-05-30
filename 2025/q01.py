#!/usr/bin/env python3

from aoc import solver


@solver(part=1)
def unlock_fast(input: str, dial=100, pos=50):
    """Analytic O(operations) solver, validated against the brute-force unlock().

    Each move of N ticks is `spins` full revolutions (one zero-crossing each)
    plus a partial move of `remainder` ticks.
    """
    zeroes = 0
    thru_zero = 0
    for step in input.strip().splitlines():
        sign = -1 if step[0] == "L" else 1
        spins, remainder = divmod(int(step[1:]), dial)
        thru_zero += spins
        if remainder:
            new_pos = pos + sign * remainder
            assert -dial < pos < dial
            # A left move reaches 0 only if it started above 0: sitting on 0 and
            # moving left departs the mark (the next 0 is a full spin away, already
            # in `spins`). The right branch's `>= dial` test excludes a pos-0 start
            # for the same reason.
            crossed = new_pos >= dial if sign == 1 else (pos != 0 and new_pos <= 0)
            if crossed:
                thru_zero += 1
            pos = new_pos % dial
        if pos == 0:
            zeroes += 1
    return zeroes, thru_zero


def unlock(input: str, dial=100, pos=50):
    """Brute-force reference: step one tick at a time. Used to validate unlock_fast."""
    zeroes = 0
    thru_zero = 0
    for operation in input.strip().splitlines():
        direction = -1 if operation[0] == "L" else 1
        for _ in range(int(operation[1:])):
            pos = (pos + direction) % dial
            if pos == 0:
                thru_zero += 1
        if pos == 0:
            zeroes += 1
    return (zeroes, thru_zero)


EXAMPLE = """L68
L30
R48
L5
R60
L55
L1
L99
R14
L82"""


def test_unlock():
    assert (3, 6) == unlock(EXAMPLE)


def test_unlock_fast_matches_brute():
    # Regression for the L-from-0 phantom zero-crossing (minimal case: R50/L7).
    assert unlock_fast(EXAMPLE) == unlock(EXAMPLE) == (3, 6)
    assert unlock_fast("R50\nL7") == unlock("R50\nL7") == (1, 1)


if __name__ == "__main__":
    from aocd import data

    print(unlock_fast(data))
