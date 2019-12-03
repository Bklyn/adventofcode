#!/usr/bin/env python3
'''--- Day 15: Beverage Bandits ---

Having perfected their hot chocolate, the Elves have a new problem:
the Goblins that live in these caves will do anything to steal
it. Looks like they're here for a fight.

You scan the area, generating a map of the walls (#), open cavern (.),
and starting position of every Goblin (G) and Elf (E) (your puzzle
input).

Combat proceeds in rounds; in each round, each unit that is still
alive takes a turn, resolving all of its actions before the next
unit's turn begins. On each unit's turn, it tries to move into range
of an enemy (if it isn't already) and then attack (if it is in range).

All units are very disciplined and always follow very strict combat
rules. Units never move or attack diagonally, as doing so would be
dishonorable. When multiple choices are equally valid, ties are broken
in reading order: top-to-bottom, then left-to-right. For instance, the
order in which units take their turns within a round is the reading
order of their starting positions in that round, regardless of the
type of unit or whether other units have moved after the round
started. For example:

                 would take their
These units:   turns in this order:
  #######           #######
  #.G.E.#           #.1.2.#
  #E.G.E#           #3.4.5#
  #.G.E.#           #.6.7.#
  #######           #######

Each unit begins its turn by identifying all possible targets (enemy
units). If no targets remain, combat ends.

Then, the unit identifies all of the open squares (.) that are in
range of each target; these are the squares which are adjacent
(immediately up, down, left, or right) to any target and which aren't
already occupied by a wall or another unit. Alternatively, the unit
might already be in range of a target. If the unit is not already in
range of a target, and there are no open squares which are in range of
a target, the unit ends its turn.

If the unit is already in range of a target, it does not move, but
continues its turn with an attack. Otherwise, since it is not in range
of a target, it moves.

To move, the unit first considers the squares that are in range and
determines which of those squares it could reach in the fewest
steps. A step is a single movement to any adjacent (immediately up,
down, left, or right) open (.) square. Units cannot move into walls or
other units. The unit does this while considering the current
positions of units and does not do any prediction about where units
will be later. If the unit cannot reach (find an open path to) any of
the squares that are in range, it ends its turn. If multiple squares
are in range and tied for being reachable in the fewest steps, the
step which is first in reading order is chosen. For example:

Targets:      In range:     Reachable:    Nearest:      Chosen:
#######       #######       #######       #######       #######
#E..G.#       #E.?G?#       #E.@G.#       #E.!G.#       #E.+G.#
#...#.#  -->  #.?.#?#  -->  #.@.#.#  -->  #.!.#.#  -->  #...#.#
#.G.#G#       #?G?#G#       #@G@#G#       #!G.#G#       #.G.#G#
#######       #######       #######       #######       #######

In the above scenario, the Elf has three targets (the three Goblins):

Each of the Goblins has open, adjacent squares which are in range
(marked with a ? on the map).

Of those squares, four are reachable (marked @); the other two (on the
right) would require moving through a wall or unit to reach.

Three of these reachable squares are nearest, requiring the fewest
steps (only 2) to reach (marked !).

Of those, the square which is first in reading order is chosen (+).

The unit then takes a single step toward the chosen square along the
shortest path to that square. If multiple steps would put the unit
equally closer to its destination, the unit chooses the step which is
first in reading order. (This requires knowing when there is more than
one shortest path so that you can consider the first step of each such
path.) For example:

In range:     Nearest:      Chosen:       Distance:     Step:
#######       #######       #######       #######       #######
#.E...#       #.E...#       #.E...#       #4E212#       #..E..#
#...?.#  -->  #...!.#  -->  #...+.#  -->  #32101#  -->  #.....#
#..?G?#       #..!G.#       #...G.#       #432G2#       #...G.#
#######       #######       #######       #######       #######

The Elf sees three squares in range of a target (?), two of which are
nearest (!), and so the first in reading order is chosen (+). Under
"Distance", each open square is marked with its distance from the
destination square; the two squares to which the Elf could move on
this turn (down and to the right) are both equally good moves and
would leave the Elf 2 steps from being in range of the Goblin. Because
the step which is first in reading order is chosen, the Elf moves
right one square.

Here's a larger example of movement:

Initially:
#########
#G..G..G#
#.......#
#.......#
#G..E..G#
#.......#
#.......#
#G..G..G#
#########

After 1 round:
#########
#.G...G.#
#...G...#
#...E..G#
#.G.....#
#.......#
#G..G..G#
#.......#
#########

After 2 rounds:
#########
#..G.G..#
#...G...#
#.G.E.G.#
#.......#
#G..G..G#
#.......#
#.......#
#########

After 3 rounds:
#########
#.......#
#..GGG..#
#..GEG..#
#G..G...#
#......G#
#.......#
#.......#
#########

Once the Goblins and Elf reach the positions above, they all are
either in range of a target or cannot find any square in range of a
target, and so none of the units can move until a unit dies.

After moving (or if the unit began its turn in range of a target), the
unit attacks.

To attack, the unit first determines all of the targets that are in
range of it by being immediately adjacent to it. If there are no such
targets, the unit ends its turn. Otherwise, the adjacent target with
the fewest hit points is selected; in a tie, the adjacent target with
the fewest hit points which is first in reading order is selected.

The unit deals damage equal to its attack power to the selected
target, reducing its hit points by that amount. If this reduces its
hit points to 0 or fewer, the selected target dies: its square becomes
. and it takes no further turns.

Each unit, either Goblin or Elf, has 3 attack power and starts with
200 hit points.

For example, suppose the only Elf is about to attack:

       HP:            HP:
G....  9       G....  9
..G..  4       ..G..  4
..EG.  2  -->  ..E..
..G..  2       ..G..  2
...G.  1       ...G.  1

The "HP" column shows the hit points of the Goblin to the left in the
corresponding row. The Elf is in range of three targets: the Goblin
above it (with 4 hit points), the Goblin to its right (with 2 hit
points), and the Goblin below it (also with 2 hit points). Because
three targets are in range, the ones with the lowest hit points are
selected: the two Goblins with 2 hit points each (one to the right of
the Elf and one below the Elf). Of those, the Goblin first in reading
order (the one to the right of the Elf) is selected. The selected
Goblin's hit points (2) are reduced by the Elf's attack power (3),
reducing its hit points to -1, killing it.

After attacking, the unit's turn ends. Regardless of how the unit's
turn ends, the next unit in the round takes its turn. If all units
have taken turns in this round, the round ends, and a new round
begins.

The Elves look quite outnumbered. You need to determine the outcome of
the battle: the number of full rounds that were completed (not
counting the round in which combat ends) multiplied by the sum of the
hit points of all remaining units at the moment combat ends. (Combat
only ends when a unit finds no targets during its turn.)

Below is an entire sample combat. Next to each map, each row's units'
hit points are listed from left to right.

Initially:
#######
#.G...#   G(200)
#...EG#   E(200), G(200)
#.#.#G#   G(200)
#..G#E#   G(200), E(200)
#.....#
#######

After 1 round:
#######
#..G..#   G(200)
#...EG#   E(197), G(197)
#.#G#G#   G(200), G(197)
#...#E#   E(197)
#.....#
#######

After 2 rounds:
#######
#...G.#   G(200)
#..GEG#   G(200), E(188), G(194)
#.#.#G#   G(194)
#...#E#   E(194)
#.....#
#######

Combat ensues; eventually, the top Elf dies:

After 23 rounds:
#######
#...G.#   G(200)
#..G.G#   G(200), G(131)
#.#.#G#   G(131)
#...#E#   E(131)
#.....#
#######

After 24 rounds:
#######
#..G..#   G(200)
#...G.#   G(131)
#.#G#G#   G(200), G(128)
#...#E#   E(128)
#.....#
#######

After 25 rounds:
#######
#.G...#   G(200)
#..G..#   G(131)
#.#.#G#   G(125)
#..G#E#   G(200), E(125)
#.....#
#######

After 26 rounds:
#######
# G....#   G(200)
#.G...#   G(131)
#.#.#G#   G(122)
#...#E#   E(122)
#..G..#   G(200)
#######

After 27 rounds:
#######
# G....#   G(200)
#.G...#   G(131)
#.#.#G#   G(119)
#...#E#   E(119)
#...G.#   G(200)
#######

After 28 rounds:
#######
# G....#   G(200)
#.G...#   G(131)
#.#.#G#   G(116)
#...#E#   E(113)
#....G#   G(200)
#######

More combat ensues; eventually, the bottom Elf dies:

After 47 rounds:
#######
# G....#   G(200)
#.G...#   G(131)
#.#.#G#   G(59)
#...#.#
#....G#   G(200)
#######

Before the 48th round can finish, the top-left Goblin finds that there
are no targets remaining, and so combat ends. So, the number of full
rounds that were completed is 47, and the sum of the hit points of all
remaining units is 200+131+59+200 = 590. From these, the outcome of
the battle is 47 * 590 = 27730.

Here are a few example summarized combats:

#######       #######
# G..#E#       #...#E#   E(200)
# E#E.E#       #E#...#   E(197)
# G.##.#  -->  #.E##.#   E(185)
#...#E#       #E..#E#   E(200), E(200)
#...E.#       #.....#
#######       #######

Combat ends after 37 full rounds
Elves win with 982 total hit points left
Outcome: 37 * 982 = 36334

#######       #######
# E..EG#       #.E.E.#   E(164), E(197)
#.#G.E#       #.#E..#   E(200)
# E.##E#  -->  #E.##.#   E(98)
# G..#.#       #.E.#.#   E(200)
#..E#.#       #...#.#
#######       #######

Combat ends after 46 full rounds
Elves win with 859 total hit points left
Outcome: 46 * 859 = 39514

#######       #######
# E.G#.#       #G.G#.#   G(200), G(98)
#.#G..#       #.#G..#   G(200)
#G.#.G#  -->  #..#..#
# G..#.#       #...#G#   G(95)
#...E.#       #...G.#   G(200)
#######       #######

Combat ends after 35 full rounds
Goblins win with 793 total hit points left
Outcome: 35 * 793 = 27755

#######       #######
#.E...#       #.....#
#.#..G#       #.#G..#   G(200)
#.###.#  -->  #.###.#
#E#G#G#       #.#.#.#
#...#G#       #G.G#G#   G(98), G(38), G(200)
#######       #######

Combat ends after 54 full rounds
Goblins win with 536 total hit points left
Outcome: 54 * 536 = 28944

#########       #########
# G......#       #.G.....#   G(137)
#.E.#...#       #G.G#...#   G(200), G(200)
#..##..G#       #.G##...#   G(200)
#...##..#  -->  #...##..#
#...#...#       #.G.#...#   G(200)
#.G...G.#       #.......#
#.....G.#       #.......#
#########       #########

Combat ends after 20 full rounds
Goblins win with 937 total hit points left
Outcome: 20 * 937 = 18740

What is the outcome of the combat described in your puzzle input?
'''

