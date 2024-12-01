#!/usr/bin/env python3
import sys
from collections import Counter

sys.path.append("../../")
from utils import *


def load_data_from_file(filename):
    """Load the input from a file and return the transformed version"""
    with open(filename, "r") as f:
        data = list(map(prepare_data, f.readlines()))
    return data


def prepare_data(x):
    """transform the data the way we want it for the puzzle"""
    return x.strip().split()


def solve(data):
    """Solve the puzzle and return the solution"""
    list1 = list(map(lambda x: int(x[0]), data))
    list2 = Counter(list(map(lambda x: int(x[1]), data)))
    x = 0
    for i in list1:
        x += list2[i] * i
    return x


print("--> test data <--")
test_input = load_data_from_file("test_input")
assert solve(test_input) == 31

print()
print("--> real data <--")
my_input = load_data_from_file("input")
print(f"\nanswer: {solve(my_input)}")
