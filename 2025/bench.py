#!/usr/bin/env python3
"""AoC 2025 benchmark runner.

Imports each day's module, runs solvers against real aocd input, and reports
a timing table.  Optionally profiles individual days with line_profiler.

Usage:
    python bench.py                  # run all days, print timing table
    python bench.py 9 10             # run only days 9 and 10
    python bench.py --profile 9      # line_profiler on day 9's solvers
    python bench.py --repeat 5       # run each day 5 times, report median
    python bench.py --csv             # append results to bench_results.csv
"""

import argparse
import glob
import importlib
import json
import os
import re
import statistics
import sys
import time


def load_module(day):
    """Import qNN.py as a module."""
    name = f"q{day:02d}"
    return importlib.import_module(name)


def get_data(day):
    """Fetch puzzle input via aocd."""
    from aocd.models import Puzzle

    return Puzzle(year=2025, day=day).input_data


def run_day(day, data, repeat=1, quiet=False):
    """Run all solvers for a day. Returns list of (label, answer, median_ms)."""
    from aoc import registered_solvers

    load_module(day)  # import triggers @solver registration
    results = []

    for entry in registered_solvers(day):
        timings = []
        answer = None
        for _ in range(repeat):
            t0 = time.perf_counter()
            answer = entry.func(data, *entry.args)
            elapsed = time.perf_counter() - t0
            timings.append(elapsed * 1000)

        median_ms = statistics.median(timings)
        results.append((entry.label, answer, median_ms))

        if not quiet:
            ans_str = str(answer)
            if len(ans_str) > 60:
                ans_str = ans_str[:57] + "..."
            print(
                f"  Day {day:2d}  {entry.label:<45s}  {median_ms:>10.1f} ms  → {ans_str}"
            )

    return results


def profile_day(day, data):
    """Run line_profiler on all solvers for a given day."""
    from aoc import registered_solvers

    try:
        from line_profiler import LineProfiler
    except ImportError:
        print("line_profiler not installed. pip install line_profiler", file=sys.stderr)
        sys.exit(1)

    mod = load_module(day)

    for entry in registered_solvers(day):
        lp = LineProfiler()
        # Profile the main function and any functions it calls in the same module
        lp.add_function(entry.func)
        for attr_name in dir(mod):
            obj = getattr(mod, attr_name)
            if callable(obj) and getattr(obj, "__module__", None) == mod.__name__:
                lp.add_function(obj)

        print(f"\n{'=' * 70}")
        print(f"PROFILE: Day {day} — {entry.label}")
        print(f"{'=' * 70}")

        wrapped = lp(entry.func)
        wrapped(data, *entry.args)
        lp.print_stats()


def available_days(script_dir):
    """Discover day numbers from qNN.py filenames in script_dir."""
    days = []
    for path in glob.glob(os.path.join(script_dir, "q[0-9][0-9].py")):
        match = re.search(r"q(\d+)\.py$", os.path.basename(path))
        if match:
            days.append(int(match.group(1)))
    return sorted(days)


def main():
    parser = argparse.ArgumentParser(description="AoC 2025 benchmark runner")
    parser.add_argument("days", nargs="*", type=int, help="Days to run (default: all)")
    parser.add_argument(
        "--repeat",
        type=int,
        default=1,
        help="Repeat each solver N times, report median",
    )
    parser.add_argument(
        "--profile", nargs="*", type=int, metavar="DAY", help="Line-profile these days"
    )
    parser.add_argument(
        "--csv", action="store_true", help="Append results to bench_results.csv"
    )
    parser.add_argument("--json", action="store_true", help="Print results as JSON")
    args = parser.parse_args()

    # Ensure 2025/ is on the path
    script_dir = os.path.dirname(os.path.abspath(__file__))
    if script_dir not in sys.path:
        sys.path.insert(0, script_dir)

    days = args.days or available_days(script_dir)

    # Profile mode
    if args.profile is not None:
        profile_days = args.profile or days
        for day in profile_days:
            data = get_data(day)
            profile_day(day, data)
        return

    # Benchmark mode
    print(f"AoC 2025 Benchmark (repeat={args.repeat})")
    print(f"{'─' * 80}")

    all_results = {}
    total_ms = 0

    for day in days:
        data = get_data(day)
        results = run_day(day, data, repeat=args.repeat)
        all_results[day] = results
        total_ms += sum(ms for _, _, ms in results)

    print(f"{'─' * 80}")
    print(f"  TOTAL: {total_ms:.1f} ms")

    if args.json:
        out = {}
        for day, results in all_results.items():
            out[day] = [
                {"solver": label, "answer": str(ans), "median_ms": ms}
                for label, ans, ms in results
            ]
        print(json.dumps(out, indent=2))

    if args.csv:
        import csv
        from datetime import datetime

        csv_path = os.path.join(script_dir, "bench_results.csv")
        is_new = not os.path.exists(csv_path)
        with open(csv_path, "a", newline="") as f:
            writer = csv.writer(f)
            if is_new:
                writer.writerow(
                    ["timestamp", "day", "solver", "answer", "median_ms", "repeat"]
                )
            ts = datetime.now().isoformat()
            for day, results in all_results.items():
                for label, ans, ms in results:
                    writer.writerow(
                        [ts, day, label, str(ans), f"{ms:.1f}", args.repeat]
                    )
        print(f"\nResults appended to {csv_path}")


if __name__ == "__main__":
    main()
