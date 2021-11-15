#!/usr/bin/env python3
"""--- Day 17: Set and Forget ---

An early warning system detects an incoming solar flare and
automatically activates the ship's electromagnetic
shield. Unfortunately, this has cut off the Wi-Fi for many small
robots that, unaware of the impending danger, are now trapped on
exterior scaffolding on the unsafe side of the shield. To rescue them,
you'll have to act quickly!

The only tools at your disposal are some wired cameras and a small
vacuum robot currently asleep at its charging station. The video
quality is poor, but the vacuum robot has a needlessly bright LED that
makes it easy to spot no matter where it is.

An Intcode program, the Aft Scaffolding Control and Information
Interface (ASCII, your puzzle input), provides access to the cameras
and the vacuum robot. Currently, because the vacuum robot is asleep,
you can only access the cameras.

Running the ASCII program on your Intcode computer will provide the
current view of the scaffolds. This is output, purely coincidentally,
as ASCII code: 35 means #, 46 means ., 10 starts a new line of output
below the current one, and so on. (Within a line, characters are drawn
left-to-right.)

In the camera output, # represents a scaffold and . represents open
space. The vacuum robot is visible as ^, v, <, or > depending on
whether it is facing up, down, left, or right respectively. When drawn
like this, the vacuum robot is always on a scaffold; if the vacuum
robot ever walks off of a scaffold and begins tumbling through space
uncontrollably, it will instead be visible as X.

In general, the scaffold forms a path, but it sometimes loops back
onto itself. For example, suppose you can see the following view from
the cameras:

..#..........
..#..........
#######...###
#.#...#...#.#
#############
..#...#...#..
..#####...^..

Here, the vacuum robot, ^ is facing up and sitting at one end of the
scaffold near the bottom-right of the image. The scaffold continues
up, loops across itself several times, and ends at the top-left of the
image.

The first step is to calibrate the cameras by getting the alignment
parameters of some well-defined points. Locate all scaffold
intersections; for each, its alignment parameter is the distance
between its left edge and the left edge of the view multiplied by the
distance between its top edge and the top edge of the view. Here, the
intersections from the above image are marked O:

..#..........
..#..........
##O####...###
#.#...#...#.#
##O###O###O##
..#...#...#..
..#####...^..

For these intersections:

The top-left intersection is 2 units from the left of the image and 2
units from the top of the image, so its alignment parameter is 2 * 2 =
4.

The bottom-left intersection is 2 units from the left and 4 units from
the top, so its alignment parameter is 2 * 4 = 8.

The bottom-middle intersection is 6 from the left and 4 from the top,
so its alignment parameter is 24.

The bottom-right intersection's alignment parameter is 40.

To calibrate the cameras, you need the sum of the alignment
parameters. In the above example, this is 76.

Run your ASCII program. What is the sum of the alignment parameters
for the scaffold intersections?

--- Part Two ---

Now for the tricky part: notifying all the other robots about the
solar flare. The vacuum robot can do this automatically if it gets
into range of a robot. However, you can't see the other robots on the
camera, so you need to be thorough instead: you need to make the
vacuum robot visit every part of the scaffold at least once.

The vacuum robot normally wanders randomly, but there isn't time for
that today. Instead, you can override its movement logic with new
rules.

Force the vacuum robot to wake up by changing the value in your ASCII
program at address 0 from 1 to 2. When you do this, you will be
automatically prompted for the new movement rules that the vacuum
robot should use. The ASCII program will use input instructions to
receive them, but they need to be provided as ASCII code; end each
line of logic with a single newline, ASCII code 10.

First, you will be prompted for the main movement routine. The main
routine may only call the movement functions: A, B, or C. Supply the
movement functions to use as ASCII text, separating them with commas
(,, ASCII code 44), and ending the list with a newline (ASCII code
10). For example, to call A twice, then alternate between B and C
three times, provide the string A,A,B,C,B,C,B,C and then a newline.

Then, you will be prompted for each movement function. Movement
functions may use L to turn left, R to turn right, or a number to move
forward that many units. Movement functions may not call other
movement functions. Again, separate the actions with commas and end
the list with a newline. For example, to move forward 10 units, turn
left, move forward 8 units, turn right, and finally move forward 6
units, provide the string 10,L,8,R,6 and then a newline.

Finally, you will be asked whether you want to see a continuous video
feed; provide either y or n and a newline. Enabling the continuous
video feed can help you see what's going on, but it also requires a
significant amount of processing power, and may even cause your
Intcode computer to overheat.

Due to the limited amount of memory in the vacuum robot, the ASCII
definitions of the main routine and the movement functions may each
contain at most 20 characters, not counting the newline.

For example, consider the following camera feed:

#######...#####
#.....#...#...#
#.....#...#...#
......#...#...#
......#...###.#
......#.....#.#
^########...#.#
......#.#...#.#
......#########
........#...#..
....#########..
....#...#......
....#...#......
....#...#......
....#####......

In order for the vacuum robot to visit every part of the scaffold at
least once, one path it could take is:

R,8,R,8,R,4,R,4,R,8,L,6,L,2,R,4,R,4,R,8,R,8,R,8,L,6,L,2

Without the memory limit, you could just supply this whole string to
function A and have the main routine call A once. However, you'll need
to split it into smaller parts.

One approach is:

Main routine: A,B,C,B,A,C
(ASCII input: 65, 44, 66, 44, 67, 44, 66, 44, 65, 44, 67, 10)
Function A:   R,8,R,8
(ASCII input: 82, 44, 56, 44, 82, 44, 56, 10)
Function B:   R,4,R,4,R,8
(ASCII input: 82, 44, 52, 44, 82, 44, 52, 44, 82, 44, 56, 10)
Function C:   L,6,L,2
(ASCII input: 76, 44, 54, 44, 76, 44, 50, 10)

Visually, this would break the desired path into the following parts:

A,        B,            C,        B,            A,        C
R,8,R,8,  R,4,R,4,R,8,  L,6,L,2,  R,4,R,4,R,8,  R,8,R,8,  L,6,L,2

CCCCCCA...BBBBB
C.....A...B...B
C.....A...B...B
......A...B...B
......A...CCC.B
......A.....C.B
^AAAAAAAA...C.B
......A.A...C.B
......AAAAAA#AB
........A...C..
....BBBB#BBBB..
....B...A......
....B...A......
....B...A......
....BBBBA......

Of course, the scaffolding outside your ship is much more complex.

As the vacuum robot finds other robots and notifies them of the
impending solar flare, it also can't help but leave them squeaky
clean, collecting any space dust it finds. Once it finishes the
programmed set of movements, assuming it hasn't drifted off into
space, the cleaning robot will return to its docking station and
report the amount of space dust it collected as a large, non-ASCII
value in a single output instruction.

After visiting every part of the scaffold at least once, how much dust
does the vacuum robot report it has collected?
"""

