#!/usr/bin/python
'''--- Day 7: Recursive Circus ---

Wandering further through the circuits of the computer, you come upon
a tower of programs that have gotten themselves into a bit of
trouble. A recursive algorithm has gotten out of hand, and now they're
balanced precariously in a large tower.

One program at the bottom supports the entire tower. It's holding a
large disc, and on the disc are balanced several more sub-towers. At
the bottom of these sub-towers, standing on the bottom disc, are other
programs, each holding their own disc, and so on. At the very tops of
these sub-sub-sub-...-towers, many programs stand simply keeping the
disc below them balanced but with no disc of their own.

You offer to help, but first you need to understand the structure of
these towers. You ask each program to yell out their name, their
weight, and (if they're holding a disc) the names of the programs
immediately above them balancing on that disc. You write this
information down (your puzzle input). Unfortunately, in their panic,
they don't do this in an orderly fashion; by the time you're done,
you're not sure which program gave which information.

For example, if your list is the following:

pbga (66)
xhth (57)
ebii (61)
havc (66)
ktlj (57)
fwft (72) -> ktlj, cntj, xhth
qoyq (66)
padx (45) -> pbga, havc, qoyq
tknk (41) -> ugml, padx, fwft
jptl (61)
ugml (68) -> gyxo, ebii, jptl
gyxo (61)
cntj (57)

...then you would be able to recreate the structure of the towers that looks like this:

                gyxo
              /
         ugml - ebii
       /      \
      |         jptl
      |
      |         pbga
     /        /
tknk --- padx - havc
     \        \
      |         qoyq
o't      |
      |         ktlj
       \      /
         fwft - cntj
              \
                xhth

In this example, tknk is at the bottom of the tower (the bottom
program), and is holding up ugml, padx, and fwft. Those programs are,
in turn, holding up other programs; in this example, none of those
programs are holding up any other programs, and are all the tops of
their own towers. (The actual tower balancing in front of you is much
larger.)

Before you're ready to help them, you need to make sure your
information is correct. What is the name of the bottom program?

Your puzzle answer was ahnofa.

The first half of this puzzle is complete! It provides one gold star: *

--- Part Two ---

The programs explain the situation: they can't get down. Rather, they
could get down, if they weren't expending all of their energy trying
to keep the tower balanced. Apparently, one program has the wrong
weight, and until it's fixed, they're stuck here.

For any program holding a disc, each program standing on that disc
forms a sub-tower. Each of those sub-towers are supposed to be the
same weight, or the disc itself isn't balanced. The weight of a tower
is the sum of the weights of the programs in that tower.

In the example above, this means that for ugml's disc to be balanced,
gyxo, ebii, and jptl must all have the same weight, and they do: 61.

However, for tknk to be balanced, each of the programs standing on its
disc and all programs above it must each match. This means that the
following sums must all be the same:

ugml + (gyxo + ebii + jptl) = 68 + (61 + 61 + 61) = 251
padx + (pbga + havc + qoyq) = 45 + (66 + 66 + 66) = 243
fwft + (ktlj + cntj + xhth) = 72 + (57 + 57 + 57) = 243

As you can see, tknk's disc is unbalanced: ugml's stack is heavier
than the other two. Even though the nodes above ugml are balanced,
ugml itself is too heavy: it needs to be 8 units lighter for its stack
to weigh 243 and keep the towers balanced. If this change were made,
its weight would be 60.

Given that exactly one program is the wrong weight, what would its
weight need to be to balance the entire tower?

Although it hasn't changed, you can still get your puzzle input.
'''

from collections import defaultdict
from itertools import groupby


class Node:
    def __init__(self):
        self.name = None
        self.children = []
        self.weight = 0
        self.totwgt = 0
        self.parent = None

    def __str__(self):
        return '%s (%d / %d)' % (self.name, self.weight, self.totwgt)

def calc_weight(node):
    total = 0
    for c in node.children:
        if not c.children:
            c.totwgt = c.weight
        else:
            c.totwgt = calc_weight (c)
        total += c.totwgt
    return total + node.weight


def make_graph(lines):
    graph = defaultdict(Node)
    for line in lines:
        paren = line.find('(')
        assert paren > 0, 'Malformed input: %s' % line
        name = line[:paren].strip()
        node = graph[name]
        node.name = name
        node.weight = int(line[paren + 1:line.find(')')])
        arrow = line.find(' -> ')
        if arrow > 0:
            names = set(line[arrow + 4:].split(', '))
            node.children = [graph[c] for c in names]
            for c in node.children:
                c.parent = node
    calc_weight (find_root (graph))

    return graph


def find_root(graph):
    root = [x for x in graph.itervalues() if x.parent is None]
    assert len(root) == 1
    return root[0]


def odd_weight(node):
    def by_weight(node): return node.totwgt
    data = sorted(node.children, key=by_weight)
    for k, g in groupby(data, by_weight):
        l = list(g)
        if len(l) == 1:
            return l[0]
    return None


def solve(node):
    if node is None:
        return node
    oddball = odd_weight(node)
    # print node, oddball
    if oddball is None:
        idealwgt = [n.totwgt for n in node.parent.children if n.totwgt != node.totwgt]
        # print node, node.weight, '->', node.weight + (idealwgt[0] - node.totwgt)
        # return node
        return node.weight + (idealwgt[0] - node.totwgt)
    return solve(oddball)


TEST = '''pbga (66)
xhth (57)
ebii (61)
havc (66)
ktlj (57)
fwft (72) -> ktlj, cntj, xhth
qoyq (66)
padx (45) -> pbga, havc, qoyq
tknk (41) -> ugml, padx, fwft
jptl (61)
ugml (68) -> gyxo, ebii, jptl
gyxo (61)
cntj (57)'''

TEST_GRAPH = make_graph(TEST.split('\n'))
assert find_root(TEST_GRAPH).name == 'tknk'
assert TEST_GRAPH['ugml'].totwgt == 251
assert TEST_GRAPH['padx'].totwgt == 243
assert solve (find_root(TEST_GRAPH)) == 60

lines = [line.strip() for line in open('7.txt').readlines()]
graph = make_graph(lines)
root = find_root(graph)
print root.name

print solve(root)
