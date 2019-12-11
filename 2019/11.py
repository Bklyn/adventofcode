#!/usr/bin/env python3
"""--- Day 11: Space Police ---

On the way to Jupiter, you're pulled over by the Space Police.

"Attention, unmarked spacecraft! You are in violation of Space Law!
All spacecraft must have a clearly visible registration identifier!
You have 24 hours to comply or be sent to Space Jail!"

Not wanting to be sent to Space Jail, you radio back to the Elves on
Earth for help. Although it takes almost three hours for their reply
signal to reach you, they send instructions for how to power up the
emergency hull painting robot and even provide a small Intcode program
(your puzzle input) that will cause it to paint your ship
appropriately.

There's just one problem: you don't have an emergency hull painting
robot.

You'll need to build a new emergency hull painting robot. The robot
needs to be able to move around on the grid of square panels on the
side of your ship, detect the color of its current panel, and paint
its current panel black or white. (All of the panels are currently
black.)

The Intcode program will serve as the brain of the robot. The program
uses input instructions to access the robot's camera: provide 0 if the
robot is over a black panel or 1 if the robot is over a white
panel. Then, the program will output two values:

First, it will output a value indicating the color to paint the panel
the robot is over: 0 means to paint the panel black, and 1 means to
paint the panel white.

Second, it will output a value indicating the direction the robot
should turn: 0 means it should turn left 90 degrees, and 1 means it
should turn right 90 degrees.

After the robot turns, it should always move forward exactly one
panel. The robot starts facing up.

The robot will continue running for a while like this and halt when it
is finished drawing. Do not restart the Intcode computer inside the
robot during this process.

For example, suppose the robot is about to start running. Drawing
black panels as ., white panels as #, and the robot pointing the
direction it is facing (< ^ > v), the initial state and region near
the robot looks like this:

.....
.....
..^..
.....
.....

The panel under the robot (not visible here because a ^ is shown
instead) is also black, and so any input instructions at this point
should be provided 0. Suppose the robot eventually outputs 1 (paint
white) and then 0 (turn left). After taking these actions and moving
forward one panel, the region now looks like this:

.....
.....
.<#..
.....
.....

Input instructions should still be provided 0. Next, the robot might
output 0 (paint black) and then 0 (turn left):

.....
.....
..#..
.v...
.....

After more outputs (1,0, 1,0):

.....
.....
..^..
.##..
.....

The robot is now back where it started, but because it is now on a
white panel, input instructions should be provided 1. After several
more outputs (0,1, 1,0, 1,0), the area looks like this:

.....
..<#.
...#.
.##..
.....

Before you deploy the robot, you should probably have an estimate of
the area it will cover: specifically, you need to know the number of
panels it paints at least once, regardless of color. In the example
above, the robot painted 6 panels at least once. (It painted its
starting panel twice, but that panel is still only counted once; it
also never painted the panel it ended on.)

Build a new emergency hull painting robot and run the Intcode program
on it. How many panels does it paint at least once?
"""

from aoc import *
from intcode import Intcode

TURNS = {UP: (LEFT, RIGHT), RIGHT: (UP, DOWN), DOWN: (RIGHT, LEFT), LEFT: (DOWN, UP)}


def Turn(direction, turn):
    return TURNS[direction][turn]


class Robot(Intcode):
    pos_ = origin
    direction_ = UP

    def __init__(self, tape, hull={}):
        super(Robot, self).__init__(tape, input=[])
        self.hull_ = hull

    def hull(self):
        return self.hull_

    def on_input(self):
        return self.hull_.get(self.pos_, 0)

    def on_output(self):
        if len(self.output) % 2:
            return
        color, turn = self.output[-2:]
        assert color in (0, 1) and turn in (0, 1)
        # paint, turn, move
        self.hull_[self.pos_] = color
        self.direction_ = Turn(self.direction_, turn)
        self.pos_ = (
            X(self.pos_) + X(self.direction_),
            Y(self.pos_) + Y(self.direction_),
        )


if __name__ == "__main__":
    tape = list(vector(Input(11).read()))
    # Part 1
    robot = Robot(tape)
    robot.run()
    print(len(robot.hull()))

    # Part 2: first square is white
    robot = Robot(tape, hull={origin: 1})
    robot.run()
    image = [k for k, v in robot.hull().items() if v]
    minx = min(X(p) for p in image)
    maxx = max(X(p) for p in image)
    miny = min(Y(p) for p in image)
    maxy = max(Y(p) for p in image)
    # Output from top to bottom (Y is reversed)
    for y in reversed(range(miny, maxy + 1)):
        print("".join("#" if (x, y) in image else " " for x in range(minx, maxx + 1)))
