#!/usr/bin/env python3


def unlock_wrong(input: str, dial=100, pos=50):
    zeroes = 0
    thru_zero = 0
    for step in input.strip().splitlines():
        sign = -1 if step[0] == "L" else 1
        spins, remainder = divmod(int(step[1:]), dial)
        thru_zero += spins
        if remainder:
            new_pos = pos + sign * remainder
            assert -dial < pos < dial
            if new_pos <= 0 or new_pos >= dial:
                thru_zero += 1
            pos = new_pos % dial
        if pos == 0:
            zeroes += 1
    return zeroes, thru_zero


def unlock(input: str, dial=100, pos=50):
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


def test_unlock():
    assert (3, 6) == unlock(
        """L68
L30
R48
L5
R60
L55
L1
L99
R14
L82"""
    )


if __name__ == "__main__":
    from aocd import data

    print(unlock(data))
