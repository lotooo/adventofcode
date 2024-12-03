#!/usr/bin/env python3
import sys
import re

sys.path.append("../../")
from utils import *


def load_data_from_file(filename):
    """Load the input from a file and return the transformed version"""
    with open(filename, "r") as f:
        data = list(map(prepare_data, f.readlines()))
    return "".join(data)


def prepare_data(x):
    """transform the data the way we want it for the puzzle"""
    return x.strip()


def solve(data):
    """Solve the puzzle and return the solution"""
    result = 0
    parsed = re.findall(r"mul\(\d+,\d+\)|do\(\)|don\'t\(\)", data)
    enabled = True
    for instruction in parsed:
        m = re.fullmatch(r"mul\((\d+),(\d+)\)", instruction)
        if m and enabled:
            result += int(m.group(1)) * int(m.group(2))
        elif instruction == "don't()":
            enabled = False
        elif instruction == "do()":
            enabled = True
    return result


print("--> test data <--")
test_input = load_data_from_file("test_input2")
assert solve(test_input) == 48

print()
print("--> real data <--")
my_input = load_data_from_file("input")
print(f"\nanswer: {solve(my_input)}")
