#!/usr/bin/env python3
import sys

sys.path.append("../../")
from utils import Grid2D


def load_data_from_file(filename):
    """Load the input from a file and return the transformed version"""
    with open(filename, "r") as f:
        data = list(map(prepare_data, f.readlines()))
    return data


def prepare_data(x):
    """transform the data the way we want it for the puzzle"""
    return x.strip()


def solve(data, size=71, max_bytes=1024):
    """Solve the puzzle and return the solution"""
    grid = []
    for y in range(size):
        grid.append("." * size)
    g = Grid2D(grid)

    for raw_byte in data[:max_bytes]:
        x, y = map(int, raw_byte.split(","))
        g.set_value(x, y, "#")

    to_process = [[(0, 0)]]

    valid_paths = []
    shortest_path = None
    cache = {}

    while len(to_process) > 0:
        processed_path = to_process.pop()
        current_node = processed_path[-1]
        x, y = current_node

        if (x, y) in cache:
            if len(processed_path) >= cache[(x, y)]:
                # We already have a shortest path to this node
                continue
        cache[(x, y)] = len(processed_path)

        # Test if we reached the end
        if current_node == (size - 1, size - 1):
            # This is the end
            valid_paths.append(processed_path)
            if shortest_path is not None:
                shortest_path = min(shortest_path, len(processed_path))
            else:
                shortest_path = len(processed_path)
            continue

        # Test if this path is not too long already
        if shortest_path is not None:
            if len(processed_path) >= shortest_path:
                continue

        # Find neighboors
        for next_direction in ["U", "D", "L", "R"]:
            processing_path = processed_path.copy()
            nexts = g.get_nexts(x, y, next_direction)
            if len(nexts) == 0:
                continue
            nx, ny = nexts[0]
            if g.value(nx, ny) != "#" and (nx, ny) not in processed_path:
                processing_path.append((nx, ny))
                to_process.append(processing_path)
    return shortest_path - 1  # the start doesn't count as "step"


print("--> test data <--")
test_input = load_data_from_file("test_input")
assert solve(test_input, size=7, max_bytes=12) == 22

print()
print("--> real data <--")
my_input = load_data_from_file("input")
print(f"\nanswer: {solve(my_input)}")
