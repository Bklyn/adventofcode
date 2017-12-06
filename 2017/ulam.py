#!/usr/bin/python
# coding: utf-8

'''Ulam spiral test code

37  36  35  34  33  32  31
38  17  16  15  14  13  30
39  18   5   4   3  12  29
40  19   6   1   2  11  28
41  20   7   8   9  10  27
42  21  22  23  24  25  26
43  44  45  46  47  48  49 ...

perimiters of squares
1: 1             (0^2+1 ... 1^2)
2-9: 8    (2*4)  (1^2+1 ... 3^2)
10-25: 16 (4*4)  (3^2+1 ... 5^2)
26-49: 24 (6*4)  (5^2+1 ... 7^2)
50-81: 32 (8*4)  (7^2+1 ... 9^2)

Coordinate logic mostly from, but that is buggy

https://math.stackexchange.com/questions/617574/inverse-of-ulams-spiral
'''

from __future__ import print_function
import math

def coord(n):
    k = int (math.sqrt (n))
    m = n - k*k
    if k % 2 == 0:              # Even
       c = (1-(k//2), k//2)
       if m == 0:
           pass
       elif m <= k+1:
           c = (c[0]-1, c[1]-(m-1))
       else:
           m = n - (k*k + k + 1)
           c = (-k//2 + m, -k//2)
    else:                        # Odd
        c = ((k-1)//2, -(k-1)//2)
        if m == 0:
            pass
        elif m <= k+1:
            c = (c[0]+1,c[1]+m-1)
        else:
            m = n - (k*k + k + 1)
            c = (1+(k//2), 1+(k//2))
            c = (c[0]-m, c[1])
    # print (n, k, m, c)
    return c

def distance(p):
    return abs(p[0])+abs(p[1])

def test_coord():
    assert coord(1) == (0,0)
    assert coord(2) == (1,0)
    assert coord(3) == (1,1)
    assert coord(4) == (0,1)
    assert coord(5) == (-1,1)
    assert coord(6) == (-1,0)
    assert coord(7) == (-1,-1)
    assert coord(8) == (0,-1)
    assert coord(9) == (1,-1)
    assert coord(10) == (2,-1)
    assert coord(11) == (2,0)
    assert coord(36) == (-2, 3)
    assert coord(37) == (-3, 3)
    assert coord(35) == (-1, 3)
    assert coord(42) == (-3, -2)

print (distance (coord (265149)))

def neighbors(p):
    for dx in (-1, 0, 1):
        for dy in (-1, 0, 1):
            if dx == 0 and dy == 0:
                continue
            yield (p[0] + dx, p[1] + dy)

assert list(neighbors((0,0))) == [(-1, -1), (-1, 0), (-1, 1), (0, -1), (0, 1), (1, -1), (1, 0), (1, 1)]

def harder(n, cache={}):
    cache[(0, 0)] = 1
    result = 1
    for i in xrange (2, n + 1):
        c = coord(i)
        result = 0
        for p in neighbors(c):
            v = cache.get (p)
            if v is None:
                continue
            result += v
        cache[c] = result
    return result

assert harder(1) == 1
assert harder(14) == 122

for i in xrange (1, 265149):
    result = harder (i, {})
    if result > 265149:
        print (result)
        break
