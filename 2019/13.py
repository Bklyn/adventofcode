#!/usr/bin/env python3
"""--- Day 13: Care Package ---

As you ponder the solitude of space and the ever-increasing three-hour
roundtrip for messages between you and Earth, you notice that the
Space Mail Indicator Light is blinking. To help keep you sane, the
Elves have sent you a care package.

It's a new game for the ship's arcade cabinet! Unfortunately, the
arcade is all the way on the other end of the ship. Surely, it won't
be hard to build your own - the care package even comes with
schematics.

The arcade cabinet runs Intcode software like the game the Elves sent
(your puzzle input). It has a primitive screen capable of drawing
square tiles on a grid. The software draws tiles to the screen with
output instructions: every three output instructions specify the x
position (distance from the left), y position (distance from the top),
and tile id. The tile id is interpreted as follows:

0 is an empty tile. No game object appears in this tile.
1 is a wall tile. Walls are indestructible barriers.
2 is a block tile. Blocks can be broken by the ball.
3 is a horizontal paddle tile. The paddle is indestructible.
4 is a ball tile. The ball moves diagonally and bounces off objects.

For example, a sequence of output values like 1,2,3,6,5,4 would draw a
horizontal paddle tile (1 tile from the left and 2 tiles from the top)
and a ball tile (6 tiles from the left and 5 tiles from the top).

Start the game. How many block tiles are on the screen when the game exits?

--- Part Two ---

The game didn't run because you didn't put in any
quarters. Unfortunately, you did not bring any quarters. Memory
address 0 represents the number of quarters that have been inserted;
set it to 2 to play for free.

The arcade cabinet has a joystick that can move left and right. The
software reads the position of the joystick with input instructions:

If the joystick is in the neutral position, provide 0.
If the joystick is tilted to the left, provide -1.
If the joystick is tilted to the right, provide 1.

The arcade cabinet also has a segment display capable of showing a
single number that represents the player's current score. When three
output instructions specify X=-1, Y=0, the third output instruction is
not a tile; the value instead specifies the new score to show in the
segment display. For example, a sequence of output values like
-1,0,12345 would show 12345 as the player's current score.

Beat the game by breaking all the blocks. What is your score after the
last block is broken?
"""

from aoc import *
from intcode import Intcode
import random

class Game(Intcode):
    score_ = 0
    ball_ = None
    dir_ = None
    paddle_ = None

    def __init__(self, tape):
        super(Game, self).__init__(tape, input=[])
        self.tiles_ = {}

    def screen(self):
        return self.tiles_

    def blocks(self):
        return sum(t == 2 for t in self.tiles_.values())

    def display(self):
        b  = self.blocks()
        # print ("SCORE: {} BLOCKS: {} BALL: {} PDL: {}".format(self.score_, b, self.ball_, self.paddle_))
        if b == 0:
            self.done_ = True
        return b

    def on_input(self):
        if self.display() == 0:
            return None
        dx = X(self.ball_) - X(self.paddle_)
        return 1 if dx > 0 else -1 if dx < 0 else 0

    def on_output(self):
        if len(self.output) % 3:
            return
        x, y, tile = self.output[-3:]
        if x == -1 and y == 0:
            self.score_ = tile
            self.display()
            return
        self.tiles_[(x,y)] = tile
        if tile == 3:
            self.paddle_ = (x,y)
        if tile == 4:
            self.ball_ = (x, y)

if __name__ == "__main__":
    tape = list(vector(Input(13).read()))
    game = Game(tape)
    game.run()
    print (len([b for b in game.screen().values() if b == 2]))
    tape[0] = 2
    game = Game(tape)
    game.run()
    print(game.score_)
