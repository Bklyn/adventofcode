#!/usr/bin/env python3
'''--- Day 24: Immune System Simulator 20XX ---

After a weird buzzing noise, you appear back at the man's cottage. He
seems relieved to see his friend, but quickly notices that the little
reindeer caught some kind of cold while out exploring.

The portly man explains that this reindeer's immune system isn't
similar to regular reindeer immune systems:

The immune system and the infection each have an army made up of
several groups; each group consists of one or more identical
units. The armies repeatedly fight until only one army has units
remaining.

Units within a group all have the same hit points (amount of damage a
unit can take before it is destroyed), attack damage (the amount of
damage each unit deals), an attack type, an initiative (higher
initiative units attack first and win ties), and sometimes weaknesses
or immunities. Here is an example group:

- 18 units each with 729 hit points (weak to fire; immune to cold,
  slashing) with an attack that does 8 radiation damage at initiative
  10

Each group also has an effective power: the number of units in that
group multiplied by their attack damage. The above group has an
effective power of 18 * 8 = 144. Groups never have zero or negative
units; instead, the group is removed from combat.

Each fight consists of two phases: target selection and attacking.

During the target selection phase, each group attempts to choose one
target. In decreasing order of effective power, groups choose their
targets; in a tie, the group with the higher initiative chooses
first. The attacking group chooses to target the group in the enemy
army to which it would deal the most damage (after accounting for
weaknesses and immunities, but not accounting for whether the
defending group has enough units to actually receive all of that
damage).

If an attacking group is considering two defending groups to which it
would deal equal damage, it chooses to target the defending group with
the largest effective power; if there is still a tie, it chooses the
defending group with the highest initiative. If it cannot deal any
defending groups damage, it does not choose a target. Defending groups
can only be chosen as a target by one attacking group.

At the end of the target selection phase, each group has selected zero
or one groups to attack, and each group is being attacked by zero or
one groups.

During the attacking phase, each group deals damage to the target it
selected, if any. Groups attack in decreasing order of initiative,
regardless of whether they are part of the infection or the immune
system. (If a group contains no units, it cannot attack.)

The damage an attacking group deals to a defending group depends on
the attacking group's attack type and the defending group's immunities
and weaknesses. By default, an attacking group would deal damage equal
to its effective power to the defending group. However, if the
defending group is immune to the attacking group's attack type, the
defending group instead takes no damage; if the defending group is
weak to the attacking group's attack type, the defending group instead
takes double damage.

The defending group only loses whole units from damage; damage is
always dealt in such a way that it kills the most units possible, and
any remaining damage to a unit that does not immediately kill it is
ignored. For example, if a defending group contains 10 units with 10
hit points each and receives 75 damage, it loses exactly 7 units and
is left with 3 units at full health.

After the fight is over, if both armies still contain units, a new
fight begins; combat only ends once one army has lost all of its
units.

For example, consider the following armies:

Immune System:
- 17 units each with 5390 hit points (weak to radiation,
  bludgeoning) with an attack that does 4507 fire damage at initiative 2

- 989 units each with 1274 hit points (immune to fire; weak to
  bludgeoning, slashing) with an attack that does 25 slashing damage
  at initiative 3

Infection:
- 801 units each with 4706 hit points (weak to radiation) with an attack
 that does 116 bludgeoning damage at initiative 1
- 4485 units each with 2961 hit points (immune to radiation; weak to fire,
  cold) with an attack that does 12 slashing damage at initiative 4

If these armies were to enter combat, the following fights, including
details during the target selection and attacking phases, would take
place:

Immune System:
- Group 1 contains 17 units
- Group 2 contains 989 units
Infection:
- Group 1 contains 801 units
- Group 2 contains 4485 units

Infection group 1 would deal defending group 1 185832 damage
Infection group 1 would deal defending group 2 185832 damage
Infection group 2 would deal defending group 2 107640 damage
Immune System group 1 would deal defending group 1 76619 damage
Immune System group 1 would deal defending group 2 153238 damage
Immune System group 2 would deal defending group 1 24725 damage

Infection group 2 attacks defending group 2, killing 84 units
Immune System group 2 attacks defending group 1, killing 4 units
Immune System group 1 attacks defending group 2, killing 51 units
Infection group 1 attacks defending group 1, killing 17 units
Immune System:
Group 2 contains 905 units
Infection:
Group 1 contains 797 units
Group 2 contains 4434 units

Infection group 1 would deal defending group 2 184904 damage
Immune System group 2 would deal defending group 1 22625 damage
Immune System group 2 would deal defending group 2 22625 damage

Immune System group 2 attacks defending group 1, killing 4 units
Infection group 1 attacks defending group 2, killing 144 units
Immune System:
Group 2 contains 761 units
Infection:
Group 1 contains 793 units
Group 2 contains 4434 units

Infection group 1 would deal defending group 2 183976 damage
Immune System group 2 would deal defending group 1 19025 damage
Immune System group 2 would deal defending group 2 19025 damage

Immune System group 2 attacks defending group 1, killing 4 units
Infection group 1 attacks defending group 2, killing 143 units
Immune System:
Group 2 contains 618 units
Infection:
Group 1 contains 789 units
Group 2 contains 4434 units

Infection group 1 would deal defending group 2 183048 damage
Immune System group 2 would deal defending group 1 15450 damage
Immune System group 2 would deal defending group 2 15450 damage

Immune System group 2 attacks defending group 1, killing 3 units
Infection group 1 attacks defending group 2, killing 143 units
Immune System:
Group 2 contains 475 units
Infection:
Group 1 contains 786 units
Group 2 contains 4434 units

Infection group 1 would deal defending group 2 182352 damage
Immune System group 2 would deal defending group 1 11875 damage
Immune System group 2 would deal defending group 2 11875 damage

Immune System group 2 attacks defending group 1, killing 2 units
Infection group 1 attacks defending group 2, killing 142 units
Immune System:
Group 2 contains 333 units
Infection:
Group 1 contains 784 units
Group 2 contains 4434 units

Infection group 1 would deal defending group 2 181888 damage
Immune System group 2 would deal defending group 1 8325 damage
Immune System group 2 would deal defending group 2 8325 damage

Immune System group 2 attacks defending group 1, killing 1 unit
Infection group 1 attacks defending group 2, killing 142 units
Immune System:
Group 2 contains 191 units
Infection:
Group 1 contains 783 units
Group 2 contains 4434 units

Infection group 1 would deal defending group 2 181656 damage
Immune System group 2 would deal defending group 1 4775 damage
Immune System group 2 would deal defending group 2 4775 damage

Immune System group 2 attacks defending group 1, killing 1 unit
Infection group 1 attacks defending group 2, killing 142 units
Immune System:
Group 2 contains 49 units
Infection:
Group 1 contains 782 units
Group 2 contains 4434 units

Infection group 1 would deal defending group 2 181424 damage
Immune System group 2 would deal defending group 1 1225 damage
Immune System group 2 would deal defending group 2 1225 damage

Immune System group 2 attacks defending group 1, killing 0 units
Infection group 1 attacks defending group 2, killing 49 units

Immune System:
No groups remain.

Infection:
Group 1 contains 782 units
Group 2 contains 4434 units

In the example above, the winning army ends up with 782 + 4434 = 5216 units.

You scan the reindeer's condition (your puzzle input); the
white-bearded man looks nervous. As it stands now, how many units
would the winning army have?

--- Part Two ---

Things aren't looking good for the reindeer. The man asks whether more
milk and cookies would help you think.

If only you could give the reindeer's immune system a boost, you might
be able to change the outcome of the combat.

A boost is an integer increase in immune system units' attack
damage. For example, if you were to boost the above example's immune
system's units by 1570, the armies would instead look like this:

Immune System:
17 units each with 5390 hit points (weak to radiation, bludgeoning) with
 an attack that does 6077 fire damage at initiative 2
989 units each with 1274 hit points (immune to fire; weak to bludgeoning,
 slashing) with an attack that does 1595 slashing damage at initiative 3

Infection:
801 units each with 4706 hit points (weak to radiation) with an attack
 that does 116 bludgeoning damage at initiative 1
4485 units each with 2961 hit points (immune to radiation; weak to fire,
 cold) with an attack that does 12 slashing damage at initiative 4
With this boost, the combat proceeds differently:

Immune System:
Group 2 contains 989 units
Group 1 contains 17 units
Infection:
Group 1 contains 801 units
Group 2 contains 4485 units

Infection group 1 would deal defending group 2 185832 damage
Infection group 1 would deal defending group 1 185832 damage
Infection group 2 would deal defending group 1 53820 damage
Immune System group 2 would deal defending group 1 1577455 damage
Immune System group 2 would deal defending group 2 1577455 damage
Immune System group 1 would deal defending group 2 206618 damage

Infection group 2 attacks defending group 1, killing 9 units
Immune System group 2 attacks defending group 1, killing 335 units
Immune System group 1 attacks defending group 2, killing 32 units
Infection group 1 attacks defending group 2, killing 84 units
Immune System:
Group 2 contains 905 units
Group 1 contains 8 units
Infection:
Group 1 contains 466 units
Group 2 contains 4453 units

Infection group 1 would deal defending group 2 108112 damage
Infection group 1 would deal defending group 1 108112 damage
Infection group 2 would deal defending group 1 53436 damage
Immune System group 2 would deal defending group 1 1443475 damage
Immune System group 2 would deal defending group 2 1443475 damage
Immune System group 1 would deal defending group 2 97232 damage

Infection group 2 attacks defending group 1, killing 8 units
Immune System group 2 attacks defending group 1, killing 306 units
Infection group 1 attacks defending group 2, killing 29 units
Immune System:
Group 2 contains 876 units
Infection:
Group 2 contains 4453 units
Group 1 contains 160 units

Infection group 2 would deal defending group 2 106872 damage
Immune System group 2 would deal defending group 2 1397220 damage
Immune System group 2 would deal defending group 1 1397220 damage

Infection group 2 attacks defending group 2, killing 83 units
Immune System group 2 attacks defending group 2, killing 427 units
After a few fights...

Immune System:
Group 2 contains 64 units
Infection:
Group 2 contains 214 units
Group 1 contains 19 units

Infection group 2 would deal defending group 2 5136 damage
Immune System group 2 would deal defending group 2 102080 damage
Immune System group 2 would deal defending group 1 102080 damage

Infection group 2 attacks defending group 2, killing 4 units
Immune System group 2 attacks defending group 2, killing 32 units
Immune System:
Group 2 contains 60 units
Infection:
Group 1 contains 19 units
Group 2 contains 182 units

Infection group 1 would deal defending group 2 4408 damage
Immune System group 2 would deal defending group 1 95700 damage
Immune System group 2 would deal defending group 2 95700 damage

Immune System group 2 attacks defending group 1, killing 19 units
Immune System:
Group 2 contains 60 units
Infection:
Group 2 contains 182 units

Infection group 2 would deal defending group 2 4368 damage
Immune System group 2 would deal defending group 2 95700 damage

Infection group 2 attacks defending group 2, killing 3 units
Immune System group 2 attacks defending group 2, killing 30 units
After a few more fights...

Immune System:
Group 2 contains 51 units
Infection:
Group 2 contains 40 units

Infection group 2 would deal defending group 2 960 damage
Immune System group 2 would deal defending group 2 81345 damage

Infection group 2 attacks defending group 2, killing 0 units
Immune System group 2 attacks defending group 2, killing 27 units
Immune System:
Group 2 contains 51 units
Infection:
Group 2 contains 13 units

Infection group 2 would deal defending group 2 312 damage
Immune System group 2 would deal defending group 2 81345 damage

Infection group 2 attacks defending group 2, killing 0 units
Immune System group 2 attacks defending group 2, killing 13 units
Immune System:
Group 2 contains 51 units
Infection:
No groups remain.
This boost would allow the immune system's armies to win! It would be left with 51 units.

You don't even know how you could boost the reindeer's immune system or what effect it might have, so you need to be cautious and find the smallest boost that would allow the immune system to win.

How many units does the immune system have left after getting the smallest boost it needs to win?

'''

