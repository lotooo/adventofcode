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
    return list(map(lambda i: int(i), x.strip().split()))


def analyse(report):
    analysis = []
    for i in range(len(report) - 1):
        analysis.append(report[i] - report[i + 1])
    return analysis


def solve(data):
    """Solve the puzzle and return the solution"""
    safe_report_count = 0
    for report in data:
        analysis = analyse(report)
        is_increasing = all(map(lambda x: x < 0, analysis))
        is_decreasing = all(map(lambda x: x > 0, analysis))
        level_is_safe = all(map(lambda x: abs(x) <= 3, analysis))
        if (is_increasing or is_decreasing) and level_is_safe:
            safe_report_count += 1
    return safe_report_count


print("--> test data <--")
test_input = load_data_from_file("test_input")
assert solve(test_input) == 2

print()
print("--> real data <--")
my_input = load_data_from_file("input")
print(f"\nanswer: {solve(my_input)}")