# Wow, long one!

from aoc2018 import *
import logging
import sys
import collections

logging.basicConfig(
    format='%(asctime)s [%(levelname)s] %(message)s', level=logging.DEBUG, stream=sys.stdout)


def sort_key(pos):
    # Need to sort top-to-bottom, left to right
    return ((Y(pos), X(pos)))


def parse(lines):
    if isinstance(lines, str):
        lines = lines.splitlines()
    dungeon = [[c for c in line.rstrip()] for line in lines]
    units = {}
    for row in range(len(dungeon)):
        for col in range(len(dungeon[row])):
            pos = (col, row)
            c = dungeon[row][col]
            if c in ('E', 'G'):
                units[pos] = (c, 200, len(units) + 1)
                dungeon[row][col] = '.'
    return dungeon, units


def find_path(start, finish, dungeon, units):
    assert finish not in units

    def valid_moves(pos):
        for move in neighbors4(pos):
            x, y = move
            if move not in units and dungeon[y][x] == '.':
                yield move
    for path in bfs(start, valid_moves, {finish}):
        yield path


def find_move(position, targets, dungeon, units):
    visiting = collections.deque([(position, 0)])
    meta = {position: (0, None)}
    seen = set()

    def valid_moves(pos):
        for move in neighbors4(pos):
            x, y = move
            if move not in units and dungeon[y][x] == '.':
                yield move

    while visiting:
        pos, dist = visiting.popleft()
        for nb in valid_moves(pos):
            if nb not in meta or meta[nb] > (dist + 1, pos):
                meta[nb] = (dist + 1, pos)
            if nb in seen:
                continue
            if not any(nb == visit[0] for visit in visiting):
                visiting.append((nb, dist + 1))
        seen.add(pos)

    try:
        min_dist, closest = min(
            (dist, pos) for pos, (dist, parent) in meta.items() if pos in targets)
    except ValueError:
        return

    logging.debug('{}: min={} closest={}'.format(position, min_dist, closest))
    while meta[closest][0] > 1:
        closest = meta[closest][1]

    return closest