from aoc2018 import *
from dataclasses import dataclass
import enum


class Team(enum.Enum):
    IMMUNE = enum.auto()
    INFECTION = enum.auto()


@dataclass
class Group:
    team: Team
    id: int
    ounits: int
    hp: int
    damage: int
    initiative: int
    weaknesses: set
    immunities: set
    attack_type: str
    killed: int = 0
    boost: int = 0

    def __hash__(self):
        return self.id

    def __cmp__(self, other):
        return self.id == other.id

    @property
    def effective_power(self):
        return self.units * (self.damage + self.boost)

    @property
    def units(self):
        return max(self.ounits - self.killed, 0)

    @property
    def alive(self):
        return self.units > 0

    def reset(self, boost):
        self.killed = 0
        self.boost = boost if self.team == Team.IMMUNE else 0

def parse(lines):
    if isinstance(lines, str):
        lines = lines.splitlines()
    team = None
    armies = []
    for line in lines:
        line = line.strip()
        if not line:
            continue
        elif line == 'Immune System:':
            team = Team.IMMUNE
            continue
        elif line == 'Infection:':
            team = Team.INFECTION
            continue
        m = re.match(
            r'(\d+) units each with (\d+) hit points(?: \(([^\)]+)\))? with an attack that does (\d+) (\w+) damage at initiative (\d+)', line)
        assert m is not None
        groups = m.groups()
        units, hp, damage, initiative = map(
            int, (groups[0], groups[1], groups[3], groups[5]))
        weaknesses = set()
        immunities = set()
        if groups[2] is not None:
            for clause in groups[2].split(';'):
                words = clause.strip().split(' ')
                what, powers = words[0], [
                    w.strip(',') for w in words[2:] if w != 'to']
                if what == 'weak':
                    weaknesses = set(powers)
                elif what == 'immune':
                    immunities = set(powers)
                else:
                    assert False, (what, powers)
        grp = Group(team, len(armies) + 1, units, hp, damage, initiative, weaknesses,
                    immunities, groups[4])
        armies.append(grp)
    return armies


