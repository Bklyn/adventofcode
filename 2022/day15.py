#!/usr/bin/env python3

from aoc import Puzzle, X, Y, cityblock_distance
import re


def impact(sensor, distance, row):
    sx, sy = X(sensor), Y(sensor)
    dy = abs(row - sy)
    delta = distance - dy
    if delta < 0:
        return None
    return (sx - delta, sx + delta)


def overlap(ranges):
    ranges = sorted(ranges)
    it = iter(ranges)
    try:
        curr_start, curr_stop = next(it)
    except StopIteration:
        return
    for start, stop in it:
        if curr_start <= start <= curr_stop + 1:
            curr_stop = max(curr_stop, stop)
        else:
            yield (curr_start, curr_stop)
            curr_start, curr_stop = start, stop
    yield curr_start, curr_stop


def find_gap(sensors, limit):
    """Find the one uncovered cell in [0, limit]^2 via boundary-line intersection.

    The cell sits just outside several sensor diamonds, where a slope +1 edge
    (on which x - y is constant) meets a slope -1 edge (on which x + y is
    constant). Each diamond contributes two "one step outside" boundaries per
    family, so we intersect every ascending with every descending candidate --
    O(sensors^2) pairs -- and keep the in-bounds point no sensor covers.
    """
    asc = set()  # values of a = x - y on each diamond's +1 boundary, d+1 out
    desc = set()  # values of b = x + y on each diamond's -1 boundary, d+1 out
    for (sx, sy), d in sensors.items():
        asc.add(sx - sy + d + 1)
        asc.add(sx - sy - d - 1)
        desc.add(sx + sy + d + 1)
        desc.add(sx + sy - d - 1)
    for a in asc:
        for b in desc:
            if (a + b) % 2:  # x, y must be integers
                continue
            x, y = (a + b) // 2, (b - a) // 2
            if not (0 <= x <= limit and 0 <= y <= limit):
                continue
            if all(
                cityblock_distance((sx, sy), (x, y)) > d
                for (sx, sy), d in sensors.items()
            ):
                return x, y
    return None


def beacons(input, row):
    sensors = dict()
    beacons = set()
    for line in input.splitlines():
        m = re.match(
            r"Sensor at x=([^,]+), y=([^:]+): closest beacon is at x=([^,]+), y=(.+)",
            line,
        )
        assert m

        sensor = tuple(int(x) for x in m.groups()[:2])
        beacon = tuple(int(x) for x in m.groups()[2:])
        dist = cityblock_distance(sensor, beacon)
        sensors[sensor] = dist
        beacons.add(beacon)
    impacts = list(
        overlap(
            x for x in (impact(s, sensors[s], row) for s in sensors) if x is not None
        )
    )
    coverage = (
        sum(y - x + 1 for x, y in impacts)
        - sum(1 for b in beacons if b[1] == row)
        - sum(1 for s in sensors if s[1] == row)
    )
    # Find the single uncovered cell. The search box is 0..2*row on each axis
    # (row is the part-1 midline: 10 -> 0..20 for the example, 2e6 -> 0..4e6).
    x, y = find_gap(sensors, 2 * row)
    freq = x * 4_000_000 + y
    return coverage, freq


EXAMPLE = """Sensor at x=2, y=18: closest beacon is at x=-2, y=15
Sensor at x=9, y=16: closest beacon is at x=10, y=16
Sensor at x=13, y=2: closest beacon is at x=15, y=3
Sensor at x=12, y=14: closest beacon is at x=10, y=16
Sensor at x=10, y=20: closest beacon is at x=10, y=16
Sensor at x=14, y=17: closest beacon is at x=10, y=16
Sensor at x=8, y=7: closest beacon is at x=2, y=10
Sensor at x=2, y=0: closest beacon is at x=2, y=10
Sensor at x=0, y=11: closest beacon is at x=2, y=10
Sensor at x=20, y=14: closest beacon is at x=25, y=17
Sensor at x=17, y=20: closest beacon is at x=21, y=22
Sensor at x=16, y=7: closest beacon is at x=15, y=3
Sensor at x=14, y=3: closest beacon is at x=15, y=3
Sensor at x=20, y=1: closest beacon is at x=15, y=3"""


def test_beacons():
    assert beacons(EXAMPLE, 10) == (26, 56000011)


if __name__ == "__main__":
    p = Puzzle(day=15)
    assert beacons(EXAMPLE, 10) == (26, 56000011)
    print(beacons(p.input_data, 2_000_000))
