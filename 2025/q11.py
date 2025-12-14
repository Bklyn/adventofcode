#!/usr/bin/env python3


from aocd import data
from aoc import vector
from collections import deque


def parse_rack(input: str) -> dict:
    devices = dict()
    for line in input.strip().splitlines():
        device, *outputs = vector(line)
        devices[device] = outputs
    return devices


def rack_graph(input: str) -> int:
    devices = parse_rack(input)
    assert "you" in devices
    num_paths = 0
    todo = deque(["you"])
    while todo:
        node = todo.popleft()
        if node == "out":
            num_paths += 1
            continue
        for out in devices.get(node, []):
            todo.append(out)
    return num_paths


def server_rack(input: str) -> int:
    devices = parse_rack(input)

    def count_paths(node, dac=False, fft=False, seen={}):
        if (node, dac, fft) in seen:
            return seen[(node, dac, fft)]
        if node == "out":
            return 1 if dac and fft else 0
        answer = seen[(node, dac, fft)] = sum(
            count_paths(child, dac or child == "dac", fft or child == "fft", seen)
            for child in devices[node]
        )
        # print(f"> {node} {dac} {fft}: {answer}")
        return answer

    return count_paths("svr")


def test_rack():
    ex = """aaa: you hhh
you: bbb ccc
bbb: ddd eee
ccc: ddd eee fff
ddd: ggg
eee: out
fff: out
ggg: out
hhh: ccc fff iii
iii: out"""
    assert 5 == rack_graph(ex)
    assert 2 == server_rack("""svr: aaa bbb
aaa: fft
fft: ccc
bbb: tty
tty: ccc
ccc: ddd eee
ddd: hub
hub: fff
eee: dac
dac: fff
fff: ggg hhh
ggg: out
hhh: out""")


if __name__ == "__main__":
    print(rack_graph(data))
    print(server_rack(data))
