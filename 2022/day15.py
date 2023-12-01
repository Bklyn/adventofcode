#!/usr/bin/env python3
 
from aoc import *

p = Puzzle(day=15)

def impact(s, d, row):
   dist = abs(row - Y(s))
   delta = d - dist
   if delta < 0:
      return None
   return (X(s) - delta, X(s) + delta)
   
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
   
def beacons(input, row):
   sensors = dict()
   beacons = set()
   for line in input.splitlines():
      m = re.match(r'Sensor at x=([^,]+), y=([^:]+): closest beacon is at x=([^,]+), y=(.+)', line)
      assert m
      s = tuple(int(x) for x in m.groups()[:2])
      b = tuple(int(x) for x in m.groups()[2:])
      d = cityblock_distance(s, b)
      sensors[s] = d
      beacons.add(b)
   impacts = list(overlap(
      x for x in (impact(s, sensors[s], row) for s in sensors)
      if x is not None))
   coverage = (
      sum(y - x + 1 for x, y in impacts) -
      sum(1 for b in beacons if b[1] == row) -
      sum(1 for s in sensors if s[1] == row)
   )
   # Find beacon location.  This is slow and I'm not sure how to speed it up
   prev = None
   for y in range(4000000 + 1):
      impacts = list(overlap(
         x for x in (impact(s, sensors[s], y) for s in sensors)
         if x is not None))
      if len(impacts) > 1:
         print(prev)
         print(impacts)
         freq = 4000000 * (impacts[0][1] + 1) + y
         break
      prev = impacts
   return coverage, freq

assert beacons(p.example_data, 10) == (26, 56000011)

print(beacons(p.input_data, 2000000))