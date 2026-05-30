#!/usr/bin/env python3

import numpy as np
import pytest

from aoc import array


def area(p, q):
    dy = 1 + abs(p[0] - q[0])
    dx = 1 + abs(p[1] - q[1])
    return dy * dx


def movie_theater(input: str) -> int:
    """Part 1: largest rectangle area spanned by any two vertices."""
    corners = array(input)
    rectangles = [(p, q) for i, p in enumerate(corners) for q in corners[i + 1 :]]
    return max(area(p, q) for p, q in rectangles)


def compress_coordinates(coordinates):
    """Rank-compress coords. Returns (compressed, width, height)."""
    unique_x = sorted({c[0] for c in coordinates})
    unique_y = sorted({c[1] for c in coordinates})
    x_rank = {x: i for i, x in enumerate(unique_x)}
    y_rank = {y: i for i, y in enumerate(unique_y)}
    compressed = [(x_rank[x], y_rank[y]) for x, y in coordinates]
    return compressed, len(unique_x), len(unique_y)


def find_interior_seed(edges, grid, width, height):
    """Find a cell strictly inside the polygon, from its border edges.

    The polygon's winding (sign of the shoelace area) tells us which side of a
    directed edge is the interior: the left for counter-clockwise loops, the
    right for clockwise ones. We step one cell off an edge's midpoint toward
    that interior side and return the first such cell that is not itself a
    border cell.

    Returns None when no interior cell exists -- e.g. when compression collapses
    the polygon to a grid that is entirely border (a bare rectangle). In that
    case the border mask is already complete and no flood-fill is needed.
    """
    twice_area = sum(x1 * y2 - x2 * y1 for (x1, y1), (x2, y2) in edges)
    turn = 1 if twice_area > 0 else -1  # +1 => interior on the left of an edge
    for (x1, y1), (x2, y2) in edges:
        dx = (x2 > x1) - (x2 < x1)  # unit edge direction
        dy = (y2 > y1) - (y2 < y1)
        nx, ny = -dy * turn, dx * turn  # inward (interior-side) normal
        cx, cy = (x1 + x2) // 2 + nx, (y1 + y2) // 2 + ny
        if 0 <= cx < width and 0 <= cy < height and not grid[cx, cy]:
            return cx, cy
    return None


def build_solid_mask(compressed, width, height):
    """Rasterize the polygon borders and flood-fill its interior.

    Returns a (width, height) int grid where 1 marks a solid cell.
    """
    grid = np.zeros((width, height), dtype=np.int32)

    # Borders: each edge is an axis-aligned span between consecutive vertices.
    edges = list(zip(compressed, compressed[1:] + compressed[:1]))
    for (x1, y1), (x2, y2) in edges:
        x_lo, x_hi = sorted((x1, x2))
        y_lo, y_hi = sorted((y1, y2))
        grid[x_lo : x_hi + 1, y_lo : y_hi + 1] = 1

    # Flood-fill the interior on a flat view -- iterative, with a frontier
    # guard so each cell is pushed at most once. A None seed means the grid is
    # all border (no interior to fill), so the mask is already complete.
    seed = find_interior_seed(edges, grid, width, height)
    if seed is None:
        return grid
    sx, sy = seed
    flat = grid.reshape(-1)
    stack = [sx * height + sy]
    while stack:
        idx = stack.pop()
        if flat[idx]:
            continue
        flat[idx] = 1
        x, y = divmod(idx, height)
        if x > 0 and not flat[idx - height]:
            stack.append(idx - height)
        if x < width - 1 and not flat[idx + height]:
            stack.append(idx + height)
        if y > 0 and not flat[idx - 1]:
            stack.append(idx - 1)
        if y < height - 1 and not flat[idx + 1]:
            stack.append(idx + 1)

    return grid


def largest_inside_rectangle(input: str) -> int:
    """Part 2: largest rectangle between two vertices that lies fully inside
    the polygon.

    Strategy: rank-compress to a small grid, rasterize the border and flood-fill
    the interior into a solid mask, then build a 2D summed-area table. A
    rectangle is fully inside iff its solid cell-count equals its area -- an O(1)
    test. All vertex pairs are evaluated at once via numpy broadcasting.
    """
    coordinates = array(input)
    compressed, width, height = compress_coordinates(coordinates)
    grid = build_solid_mask(compressed, width, height)

    # Summed-area table: prefix[x][y] = count of solid cells in [0,x) x [0,y).
    prefix = np.zeros((width + 1, height + 1), dtype=np.int64)
    prefix[1:, 1:] = grid.cumsum(0).cumsum(1)

    comp = np.array(compressed)
    orig = np.array(coordinates)
    cx, cy = comp[:, 0], comp[:, 1]
    ox, oy = orig[:, 0], orig[:, 1]

    # All coordinate pairs at once via outer broadcasting (n x n).
    x_min = np.minimum.outer(cx, cx)
    x_max = np.maximum.outer(cx, cx)
    y_min = np.minimum.outer(cy, cy)
    y_max = np.maximum.outer(cy, cy)

    cells = (x_max - x_min + 1) * (y_max - y_min + 1)
    solid = (
        prefix[x_max + 1, y_max + 1]
        - prefix[x_min, y_max + 1]
        - prefix[x_max + 1, y_min]
        + prefix[x_min, y_min]
    )
    inside = solid == cells

    # Area is measured on the ORIGINAL (uncompressed) coordinates.
    areas = (np.abs(np.subtract.outer(ox, ox)) + 1) * (
        np.abs(np.subtract.outer(oy, oy)) + 1
    )
    return int(areas[inside].max())


EXAMPLE = """7,1
11,1
11,7
9,7
9,5
2,5
2,3
7,3"""


def test_q09_example():
    assert movie_theater(EXAMPLE) == 50
    assert largest_inside_rectangle(EXAMPLE) == 24


@pytest.mark.real
def test_q09_real(puzzle):
    assert movie_theater(puzzle.input_data) == 4729332959
    assert largest_inside_rectangle(puzzle.input_data) == 1474477524


def main():
    from aocd import data

    print(movie_theater(data))
    print(largest_inside_rectangle(data))


if __name__ == "__main__":
    main()
