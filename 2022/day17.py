#!/usr/bin/env python3
 
from aoc import *

def tetris(input, rocks=2022, debug=False):
   shapes = [  # Bottom row first
      ['####'],
      ['.#.', '###', '.#.'],
      ['###', '..#', '..#'],
      ['#', '#', '#', '#'],
      ['##', '##']
   ]
   cavern = []

   def collides(cavern, shape, x, y):
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

   def window(cav):
      peaks = [
         max([y for y in range(len(cav)) if cav[y][x] == '#'], default=0)
         for x in range(1, 8)
      ]
      bottom = max([y for y in range(len(cav)) if cav[y][1:8] == '#######'], default=0)
      # return min(peaks, default=0), max(peaks, default=0)
      return bottom, max(peaks, default=0)

   def draw(cav, offset=0):
      for y in reversed(range(len(cav))):
         print(f"{y+offset:>4} {cav[y]}")

   gas_index = 0
   scrolled = 0
   height = 0
   cavern = ['+-------+']
   seen = {}
   scores = []

   assert window(cavern) == (0, 0)
   logged = 1

   for shape_index in range(rocks):
      shape = shapes[shape_index % len(shapes)]
      if shape_index == logged * 10:
         print(f"Shape #{shape_index}: height={height} scrolled={scrolled} seen={len(seen)} scores={len(scores)}")
         logged = shape_index
      x, y = 3, height + 4
      add_lines = y + len(shape) - len(cavern)
      if add_lines:
         cavern.extend(['|.......|'] * add_lines)
      while True:
         gas = input[gas_index % len(input)]
         gas_index += 1
         dx = -1 if gas == '<' else 1
         # Check for collision with wall or fixed shape
         if not collides(cavern, shape, x + dx, y):
            x += dx
         if collides(cavern, shape, x, y - 1):
            cavern = list(paint(cavern, shape, x, y, '#'))
            bottom, top = window(cavern)
            assert top == max(height, y + len(shape) - 1)
            height = top
            # print(f"Shape #{shape_index}: height={height} scrolled={scrolled} bottom={bottom} shape={shape} period={len(input) * len(shapes)}")
            if bottom > 1:
               rep = '\n'.join(cavern)
               state = (shape_index, bottom, top, scrolled, top + scrolled)
               if (prev := seen.get(rep)) is not None:
                  period = state[0] - prev[0]
                  cycles = rocks // period
                  remainder = rocks % period
                  print(f"{shape_index}: period={period} cycles={cycles} remainder={remainder} scores={len(scores)}")
                  assert len(scores) > remainder
                  score = cycles * (state[-1] - prev[-1]) + scores[remainder-1]
                  print(f"Shape #{shape_index}: have seen this state before: {prev} -> {state}: period={period} "
                     f"cycles={cycles} remainder={remainder} scores[{remainder}]={scores[remainder]} total={score}")
                  for i in range(prev[0]):
                     print(f"scores[{i}]={scores[i]}")
                  return score
               seen[rep] = state
               scrolled += bottom
               height -= bottom 
               cavern = [cavern[0]] + cavern[bottom+1:]
               if debug > 1:
                  print(f"> Shape #{shape_index}: height={height} scrolled={scrolled}")
                  draw(cavern)

            scores.append(height + scrolled)
            break
         y -= 1

   if debug:
      print(f"Shape #{shape_index}: height={height} scrolled={scrolled} bottom={bottom} shape={shape}")
      draw(cavern, scrolled)
   return height + scrolled


ex18 = '>>><<><>><<<>><>>><<<>>><<<><<<>><>><<>>'
assert tetris(ex18, 2022) ==  3068
# assert tetris(ex18, 10**12) == 1514285714288

print(tetris(Puzzle(day=17).input_data.strip(), 2022))
print(tetris(Puzzle(day=17).input_data.strip(), 10**12))