from aoc import *
import re

def monkey_map(input):
   M = list(input.splitlines())
   M, path = M[:-2], M[-1]
   path = [int(x) if x.isdigit() else x for x in re.split("([LR])", path)]
   LEFT, RIGHT, UP, DOWN = (-1, 0), (1, 0), (0, -1), (0, 1)
   GLYPH = {LEFT: '<', RIGHT: '>', UP: '^', DOWN: 'v'}
   TURNS = {
      (LEFT, 'L'): DOWN, (LEFT, 'R'): UP,
      (RIGHT, 'L'): UP, (RIGHT, 'R'): DOWN,
      (UP, 'L'): LEFT, (UP, 'R'): RIGHT,
      (DOWN, 'L'): RIGHT, (DOWN, 'R'): LEFT
   }
   def move(x, y, facing):
      while True:
         y = (y + Y(facing)) % len(M)
         x = (x + X(facing)) % len(M[y])
         if M[y][x] in '.#':
            break
      if M[y][x] == '.':
         return x, y

   facing = RIGHT
   x, y = M[0].index('.'), 0
   trace = {}
   for step in path:
      if type(step) is str:
         facing = TURNS[(facing, step)]
         continue
      for _ in range(step):
         tpl = move(x, y, facing)
         # print(f"{_+1}/{step}: {(x, y)} + {facing} -> {tpl}")
         if tpl is None:
            break
         trace[(x, y)] = GLYPH[facing]
         x, y = tpl

   for yy, row in enumerate(M):
      chars = [trace.get((xx, yy), c) for xx, c in enumerate(row)]
      print(f"{yy+1:4} {''.join(chars)}")
   return 1000 * (y + 1) + 4 * (x + 1) + {RIGHT: 0, DOWN: 1, LEFT: 2, UP: 3}[facing]

p = Puzzle(year=2022, day=22)
assert monkey_map(p.example_data) == 6032

monkey_map(p.input_data)
