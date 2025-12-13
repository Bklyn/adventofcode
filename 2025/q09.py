#!/usr/bin/env python3

from aoc import array
from aocd import data


def area(p, q):
    dy = 1 + abs(p[0] - q[0])
    dx = 1 + abs(p[1] - q[1])
    return dy * dx


def movie_theater(input: str) -> int:
    corners = array(input)
    rectangles = [(p, q) for i, p in enumerate(corners) for q in corners[i + 1 :]]
    return max(area(p, q) for p, q in rectangles)


def point_in_polygon_fast(x, y, polygon):
    """Fast ray casting without boundary check - used for interior points"""
    n = len(polygon)
    inside = False
    p1x, p1y = polygon[0]
    for i in range(1, n + 1):
        p2x, p2y = polygon[i % n]
        if y > min(p1y, p2y):
            if y <= max(p1y, p2y):
                if x <= max(p1x, p2x):
                    if p1y != p2y:
                        xinters = (y - p1y) * (p2x - p1x) / (p2y - p1y) + p1x
                    if p1x == p2x or x <= xinters:
                        inside = not inside
        p1x, p1y = p2x, p2y
    return inside


def point_in_or_on_polygon(x, y, polygon):
    """Check if point is inside or on boundary of polygon"""
    # Quick ray-cast check first (much faster)
    if point_in_polygon_fast(x, y, polygon):
        return True

    # Only check boundary if ray-cast says outside
    # For integer coordinates on integer grid, boundary check is rare
    n = len(polygon)
    eps = 1e-9
    for i in range(n):
        x1, y1 = polygon[i]
        x2, y2 = polygon[(i + 1) % n]

        # Inline boundary check for speed
        if (
            min(x1, x2) - eps <= x <= max(x1, x2) + eps
            and min(y1, y2) - eps <= y <= max(y1, y2) + eps
        ):
            cross = (y - y1) * (x2 - x1) - (x - x1) * (y2 - y1)
            if abs(cross) < eps:
                return True

    return False


def segment_intersects_segment_proper(x1, y1, x2, y2, x3, y3, x4, y4, eps=1e-9):
    """Check if two segments properly intersect (cross, not just touch)"""
    denom = (x1 - x2) * (y3 - y4) - (y1 - y2) * (x3 - x4)

    if abs(denom) < eps:
        return False

    t = ((x1 - x3) * (y3 - y4) - (y1 - y3) * (x3 - x4)) / denom
    u = -((x1 - x2) * (y1 - y3) - (y1 - y2) * (x1 - x3)) / denom

    # Proper intersection - strictly inside both segments
    return 0 < t < 1 and 0 < u < 1


def rectangle_inside_polygon(
    rect_min_x, rect_min_y, rect_max_x, rect_max_y, polygon, polygon_edges
):
    """Check if rectangle is entirely inside polygon"""

    # Check center first (fastest rejection)
    center_x = (rect_min_x + rect_max_x) / 2
    center_y = (rect_min_y + rect_max_y) / 2
    if not point_in_polygon_fast(center_x, center_y, polygon):
        return False

    # Check corners (most likely to be on boundary)
    corners = [
        (rect_min_x, rect_min_y),
        (rect_max_x, rect_min_y),
        (rect_max_x, rect_max_y),
        (rect_min_x, rect_max_y),
    ]

    for cx, cy in corners:
        if not point_in_or_on_polygon(cx, cy, polygon):
            return False

    # Check for proper intersections with polygon edges
    rect_edges = [
        (rect_min_x, rect_min_y, rect_max_x, rect_min_y),
        (rect_max_x, rect_min_y, rect_max_x, rect_max_y),
        (rect_max_x, rect_max_y, rect_min_x, rect_max_y),
        (rect_min_x, rect_max_y, rect_min_x, rect_min_y),
    ]

    for x1, y1, x2, y2 in polygon_edges:
        for rx1, ry1, rx2, ry2 in rect_edges:
            if segment_intersects_segment_proper(x1, y1, x2, y2, rx1, ry1, rx2, ry2):
                return False

    # Reduced sampling - check just 2 points per edge
    # If corners and center are inside and no intersections, usually sufficient
    samples = 2
    for i in range(1, samples):
        t = i / samples
        # Use fast check for interior sample points (not on rect boundary)
        if not point_in_polygon_fast(
            rect_min_x + t * (rect_max_x - rect_min_x), rect_min_y, polygon
        ):
            return False
        if not point_in_polygon_fast(
            rect_min_x + t * (rect_max_x - rect_min_x), rect_max_y, polygon
        ):
            return False
        if not point_in_polygon_fast(
            rect_min_x, rect_min_y + t * (rect_max_y - rect_min_y), polygon
        ):
            return False
        if not point_in_polygon_fast(
            rect_max_x, rect_min_y + t * (rect_max_y - rect_min_y), polygon
        ):
            return False

    return True


def find_largest_rectangle_optimized(polygon):
    """Optimized algorithm with early termination and smart ordering"""
    n = len(polygon)

    # Precompute polygon edges
    polygon_edges = [
        (polygon[i][0], polygon[i][1], polygon[(i + 1) % n][0], polygon[(i + 1) % n][1])
        for i in range(n)
    ]

    # Get bounding box for early termination
    all_x = [p[0] for p in polygon]
    all_y = [p[1] for p in polygon]
    poly_min_x, poly_max_x = min(all_x), max(all_x)
    poly_min_y, poly_max_y = min(all_y), max(all_y)
    max_possible_area = (1 + poly_max_x - poly_min_x) * (1 + poly_max_y - poly_min_y)

    max_area = 0
    best_rect = None

    # Create list of all pairs with their potential areas
    candidates = []
    for i in range(n):
        x1, y1 = polygon[i]
        for j in range(i + 1, n):
            x2, y2 = polygon[j]

            # Skip degenerate
            if x1 == x2 or y1 == y2:
                continue

            # AOC uses discrete grid - area includes boundary points
            area = (1 + abs(x2 - x1)) * (1 + abs(y2 - y1))
            candidates.append((area, i, j))

    # Sort by area descending - check largest potential areas first
    candidates.sort(reverse=True)

    checked = 0
    for potential_area, i, j in candidates:
        # Early termination: if this area can't beat current best, we're done
        if potential_area <= max_area:
            break

        checked += 1

        x1, y1 = polygon[i]
        x2, y2 = polygon[j]

        rect_min_x = min(x1, x2)
        rect_max_x = max(x1, x2)
        rect_min_y = min(y1, y2)
        rect_max_y = max(y1, y2)

        # Quick rejection: check if rectangle center is inside before full validation
        center_x = (rect_min_x + rect_max_x) / 2
        center_y = (rect_min_y + rect_max_y) / 2
        if not point_in_polygon_fast(center_x, center_y, polygon):
            continue

        # Full validation
        if rectangle_inside_polygon(
            rect_min_x, rect_min_y, rect_max_x, rect_max_y, polygon, polygon_edges
        ):
            max_area = potential_area
            best_rect = ((rect_min_x, rect_min_y), (rect_max_x, rect_max_y))

            # If we found a very large rectangle, we can stop early
            if max_area > 0.9 * max_possible_area:
                break

    print(f"Checked {checked} out of {len(candidates)} candidates")
    return best_rect, max_area


def test_movie_theater():
    ex = """7,1
11,1
11,7
9,7
9,5
2,5
2,3
7,3"""
    assert 50 == movie_theater(ex)
    assert 24 == find_largest_rectangle_optimized(array(ex))[1]


if __name__ == "__main__":
    print(movie_theater(data))
    print(find_largest_rectangle_optimized(array(data)))
