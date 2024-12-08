#!/usr/bin/env python3
import sys
from itertools import permutations
import math

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


def get_antinodes(points):
    p1, p2 = points
    x1, y1 = p1
    x2, y2 = p2

    distance = math.sqrt((x2 - x1) ** 2 + (y2 - y1) ** 2)

    # direction
    dx = x2 - x1
    dy = y2 - y1

    length = math.sqrt(dx**2 + dy**2)
    dx = dx / length
    dy = dy / length

    nx1 = int(x1 - distance * dx)
    ny1 = int(y1 - distance * dy)
    nx2 = int(x2 + distance * dx)
    ny2 = int(y2 + distance * dy)

    return (nx1, ny1), (nx2, ny2)


def solve(data):
    """Solve the puzzle and return the solution"""
    m = Grid2D(data)
    frequencies = {}
    for y, line in enumerate(data):
        for x, char in enumerate(line):
            if char != ".":
                frequencies[char] = []
    antinodes = []
    for freq in frequencies:
        antennas = m.search(freq)
        for pair in permutations(antennas, 2):
            for antinode in get_antinodes(pair):
                x, y = antinode
                if (
                    x >= 0
                    and x < m.max_x
                    and y >= 0
                    and y < m.max_y
                    and (x, y) not in antinodes
                ):
                    antinodes.append((x, y))
    m.print(antinodes)
    return len(antinodes)


print("--> test data <--")
test_input = load_data_from_file("test_input")
assert solve(test_input) == 14

print()
print("--> real data <--")
my_input = load_data_from_file("input")
print(f"\nanswer: {solve(my_input)}")
