#!/usr/bin/env python3

from collections import deque

from aocd import data


def parse_input(data: str):
    return [[int(num) for num in row.split(",")] for row in data.splitlines()]


def compress_coordinates(coordinates):
    x_values = [c[0] for c in coordinates]
    y_values = [c[1] for c in coordinates]
    unique_x, unique_y = sorted(set(x_values)), sorted(set(y_values))
    x_rank = {x: i for i, x in enumerate(unique_x)}
    y_rank = {y: i for i, y in enumerate(unique_y)}
    return [(x_rank[x], y_rank[y]) for x, y in coordinates]


def span(c1, c2):
    x1, y1 = c1
    x2, y2 = c2
    x_min, x_max = sorted((x1, x2))
    y_min, y_max = sorted((y1, y2))
    return {(x, y) for x in range(x_min, x_max + 1) for y in range(y_min, y_max + 1)}


def flood_fill(borders, internal_point):
    directions = [(0, 1), (0, -1), (-1, 0), (1, 0)]
    visited = set()
    queue = deque([internal_point])
    while queue:
        current = queue.popleft()
        if current in visited:
            continue
        visited.add(current)
        x, y = current
        for dx, dy in directions:
            new_x, new_y = x + dx, y + dy
            if (new_x, new_y) not in borders:
                queue.append((new_x, new_y))
    return visited


def create_borders(coordinates):
    borders = set()
    complete = coordinates + [coordinates[0]]
    for c1, c2 in zip(complete, complete[1:]):
        borders |= span(c1, c2)
    return borders


def calculate_area(rectangle):
    (x1, y1), (x2, y2) = rectangle
    return (abs(x1 - x2) + 1) * (abs(y1 - y2) + 1)


def rectangle_inside(p1, p2, polygon):
    x1, y1 = p1
    x2, y2 = p2
    x_min, x_max = sorted((x1, x2))
    y_min, y_max = sorted((y1, y2))
    # First check corners
    if any(
        p not in polygon
        for p in ((x_min, y_min), (x_max, y_min), (x_min, y_max), (x_max, y_max))
    ):
        return False
    for x in range(x_min, x_max + 1):
        if (x, y_min) not in polygon or (x, y_max) not in polygon:
            return False
    for y in range(y_min, y_max + 1):
        if (x_min, y) not in polygon or (x_max, y) not in polygon:
            return False
    # Deep check of all points
    return all(
        (x, y) in polygon
        for x in range(x_min, x_max + 1)
        for y in range(y_min, y_max + 1)
    )


def part_two(coordinates, interior_seed):
    compressed = compress_coordinates(coordinates)
    borders = create_borders(compressed)
    interior = flood_fill(borders, interior_seed)
    polygon = borders | interior
    max_area = 0
    for i, p1 in enumerate(compressed):
        for j, p2 in enumerate(compressed[i + 1 :], i + 1):
            area = calculate_area((coordinates[i], coordinates[j]))
            if area <= max_area:
                continue
            if rectangle_inside(p1, p2, polygon):
                max_area = area
    return max_area


def main():
    coordinates = parse_input(data)
    seed = (150, 150)
    print(part_two(coordinates, seed))


if __name__ == "__main__":
    main()
