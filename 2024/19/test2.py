#!/usr/bin/env python3
import sys
from collections import defaultdict

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


def fget_arrangements(pattern, towels):
    """Test if a pattern is possible with the available towels"""
    to_process = [""]
    arrangements = []
    while len(to_process) > 0:
        p = to_process.pop()
        if p == pattern:
            arrangements.append(p)
        for towel in towels:
            if pattern.startswith(p + towel):
                to_process.append(p + towel)
    return arrangements


def get_arrangements(pattern, towels):
    sorted_towels = defaultdict(list)
    distinct_designs = defaultdict(int)
    distinct_designs[0] = 1
    for t in towels:
        sorted_towels[len(t)].append(t)
    for i in range(1, len(pattern) + 1):
        for towel in towels:
            l = len(towel)
            # print(f'{i=} : {towel=}')
            if i - l >= 0:
                same_size_towels = [t for t in towels if len(t) == l]
                # print(f'{i=} : {towel=} : {pattern[i-l:i]} - {same_size_towels}')
                # if pattern[i - l : i] in same_size_towels:
                if pattern[i - l : i] == towel:
                    distinct_designs[i] += distinct_designs[i - l]
            # print(f"=> {distinct_designs[i]}")
        # print(f"dp for {i}: {distinct_designs[i]}")
    return distinct_designs[len(pattern)]


def solve(data):
    """Solve the puzzle and return the solution"""
    towels = sorted(data[0].split(", "), key=lambda x: len(x), reverse=False)
    patterns = data[2:]
    result = []
    for i, pattern in enumerate(patterns):
        print(f"Working on pattern {i+1}/{len(patterns)}: {pattern}")
        arr = get_arrangements(pattern.strip(), towels)
        result.append(arr)
    print(result)
    return sum(result)


print("--> test data <--")
test_input = load_data_from_file("test_input")
assert solve(test_input) == 16

print()
print("--> real data <--")
my_input = load_data_from_file("input")
print(f"\nanswer: {solve(my_input)}")
