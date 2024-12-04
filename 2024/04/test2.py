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


def solve(data):
    """Solve the puzzle and return the solution"""
    g = Grid2D(data)
    to_process = []
    working_paths = 0
    for y, line in enumerate(data):
        for x, chr in enumerate(line):
            if chr == "A":
                to_process.append((x, y))
    usefull_path = []
    g.print(to_process)
    for start in to_process:
        x, y = start
        neighboors = [
            n[0]
            for n in g.get_neighboors_in_line(
                x,
                y,
                distance=1,
                include_self=False,
                include_vertical=False,
                include_horizontal=False,
            )
            if len(n) > 0
        ]
        if len(neighboors) < 4:
            continue
        if (
            (
                g.value(x - 1, y - 1) == "M"  # top left
                and g.value(x + 1, y + 1) == "S"  # bottom right
                and g.value(x - 1, y + 1) == "M"  # bottom left
                and g.value(x + 1, y - 1) == "S"  # top right
            )
            or (
                g.value(x - 1, y - 1) == "M"
                and g.value(x + 1, y + 1) == "S"
                and g.value(x - 1, y + 1) == "S"
                and g.value(x + 1, y - 1) == "M"
            )
            or (
                g.value(x - 1, y - 1) == "S"  # top left
                and g.value(x + 1, y + 1) == "M"  # bottom right
                and g.value(x - 1, y + 1) == "M"  # bottom left
                and g.value(x + 1, y - 1) == "S"  # top right
            )
            or (
                g.value(x - 1, y - 1) == "S"  # top left
                and g.value(x + 1, y + 1) == "M"  # bottom right
                and g.value(x - 1, y + 1) == "S"  # bottom left
                and g.value(x + 1, y - 1) == "M"  # top right
            )
        ):
            usefull_path.extend(neighboors)
            working_paths += 1
    return working_paths


print("--> test data <--")
test_input = load_data_from_file("test_input")
assert solve(test_input) == 9

print()
print("--> real data <--")
my_input = load_data_from_file("input")
print(f"\nanswer: {solve(my_input)}")
