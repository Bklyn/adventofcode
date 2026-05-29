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
import importlib
import json
import os
import statistics
import sys
import time

# Solver registry: day -> list of (func_name, args) to call
# Each entry calls func(data, *args) and captures the return value.
SOLVERS = {
    1: [("unlock",)],
    2: [("invalid_ids",), ("invalid_ids", True)],
    3: [("total_joltage",), ("total_joltage", 12)],
    4: [("forklift",), ("forklift", 10**10)],
    5: [("freshness",)],
    6: [("squid_math",), ("squid_math2",)],
    7: [("tachyon_beams",), ("tachyon_timelines",)],
    8: [("longest_circuits", 1000)],
    9: [("movie_theater",), ("find_largest_rectangle_optimized",)],
    10: [("factory",)],
    11: [("rack_graph",), ("server_rack",)],
    12: [("fit_presents",)],
}


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
    mod = load_module(day)
    results = []

    for entry in SOLVERS.get(day, []):
        func_name = entry[0]
        extra_args = entry[1:]
        func = getattr(mod, func_name)

        # For day 9 part 2, input needs array() preprocessing
        if func_name == "find_largest_rectangle_optimized":
            from aoc import array

            call_data = array(data)
        else:
            call_data = data

        label = (
            func_name
            if not extra_args
            else f"{func_name}({', '.join(map(str, extra_args))})"
        )

        timings = []
        answer = None
        for _ in range(repeat):
            t0 = time.perf_counter()
            answer = func(call_data, *extra_args)
            elapsed = time.perf_counter() - t0
            timings.append(elapsed * 1000)

        median_ms = statistics.median(timings)
        results.append((label, answer, median_ms))

        if not quiet:
            ans_str = str(answer)
            if len(ans_str) > 60:
                ans_str = ans_str[:57] + "..."
            print(f"  Day {day:2d}  {label:<45s}  {median_ms:>10.1f} ms  → {ans_str}")

    return results


def profile_day(day, data):
    """Run line_profiler on all solvers for a given day."""
    try:
        from line_profiler import LineProfiler
    except ImportError:
        print("line_profiler not installed. pip install line_profiler", file=sys.stderr)
        sys.exit(1)

    mod = load_module(day)

    for entry in SOLVERS.get(day, []):
        func_name = entry[0]
        extra_args = entry[1:]
        func = getattr(mod, func_name)

        if func_name == "find_largest_rectangle_optimized":
            from aoc import array

            call_data = array(data)
        else:
            call_data = data

        lp = LineProfiler()
        # Profile the main function and any functions it calls in the same module
        lp.add_function(func)
        for attr_name in dir(mod):
            obj = getattr(mod, attr_name)
            if callable(obj) and getattr(obj, "__module__", None) == mod.__name__:
                lp.add_function(obj)

        print(f"\n{'=' * 70}")
        print(f"PROFILE: Day {day} — {func_name}({', '.join(map(str, extra_args))})")
        print(f"{'=' * 70}")

        wrapped = lp(func)
        wrapped(call_data, *extra_args)
        lp.print_stats()


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

    days = args.days or sorted(SOLVERS.keys())

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
