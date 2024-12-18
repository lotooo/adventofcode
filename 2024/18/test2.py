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


def solvable(g):
    """Test if a valid path can be found"""
    to_process = [[(0, 0)]]
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
        if current_node == (g.max_x - 1, g.max_y - 1):
            # This is the end
            return True

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
    return False


def solve(data, size=71, starter_byte=1024):
    """Solve the puzzle and return the solution"""
    grid = []
    for y in range(size):
        grid.append("." * size)
    g = Grid2D(grid)

    for i, raw_byte in enumerate(data):
        if i % 100 == 0:
            print(f"Adding byte {i}/{len(data)}")
        x, y = map(int, raw_byte.split(","))
        g.set_value(x, y, "#")
        if i >= starter_byte:
            if not solvable(g):
                print("No valid path found")
                break
    print(raw_byte)
    return raw_byte


print("--> test data <--")
test_input = load_data_from_file("test_input")
assert solve(test_input, size=7, starter_byte=12) == "6,1"

print()
print("--> real data <--")
my_input = load_data_from_file("input")
print(f"\nanswer: {solve(my_input)}")
