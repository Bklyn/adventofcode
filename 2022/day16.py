from aoc import *


def volcano(input):
   valves = {}
   rates = {}
   for line in input.splitlines():
      # Valve HH has flow rate=22; tunnel leads to valve GG
      m = re.match(r"Valve (\w+) has flow rate=(\d+); .* valve(?:s)? (.+)", line)
      assert m, line
      valve, rate, n = m.groups()
      valves[valve] = (int(rate), set(n.split(", ")))
      rates[valve] = int(rate)

   # Find paths between all valves
   paths = {}
   for v1, v2 in permutations(valves.keys(), 2):
      path = bfs(v1, lambda v: valves[v][1], v2)
      paths[(v1, v2)] = path[1:]
      paths[(v1, v1)] = paths[(v2, v2)] = []

   def flow(v1, v2, t):
      steps = len(paths[(v1, v2)])
      x = rates[v2] * (30 - t - steps - 1)
      return max(x, 0)

   closed = set(valves.keys())
   path = []
   loc = 'AA'
   score = 0
   while closed:
      time = len(path)
      print(f"Minute {time}: {path}")
      options = [
         (v, flow(loc, v, time), paths[(loc, v)])
         for v in closed]
      options.sort(key=lambda x: x[1], reverse=True)
      best, s, p = options[0]
      print(time, score, options)
      path.extend(paths[(loc, best)] + ["Open " + best])
      closed.remove(best)
      score += s
      loc = best

   print(s, path)

p = Puzzle(day=16)
assert volcano(p.example_data) == 1651