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
            if chr == "X":
                to_process.append((x, y))
    usefull_path = []
    for start in to_process:
        x, y = start
        for n in g.get_neighboors_in_line(x, y, distance=3, include_self=True):
            if len(n) < 4:
                continue
            r = "".join(list(map(lambda x: g.value(x[0], x[1]), n)))
            if r in ["XMAS", "SAMX"]:
                usefull_path.extend(n)
                working_paths += 1
    g.print(usefull_path)
    return working_paths


print("--> test data <--")
test_input = load_data_from_file("test_input")
assert solve(test_input) == 18

print()
print("--> real data <--")
my_input = load_data_from_file("input")
print(f"\nanswer: {solve(my_input)}")