def open_spaces(pos, dungeon, units):
    for move in neighbors4(pos):
        x, y = move
        if move not in units and dungeon[y][x] == '.':
            yield move


def weakest_neighbor(pos, opponents):
    # Find weakest opponent in range.  Returns None if nothing is in
    # range
    score = BIG
    weakest = None
    for move in neighbors4(pos):
        if move not in opponents:
            continue
        hp = opponents[move][1]
        # neighbors4 should return points in "reading" order, so
        # we do not need tiebreak logic
        if hp < score:
            score = hp
            weakest = move
    return weakest


def dump(dungeon, units):
    for div in (10, 1):
        for idx in range(len(dungeon[0])):
            if idx == 0:
                print('    ', end='')
            digit = idx // div % 10
            print(digit if div == 1 or (digit > 0 and idx %
                                        10 == 0) else ' ', end='')
        print('')
    for y, row in enumerate(dungeon):
        scores = '  ' + ', '.join(['{}({}#{})'.format(*units[(x, y)])
                                   for x in range(len(row))
                                   if (x, y) in units])
        for x, c in enumerate(row):
            pos = (x, y)
            glyph = units.get(pos, [c])[0]
            if x == 0:
                print('{:3} '.format(y), end='')
            print(glyph, end='')
        print(scores)