class Reindeer:
    def __init__(self, armies):
        self.armies = armies

    @staticmethod
    def calc_damage(army, opponent):
        damage = army.effective_power
        if army.attack_type in opponent.weaknesses:
            damage *= 2
        elif army.attack_type in opponent.immunities:
            damage = 0
        return damage

    def team(self, which):
        return [a for a in self.armies if a.team == which and a.units > 0]

    def game_over(self):
        teams = set ([a.team for a in self.armies if a.alive])
        return len(teams) == 1

    def round(self, debug=False):
        # Targeting phase
        armies = [a for a in self.armies if a.units > 0]
        targets = dict ((a.id, a) for a in armies)
        attacks = {}
        total_kills = 0
        for a in sorted(armies, key=lambda g: (g.effective_power, g.initiative), reverse=True):
            if debug:
                print('Targeting:', a)
            opponents = sorted ([(self.calc_damage (a, t), t.effective_power, t.initiative, t)
                                 for t in targets.values() if t.team != a.team],
                                key=lambda x: (x[0], x[1], x[2]), reverse=True)
            if not opponents:
                continue
            damage, _ep, _in, opp = opponents[0]
            if not damage:
                continue
            targets.pop (opp.id)
            if debug:
                print ('\tTarget:', damage, opp)
            attacks[a.id] = opp

        # Attack phase
        for a in sorted(armies, key=lambda g: g.initiative, reverse=True):
            if not a.id in attacks:
                continue
            elif not a.units:   # Perhaps killed along the way
                continue
            opp = attacks[a.id]
            assert opp in armies
            damage = self.calc_damage (a, opp)
            kilt = min(opp.units, damage // opp.hp)
            if debug:
                print ('Attack:', a, 'vs', opp, 'deals', damage, 'damage, killing', kilt, 'units, leaving', opp.units - kilt)
            opp.killed += kilt
            total_kills += kilt
        return total_kills

    def play(self, maxrounds=10**10, debug=False):
        rounds = 0
        zeroes = 0
        while not self.game_over () and rounds < maxrounds:
            kills = self.round(debug=debug)
            if kills != 0:
                zeroes = 0
            else:
                zeroes += 1
                if zeroes > 10:
                    break
            rounds += 1

    def final_score(self):
        if not self.game_over():
            return (None, 0)
        alive = [a for a in self.armies if a.alive]
        return first(a.team for a in alive), sum(a.units for a in alive)

test_armies = parse('''Immune System:
17 units each with 5390 hit points (weak to radiation, bludgeoning) with an attack that does 4507 fire damage at initiative 2
989 units each with 1274 hit points (immune to fire; weak to bludgeoning, slashing) with an attack that does 25 slashing damage at initiative 3

Infection:
801 units each with 4706 hit points (weak to radiation) with an attack that does 116 bludgeoning damage at initiative 1
4485 units each with 2961 hit points (immune to radiation; weak to fire, cold) with an attack that does 12 slashing damage at initiative 4''')
rd = Reindeer(test_armies)
rd.play ()
print (rd.final_score())

armies = parse(Input(24))
rd = Reindeer (armies)
rd.play()
print (rd.final_score())

# Binary search for necessary boost to make immunity win
boost_lb, boost_ub = 1, 1048576
while True:
#     boost_lb < boost_ub:
    boost = (boost_lb + boost_ub) // 2
    print (boost_lb, boost_ub, boost)
    for a in armies:
        a.reset (boost)
    rd = Reindeer(armies)
    rd.play()
    winner, score = rd.final_score()
    print (boost, winner, score)
    if boost_lb == boost_ub:
        assert winner == Team.IMMUNE
        break
    if winner == Team.IMMUNE:
        boost_ub = boost
    else:
        boost_lb = boost + 1

print (boost_lb, rd.final_score())
