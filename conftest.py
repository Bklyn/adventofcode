"""Root pytest config: keep collection to active, test-bearing locations.

Legacy year directories hold solved-puzzle scripts (some Python 2.x) with no
tests. After numeric solvers are renamed to dayNN.py they would match the
day*.py collection glob, so a root-level `pytest` would try to import them and
could fail (e.g. SyntaxError on Py2). Ignore them from default collection.
"""

collect_ignore_glob = [
    "2015/*",
    "2016/*",
    "2017/*",
    "2018/*",
    "2019/*",
    "2020/*",
    "2021/*",
    # 2022 scripts with module-level side effects / no tests
    "2022/day14.py",  # renamed script; runs a fetch+assert at module level
    "2022/day15-zniperr.py",  # reads from stdin at module level
    "2022/day16.py",
    "2022/day17.py",  # fetches puzzle input at import
]