import itertools
from aoc import *
from intcode import Intcode

# For my own sanity, swap the UP and DOWN tuples
UP, DOWN, LEFT, RIGHT = (0, -1), (0, 1), (-1, 0), (1, 0)

TURNS = {
    LEFT: {LEFT: DOWN, RIGHT: UP},
    RIGHT: {LEFT: UP, RIGHT: DOWN},
    UP: {LEFT: LEFT, RIGHT: RIGHT},
    DOWN: {LEFT: RIGHT, RIGHT: LEFT},
}

ROBOT = {"^": UP, "v": DOWN, "<": LEFT, ">": RIGHT}


def move(p, heading):
    return (X(p) + X(heading), Y(p) + Y(heading))


def pipe_neighbors(p, heading):
    return (move(p, TURNS[heading][LEFT]), move(p, TURNS[heading][RIGHT]))


def render(code):
    return ",".join(",".join(str(i) for i in tpl) for tpl in code)


def legal(code):
    return len(render(code)) <= 20


def replace(code, func, repl):
    result = []
    i = 0
    while i < len(code):
        if code[i : i + len(func)] == list(func):
            result.append(repl)
            i += len(func)
            continue
        result.append(code[i])
        i += 1
    return result


def compress(code):
    import string

    routines = []
    while any(c[0] in ("L", "R") for c in code):
        idx = next(idx for idx, c in enumerate(code) if c[0] in ("L", "R"))
        # Skip ahead 2 code-points and look for a repeat or an
        # subroutine call
        eidx = next(
            (
                x
                for x, c in enumerate(code[idx + 2 :], idx + 2)
                if c[0] not in ("L", "R") or c == code[idx]
            ),
            len(code),
        )
        func = code[idx:eidx]
        code = replace(code, func, (string.ascii_uppercase[len(routines)],))
        routines.append(func)
    assert len(routines) <= 3
    return (code, routines)


class Scaffold(Intcode):
    def __init__(self, tape, input=[], display=False):
        super(Scaffold, self).__init__(tape, input=input)
        self.pos_ = origin
        self.map_ = {}
        self.robot_ = None
        self.display_ = display

    def on_output(self):
        while len(self.output) > 1:
            self.output.pop(0)
        val = self.output[-1]
        if val > 127:
            return
        glyph = chr(val)
        if self.display_:
            print(glyph, end="")
        if glyph == "\n":
            if X(self.pos_) == 0:
                self.pos_ = origin
            else:
                self.pos_ = (0, Y(self.pos_) + 1)
            return
        self.map_[self.pos_] = glyph
        if glyph in "<>^v":
            self.robot_ = self.pos_
        self.pos_ = (X(self.pos_) + 1, Y(self.pos_))

    def intersections(self):
        for pos, glyph in self.map_.items():
            if glyph not in "#<>^v":
                continue
            if all(self.map_.get(n, "") in "#<>^v" for n in neighbors4(pos)):
                yield pos

    def get_path(self, debug=False):
        path = [self.robot_]
        code = []
        pos = self.robot_
        heading = ROBOT[self.map_[pos]]
        leg = 0
        turncode = None
        while True:
            assert pos in self.map_ and self.map_.get(pos) != "."
            if debug:
                print(
                    pos,
                    heading,
                    self.map_.get(pos),
                    leg,
                    move(pos, heading),
                    pipe_neighbors(pos, heading),
                )
            path.append(pos)
            fwd = move(pos, heading)
            if self.map_.get(fwd) == "#":
                leg = leg + 1
                pos = fwd
                continue
            if leg:
                assert turncode is not None
                code.append((turncode, leg))
            pn = pipe_neighbors(pos, heading)
            next_pipe = [
                p
                for p in pipe_neighbors(pos, heading)
                if p not in path and self.map_.get(p) == "#"
            ]
            if not next_pipe:
                break
            turn = LEFT if (next_pipe[0] == pipe_neighbors(pos, heading)[0]) else RIGHT
            heading = TURNS[heading][turn]
            turncode = "L" if turn == LEFT else "R"
            leg = 0
        return code


if __name__ == "__main__":
    tape = list(vector(Input(17).read().strip()))
    scaff = Scaffold(tape)
    scaff.run()
    print(sum(X(p) * Y(p) for p in scaff.intersections()))
    code = scaff.get_path()
    main, functions = compress(code)
    program = "\n".join(render(x) for x in [main] + functions) + "\nn\n"
    # print(program)
    input = [ord(x) for x in program]
    tape[0] = 2
    scaff = Scaffold(tape, input=input)
    scaff.run()
    print(scaff.output[-1])
