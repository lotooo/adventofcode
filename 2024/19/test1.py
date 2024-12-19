#!/usr/bin/env python3
import sys

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


def is_possible(pattern, towels):
    """Test if a pattern is possible with the available towels"""
    to_process = [""]
    visited = []
    while len(to_process) > 0:
        p = to_process.pop()
        # print(f"Current: {p}")
        if len(p) > len(pattern):
            continue
        if p in visited:
            continue
        visited.append(p)
        if p == pattern:
            return True
        for towel in towels:
            if p + towel in pattern:
                to_process.append(p + towel)
            if towel + p in pattern:
                to_process.append(towel + p)
    return False


def solve(data):
    """Solve the puzzle and return the solution"""
    towels = sorted(data[0].split(", "), key=lambda x: len(x), reverse=True)
    patterns = data[2:]
    possible_patterns = []
    for pattern in patterns:
        if is_possible(pattern, towels):
            possible_patterns.append(pattern)
    return len(possible_patterns)


print("--> test data <--")
test_input = load_data_from_file("test_input")
assert solve(test_input) == 6

print()
print("--> real data <--")
my_input = load_data_from_file("input")
print(f"\nanswer: {solve(my_input)}")
