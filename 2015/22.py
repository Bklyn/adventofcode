#!/usr/bin/env python3

import io
import random
from collections import namedtuple

Wizard = namedtuple("Wizard", "hp mana armor damage")
Effect = namedtuple("Effect", "timer armor damage mana")
Spell = namedtuple("Spell", "name mana damage healing effect")

Spells = [
    Spell("Magic Missile", 53, 4, 0, None),
    Spell("Drain", 73, 2, 2, None),
    Spell("Shield", 113, 0, 0, Effect(6, 7, 0, 0)),
    Spell("Poison", 173, 0, 0, Effect(6, 0, 3, 0)),
    Spell("Recharge", 229, 0, 0, Effect(5, 0, 0, 101)),
]


def age_effects(effects, output=None):
    result = dict()
    armor, damage, mana = 0, 0, 0
    for name, e in effects.items():
        e = e._replace(timer=e.timer - 1)
        if output:
            if name == "Shield":
                print(
                    f"Shield provides {e.armor} armor; its timer is now {e.timer}",
                    file=output,
                )
            if name == "Poison":
                print(
                    f"Poison deals {e.damage} damage; its timer is now {e.timer}",
                    file=output,
                )
            if name == "Recharge":
                print(
                    f"Recharge adds {e.mana} mana; its timer is now {e.timer}",
                    file=output,
                )
        armor += e.armor
        damage += e.damage
        mana += e.mana
        if e.timer == 0:
            if output:
                print(f"{name} wears off", file=output)
            continue
        result[name] = e
    if result:
        assert armor or damage or mana
    return (armor, damage, mana, result)


def wizardry(player, boss, hard=False, output=None):
    effects = dict()
    turn = 0
    spent = 0
    casted = []
    while True:
        turn += 1
        if output:
            print(f"-- Player turn {turn} --", file=output)
            print(
                f"- Player has {player.hp} HP, {player.armor} armor, {player.mana} mana, spent {spent}",
                file=output,
            )
            print(f"- Boss has {boss.hp} HP", file=output)
        if hard:
            player = player._replace(hp=player.hp - 1)
            if player.hp <= 0:
                return 10 ** 10, casted
        armor, damage, mana, effects = age_effects(effects, output)
        player = player._replace(armor=armor, damage=damage, mana=player.mana + mana)
        spells = [s for s in Spells if s.mana <= player.mana and s.name not in effects]
        if player.damage:
            boss = boss._replace(hp=boss.hp - player.damage)
            if boss.hp <= 0:
                if output:
                    print(f"This kills the Boss and we win", file=output)
                return spent, casted
        if not spells:
            if output:
                print(f"Can't afford any spells - we lose", file=output)
            return 10 ** 10, casted
        spell = random.choice(spells)
        casted.append(spell.name)
        spent += spell.mana
        player = player._replace(mana=player.mana - spell.mana)
        if output:
            print(
                f"Player casts {spell.name}, dealing {spell.damage} and healing {spell.healing} HP",
                file=output,
            )
        boss = boss._replace(hp=boss.hp - spell.damage)
        if boss.hp <= 0:
            if output:
                print(f"This kills the boss!", file=output)
            return spent, casted
        player = player._replace(hp=player.hp + spell.healing)
        if spell.effect is not None:
            effects[spell.name] = spell.effect
        if output:
            print(f"-- Boss turn {turn} --", file=output)
            print(
                f"- Player has {player.hp} HP, {player.armor} armor, {player.mana} mana",
                file=output,
            )
            print(f"- Boss has {boss.hp} HP", file=output)
        armor, damage, mana, effects = age_effects(effects, output)
        player = player._replace(armor=armor, damage=damage, mana=player.mana + mana)
        if player.damage:
            boss = boss._replace(hp=boss.hp - player.damage)
            if boss.hp <= 0:
                return spent, casted
        damage = max(1, boss.damage - player.armor)
        if output:
            print(
                f"Boss attacks for {boss.damage} - {player.armor} = {damage} damage",
                file=output,
            )
        player = player._replace(hp=player.hp - damage)
        if player.hp <= 0:
            if output:
                print(f"The Boss wins", file=output)
            return 10 ** 10, casted


best = 10 ** 10
for _ in range(20_000):
    gold, casted = wizardry(
        Wizard(hp=50, mana=500, armor=0, damage=0),
        Wizard(hp=51, mana=0, armor=0, damage=9),
    )
    if gold < best:
        best = gold
        print(f"Won with {gold} casting {casted}")
print(best)

best = 10 ** 10
for _ in range(100_000):
    gold, casted = wizardry(
        Wizard(hp=50, mana=500, armor=0, damage=0),
        Wizard(hp=51, mana=0, armor=0, damage=9),
        hard=True,
    )
    if gold < best:
        best = gold
        print(f"Won (hard) with {gold} casting {casted}")

print(best)
