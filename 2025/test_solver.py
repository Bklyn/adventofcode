"""Unit tests for the @solver registration decorator in aoc.py."""

import pytest

import aoc


def test_day_from_file_parses_day():
    assert aoc._day_from_file("/repo/2025/q09.py") == 9
    assert aoc._day_from_file("/repo/2025/q12.py") == 12
    assert aoc._day_from_file("q01.py") == 1


def test_day_from_file_rejects_non_qNN():
    with pytest.raises(ValueError):
        aoc._day_from_file("/repo/2025/aoc.py")


def test_solver_registers_entry_with_args(monkeypatch):
    monkeypatch.setattr(aoc, "_day_from_file", lambda path: 99)
    aoc._REGISTRY.pop(99, None)

    @aoc.solver(part=2, args=(7,))
    def dummy(x):
        return x * 2

    entries = aoc.registered_solvers(99)
    assert len(entries) == 1
    entry = entries[0]
    assert entry.day == 99
    assert entry.part == 2
    assert entry.args == (7,)
    assert entry.label == "dummy(7)"
    assert dummy(5) == 10  # decorator returns the function unchanged
    aoc._REGISTRY.pop(99, None)


def test_solver_label_without_args(monkeypatch):
    monkeypatch.setattr(aoc, "_day_from_file", lambda path: 98)
    aoc._REGISTRY.pop(98, None)

    @aoc.solver(part=1)
    def plain(x):
        return x

    assert aoc.registered_solvers(98)[0].label == "plain"
    aoc._REGISTRY.pop(98, None)


def test_registered_solvers_sorted_by_part(monkeypatch):
    monkeypatch.setattr(aoc, "_day_from_file", lambda path: 97)
    aoc._REGISTRY.pop(97, None)

    @aoc.solver(part=2)
    def second(x):
        return x

    @aoc.solver(part=1)
    def first(x):
        return x

    assert [e.part for e in aoc.registered_solvers(97)] == [1, 2]
    aoc._REGISTRY.pop(97, None)