def round(dungeon, units):
    moves, attacks = 0, 0
    seen_units = set()
    for pos in sorted(units.keys(), key=sort_key):
        if pos not in units:
            # Kilt
            continue
        x, y = pos
        assert dungeon[y][x] == '.', dump(dungeon, units)
        unit_type, hp, uid = units[pos]
        assert uid not in seen_units
        assert hp > 0, (pos, units[pos])
        opponents = dict((pos, unit)
                         for pos, unit in units.items() if unit[0] != unit_type)
        if not opponents:
            # Game over, man!
            return units, True
        first_steps = [move for move in neighbors4(pos)]
        fight_with = weakest_neighbor(pos, opponents)
        if not fight_with:
            # No attacks possible; try a move
            in_range = [osp
                        for opos in opponents
                        for osp in open_spaces(opos, dungeon, units)]
            move = find_move(pos, in_range, dungeon, units)
            if not move:
                # Can't fight, can't move; what good are you?
                # print('{} at {} cannot move'.format(unit_type, pos))
                continue
            # Whew!  Now we know where to move
            units.pop(pos)
            pos = move
            x, y = pos
            assert dungeon[y][x] == '.'
            units[pos] = (unit_type, hp, uid)
            moves += 1
            # Now see if we can attack!
            fight_with = weakest_neighbor(pos, opponents)
        if fight_with:
            assert fight_with != pos
            otype, ohp, oid = units[fight_with]
            ohp -= 3
            if ohp <= 0:
                logging.debug('{} kills {} at {}, leaving {} units'.format(
                    pos, otype, fight_with, len(units) - 1))
                units.pop(fight_with)
            else:
                logging.debug('{} damages {} at {} leaving hp={}'.format(
                    pos, otype, fight_with, ohp))
                units[fight_with] = (otype, ohp, oid)
            attacks += 1
    assert moves + attacks > 0
    return units, False


def play(dungeon, units, verbose=False):
    rounds = 0
    gameover = False
    if verbose:
        dump(dungeon, units)
    while not gameover:
        units, gameover = round(dungeon, units)
        if not gameover:
            rounds += 1
        if verbose:
            dump(dungeon, units)
    if verbose:
        logging.info('Play ends after {} rounds with {} units remaining hp={}'.format(
                     rounds, len(units), sum(unit[1] for unit in units.values())))
    return rounds * sum(unit[1] for unit in units.values())


# assert play(*parse('''#######
# #.G...#
# #...EG#
# #.#.#G#
# #..G#E#
# #.....#
# ####### '''), verbose=True) == 27730

# dungeon, units = parse('''#########
# #G......#
# #.E.#...#
# #..##..G#
# #...##..#
# #...#...#
# #.G...G.#
# #.....G.#
# #########''')
# assert play(dungeon, units) == 18740

# assert play(*parse('''#######
# #G..#E#
# #E#E.E#
# #G.##.#
# #...#E#
# #...E.#
# #######''')) == 36334

# assert play(*parse('''#######
# #.E...#
# #.#..G#
# #.###.#
# #E#G#G#
# #...#G#
# #######'''), verbose=True) == 28944

dungeon, units = parse(Input(15))
print(play(dungeon, units, verbose=True))
