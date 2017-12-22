#!/usr/bin/env python3
'''--- Day 22: Sporifica Virus ---

Diagnostics indicate that the local grid computing cluster has been
contaminated with the Sporifica Virus. The grid computing cluster is a
seemingly-infinite two-dimensional grid of compute nodes. Each node is
either clean or infected by the virus.

To prevent overloading the nodes (which would render them useless to
the virus) or detection by system administrators, exactly one virus
carrier moves through the network, infecting or cleaning nodes as it
moves. The virus carrier is always located on a single node in the
network (the current node) and keeps track of the direction it is
facing.

To avoid detection, the virus carrier works in bursts; in each burst,
it wakes up, does some work, and goes back to sleep. The following
steps are all executed in order one time each burst:

* If the current node is infected, it turns to its right. Otherwise,
  it turns to its left. (Turning is done in-place; the current node
  does not change.)

* If the current node is clean, it becomes infected. Otherwise, it
  becomes cleaned. (This is done after the node is considered for the
  purposes of changing direction.)

* The virus carrier moves forward one node in the direction it is
  facing.

Diagnostics have also provided a map of the node infection status
(your puzzle input). Clean nodes are shown as .; infected nodes are
shown as #. This map only shows the center of the grid; there are many
more nodes beyond those shown, but none of them are currently
infected.

The virus carrier begins in the middle of the map facing up.

For example, suppose you are given a map like this:

..#
#..
...

Then, the middle of the infinite grid looks like this, with the virus carrier's position marked with [ ]:

. . . . . . . . .
. . . . . . . . .
. . . . . . . . .
. . . . . # . . .
. . . #[.]. . . .
. . . . . . . . .
. . . . . . . . .
. . . . . . . . .

The virus carrier is on a clean node, so it turns left, infects the node, and moves left:

. . . . . . . . .
. . . . . . . . .
. . . . . . . . .
. . . . . # . . .
. . .[#]# . . . .
. . . . . . . . .
. . . . . . . . .
. . . . . . . . .

The virus carrier is on an infected node, so it turns right, cleans the node, and moves up:

. . . . . . . . .
. . . . . . . . .
. . . . . . . . .
. . .[.]. # . . .
. . . . # . . . .
. . . . . . . . .
. . . . . . . . .
. . . . . . . . .

Four times in a row, the virus carrier finds a clean, infects it,
turns left, and moves forward, ending in the same place and still
facing up:

. . . . . . . . .
. . . . . . . . .
. . . . . . . . .
. . #[#]. # . . .
. . # # # . . . .
. . . . . . . . .
. . . . . . . . .
. . . . . . . . .

Now on the same node as before, it sees an infection, which causes it to turn right, clean the node, and move forward:

. . . . . . . . .
. . . . . . . . .
. . . . . . . . .
. . # .[.]# . . .
. . # # # . . . .
. . . . . . . . .
. . . . . . . . .
. . . . . . . . .

After the above actions, a total of 7 bursts of activity had taken
place. Of them, 5 bursts of activity caused an infection.

After a total of 70, the grid looks like this, with the virus carrier
facing up:

. . . . . # # . .
. . . . # . . # .
. . . # . . . . #
. . # . #[.]. . #
. . # . # . . # .
. . . . . # # . .
. . . . . . . . .
. . . . . . . . .

By this time, 41 bursts of activity caused an infection (though most
of those nodes have since been cleaned).

After a total of 10000 bursts of activity, 5587 bursts will have
caused an infection.

Given your actual map, after 10000 bursts of activity, how many bursts
cause a node to become infected? (Do not count nodes that begin
infected.)

--- Part Two ---

As you go to remove the virus from the infected nodes, it evolves to
resist your attempt.

Now, before it infects a clean node, it will weaken it to disable your
defenses. If it encounters an infected node, it will instead flag the
node to be cleaned in the future. So:

Clean nodes become weakened.
Weakened nodes become infected.
Infected nodes become flagged.
Flagged nodes become clean.

Every node is always in exactly one of the above states.

The virus carrier still functions in a similar way, but now uses the following logic during its bursts of action:

Decide which way to turn based on the current node:

If it is clean, it turns left.
If it is weakened, it does not turn, and will continue moving in the same direction.
If it is infected, it turns right.
If it is flagged, it reverses direction, and will go back the way it came.

Modify the state of the current node, as described above.

The virus carrier moves forward one node in the direction it is facing.

Start with the same map (still using . for clean and # for infected)
and still with the virus carrier starting in the middle and facing up.

Using the same initial state as the previous example, and drawing
weakened as W and flagged as F, the middle of the infinite grid looks
like this, with the virus carrier's position again marked with [ ]:

. . . . . . . . .
. . . . . . . . .
. . . . . . . . .
. . . . . # . . .
. . . #[.]. . . .
. . . . . . . . .
. . . . . . . . .
. . . . . . . . .
This is the same as before, since no initial nodes are weakened or flagged. The virus carrier is on a clean node, so it still turns left, instead weakens the node, and moves left:

. . . . . . . . .
. . . . . . . . .
. . . . . . . . .
. . . . . # . . .
. . .[#]W . . . .
. . . . . . . . .
. . . . . . . . .
. . . . . . . . .
The virus carrier is on an infected node, so it still turns right, instead flags the node, and moves up:

. . . . . . . . .
. . . . . . . . .
. . . . . . . . .
. . .[.]. # . . .
. . . F W . . . .
. . . . . . . . .
. . . . . . . . .
. . . . . . . . .
This process repeats three more times, ending on the previously-flagged node and facing right:

. . . . . . . . .
. . . . . . . . .
. . . . . . . . .
. . W W . # . . .
. . W[F]W . . . .
. . . . . . . . .
. . . . . . . . .
. . . . . . . . .
Finding a flagged node, it reverses direction and cleans the node:

. . . . . . . . .
. . . . . . . . .
. . . . . . . . .
. . W W . # . . .
. .[W]. W . . . .
. . . . . . . . .
. . . . . . . . .
. . . . . . . . .
The weakened node becomes infected, and it continues in the same direction:

. . . . . . . . .
. . . . . . . . .
. . . . . . . . .
. . W W . # . . .
.[.]# . W . . . .
. . . . . . . . .
. . . . . . . . .
. . . . . . . . .

Of the first 100 bursts, 26 will result in infection. Unfortunately,
another feature of this evolved virus is speed; of the first 10000000
bursts, 2511944 will result in infection.

Given your actual map, after 10000000 bursts of activity, how many
bursts cause a node to become infected? (Do not count nodes that begin
infected.)
'''

