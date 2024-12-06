#!/usr/bin/env python3
import sys
from itertools import takewhile

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
    m = Grid2D(data)
    x, y = m.search("^")[0]
    my_way = [(x, y)]
    orders = "URDL"
    i = -1
    while True:
        i += 1
        x, y = my_way[-1]
        nexts = list(
            takewhile(
                lambda n: m.value(n[0], n[1]) != "#", m.get_nexts(x, y, orders[i % 4])
            )
        )
        my_way.extend(nexts)
        if nexts == m.get_nexts(x, y, orders[i % 4]):
            break
    return len(set(my_way))


print("--> test data <--")
test_input = load_data_from_file("test_input")
assert solve(test_input) == 41

print()
print("--> real data <--")
my_input = load_data_from_file("input")
print(f"\nanswer: {solve(my_input)}")
