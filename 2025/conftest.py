"""Pytest fixtures for AoC 2025 — real-input regression tests and timing."""

import time
import pytest
from aocd.models import Puzzle


@pytest.fixture
def puzzle(request):
    """Provide the aocd Puzzle object for a given day.

    Usage in test:
        def test_q01_real(puzzle):
            from q01 import unlock
            assert unlock(puzzle.input_data) == (expected_p1, expected_p2)

    The day number is extracted from the test function name: test_q05_real → day 5.
    """
    import re

    match = re.search(r"q(\d+)", request.node.name)
    if not match:
        pytest.skip("Could not determine day from test name")
    day = int(match.group(1))
    return Puzzle(year=2025, day=day)


@pytest.fixture(autouse=True)
def _report_duration(request):
    """Print wall-clock time for every test (visible with pytest -s)."""
    start = time.perf_counter()
    yield
    elapsed = time.perf_counter() - start
    # Stash for the terminal reporter
    request.node.user_properties.append(("duration_ms", f"{elapsed * 1000:.1f}"))


def pytest_terminal_summary(terminalreporter, exitstatus, config):
    """Print a timing summary table at the end of the run."""
    reports = terminalreporter.stats.get("passed", []) + terminalreporter.stats.get(
        "failed", []
    )
    if not reports:
        return

    rows = []
    for report in reports:
        props = dict(report.user_properties)
        if "duration_ms" in props:
            rows.append((report.nodeid, props["duration_ms"]))

    if rows:
        terminalreporter.write_sep("=", "timing summary")
        for nodeid, ms in sorted(rows):
            terminalreporter.write_line(f"  {ms:>10s} ms  {nodeid}")
