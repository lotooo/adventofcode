#!/usr/bin/env python3
import sys
import re

sys.path.append("../../")
from utils import *


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
    result = 0
    for line in data:
        for instruction in re.findall(r"mul\((\d+),(\d+)\)", line):
            result += int(instruction[0]) * int(instruction[1])
    return result


print("--> test data <--")
test_input = load_data_from_file("test_input")
assert solve(test_input) == 161

print()
print("--> real data <--")
my_input = load_data_from_file("input")
print(f"\nanswer: {solve(my_input)}")
