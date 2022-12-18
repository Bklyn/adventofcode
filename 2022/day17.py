#!/usr/bin/env python3
 
from aoc import *

def tetris(input, rocks=2022):
   shapes = [  # Bottom row first
      ['####'],
      ['.#.', '###', '.#.'],
      ['###', '..#', '..#'],
      ['#', '#', '#', '#'],
      ['##', '##']
   ]
   cavern = ['+-------+']

   def collides(shape, x, y):
      return any(
            cavern[y + dy][x + dx] not in '.@'
            and shape[dy][dx] == '#'
            for dy in range(len(shape))
            for dx in range(len(shape[0])))

   def paint(cav, shape, x, y, glyph='#'):
      for cy in range(len(cav)):
         if cy < y or cy >= y + len(shape):
            yield cav[cy]
            continue
         dy = cy - y
         line = list(cavern[cy])
         for dx in range(len(shape[dy])):
            if shape[dy][dx] == '#':
               line[x + dx] = glyph
         yield ''.join(line)

   def bottom(cav):
      peaks = [
         max([y for y in range(len(cav)) if cav[y][x] == '#'], default=0)
         for x in range(1, 8)
      ]
      return min(peaks, default=0)

   def draw(cav):
      print('\n'.join(reversed(cav)))

   gas_index = 0
   scrolled = 0
   height = 0
   for shape_index in range(rocks):
      shape = shapes[shape_index % len(shapes)]
      x, y = 3, height + 4
      add_lines = y + len(shape) + 1 - len(cavern)
      if add_lines:
         cavern.extend(['|.......|'] * add_lines)
      while True:
         # print(f"\033[2JRock falls from {x},{y} height={height}")
         # draw(list(paint(cavern, shape, x, y, '@')))
         gas = input[gas_index % len(input)]
         gas_index += 1
         dx = -1 if gas == '<' else 1
         # Check for collision with wall or fixed shape
         if not collides(shape, x + dx, y):
            # print(f"Jet of gas pushes rock {'left' if dx < 0 else 'right'}")
            x += dx
         else:
            # print(f"Jet of gas pushes rock {'left' if dx < 0 else 'right'} but nothing happens")
            pass
         if collides(shape, x, y - 1):
            # print("Rock falls one unit, causing it to come to rest")
            cavern = list(paint(cavern, shape, x, y, '#'))
            # draw(cavern)
            bot = min(
               max(y for y in range(1, len(cavern)))
               for x in range(1, 8)
               if cavern[y][x] == '#')
            height = max(height, y + len(shape) - 1)
            break
         y -= 1

   return height

assert tetris('>>><<><>><<<>><>>><<<>>><<<><<<>><>><<>>', 2022) ==  3068

print(tetris(Puzzle(day=17).input_data.strip()))

# print(tetris(Puzzle(day=17).input_data.strip(), 3168))