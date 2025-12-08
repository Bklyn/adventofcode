#!/usr/bin/env python3

from aoc import array
from aocd import data

import math
import operator
from functools import reduce


def longest_circuits(input: str, npairs: int) -> int:
    boxes = array(input)
    distances = {}
    for i, (x, y, z) in enumerate(boxes):
        p = x, y, z
        for j in range(i + 1, len(boxes)):
            xx, yy, zz = q = boxes[j]
            dist = math.sqrt((xx - x) ** 2 + (yy - y) ** 2 + (zz - z) ** 2)
            distances[p, q] = dist

    closest = sorted(distances.keys(), key=lambda k: distances[k])

    def connect(circuits, p, q):
        pq = set([p, q])
        links = [c for c in circuits if c & pq]
        if len(links) == 2:
            for c in links:
                circuits.remove(c)
            circuit = set.union(*links)
            circuits.append(circuit)
        elif len(links) == 1:
            circuit = links[0]
        else:
            circuit = set()
            circuits.append(circuit)
        circuit.add(p)
        circuit.add(q)
        return circuit

    circuits = []
    for p, q in closest[:npairs]:
        connect(circuits, p, q)

    # Find 3 longest circuits
    longest = sorted(circuits, key=lambda c: len(c), reverse=True)
    part1 = reduce(operator.mul, [len(c) for c in longest[:3]])

    # Keep connecting the rest of the nodes until we have a single circuit
    for p, q in closest[npairs:]:
        circuit = connect(circuits, p, q)
        if len(circuit) == len(boxes) and len(circuits) == 1:
            # product of X coords is answer for part 2
            part2 = p[0] * q[0]
            break

    return part1, part2


def test_circuits():
    ex = """162,817,812
57,618,57
906,360,560
592,479,940
352,342,300
466,668,158
542,29,236
431,825,988
739,650,466
52,470,668
216,146,977
819,987,18
117,168,530
805,96,715
346,949,466
970,615,88
941,993,340
862,61,35
984,92,344
425,690,689"""
    assert (40, 25272) == longest_circuits(ex, 10)


if __name__ == "__main__":
    print(longest_circuits(data, 1000))
