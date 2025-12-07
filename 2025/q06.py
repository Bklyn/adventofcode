#!/usr/bin/env python3

from aoc import array
from aocd import data
from functools import reduce
import operator
import itertools

OPS = {"*": operator.mul, "+": operator.add}


def squid_math(input: str) -> int:
    data = array(input)
    assert all(len(row) == len(data[0]) for row in data[1:])
    rows = data[:-1]
    ops = [OPS[op] for op in data[-1]]
    cols = [[row[col] for row in rows] for col in range(len(ops))]
    answers = [reduce(ops[i], cols[i]) for i in range(len(cols))]
    return sum(answers)


def squid_math2(input: str) -> int:
    lines = input.splitlines()
    # find colunms with all spaces; add zero and trailing column
    gutters = (
        [0]
        + [c for c in range(len(lines[0])) if all(line[c] == " " for line in lines)]
        + [len(lines[0])]
    )
    result = 0
    for lo, hi in itertools.pairwise(gutters):
        op = None
        vals = []
        for idx in range(lo, hi):
            val = "".join(line[idx] for line in lines).strip()
            if not val:
                continue
            if val[-1] in OPS:
                op = OPS[val[-1]]
                val = val[:-1]
            vals.append(int(val.strip()))
        assert op is not None
        result += reduce(op, vals)
    return result


def test_squid_math():
    ex = """123 328  51 64 
 45 64  387 23 
  6 98  215 314
*   +   *   +  """
    assert 4277556 == squid_math(ex)
    assert 3263827 == squid_math2(ex)


if __name__ == "__main__":
    print(squid_math(data))
    print(squid_math2(data))
