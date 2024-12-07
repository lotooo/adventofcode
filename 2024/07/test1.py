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


def partial_test(remaining, expected_result):
    a = remaining.pop(0)
    b = remaining.pop(0)

    out = []

    if a * b <= expected_result:
        m_remaining = remaining.copy()
        m_remaining.insert(0, a * b)
        out.append(m_remaining)
    if a + b <= expected_result:
        s_remaining = remaining.copy()
        s_remaining.insert(0, a + b)
        out.append(s_remaining)
    return out


def solve(data):
    """Solve the puzzle and return the solution"""
    valid = []
    for line in data:
        n = re.findall(r"(\d+)", line)
        expected_result = int(n[0])
        numbers = list(map(int, n[1:]))
        to_process = [numbers]
        while len(to_process) > 0:
            numbers = to_process.pop()
            tests = partial_test(numbers, expected_result)
            for candidate in tests:
                if len(candidate) == 1 and candidate[0] == expected_result:
                    valid.append(expected_result)
                    to_process = []
                    break
                if len(candidate) > 1:
                    to_process.append(candidate)

    return sum(valid)


print("--> test data <--")
test_input = load_data_from_file("test_input")
assert solve(test_input) == 3749

print()
print("--> real data <--")
my_input = load_data_from_file("input")
print(f"\nanswer: {solve(my_input)}")