from aoc2017 import Input

UP, DOWN, LEFT, RIGHT = (0, -1), (0, 1), (-1, 0), (1, 0)

Turns = {UP:   [LEFT, RIGHT], LEFT:  [DOWN, UP],
         DOWN: [RIGHT, LEFT], RIGHT: [UP, DOWN]}


def turn(dir, state):
    if state == '#':
        return Turns[dir][1]
    elif state == 'W':
        return dir
    elif state == '.':
        return Turns[dir][0]
    elif state == 'F':
        return (-dir[0], -dir[1])
    assert False


def make_dict(m):
    result = {(x, y): m[y][x]
              for y in range(len(m))
              for x in range(len(m[y]))}
    assert len(result) == len(m)**2
    return result


def print_map(d, pos=None):
    exes, whys = ([x for x, _ in d.keys()],
                  [y for _, y in d.keys()])
    x_range = (min(exes), max(exes))
    y_range = (min(whys), max(whys))
    # print (x_range, y_range)
    for y in range(y_range[0], y_range[1] + 1):
        row = []
        for x in range(x_range[0], x_range[1] + 1):
            fmt = '[{}]' if pos == (x, y) else ' {} '
            row.append(fmt.format(d.get((x, y), '.')))
        print(''.join(row))


def virus(m, turns, transitions, dump=False):
    pos = (len(m) // 2, len(m) // 2)
    m = make_dict(m)
    dir = UP
    num_infected = 0
    for i in range(turns):
        state = m.get(pos, '.')
        dir = turn(dir, state)
        m[pos] = newstate = transitions[state]
        if newstate == '#':
            num_infected += 1
        pos = (pos[0] + dir[0], pos[1] + dir[1])
    if dump:
        print_map(m, pos)
    return num_infected


Part1 = {'#': '.', '.': '#'}
Part2 = {'.': 'W', 'W': '#', '#': 'F', 'F': '.'}

assert virus([list('..#'), list('#..'), list('...')], 70, Part1) == 41
assert virus([list('..#'), list('#..'), list('...')], 10000, Part1) == 5587
# Slow:
# assert virus([list('..#'), list('#..'), list('...')], 10**7, Part2) ==
# 2511944

Map = [
    [x for x in line.strip()]
    for line in Input(22)]

print(virus(Map, 10000, Part1))
print(virus(Map, 10**7, Part2))
