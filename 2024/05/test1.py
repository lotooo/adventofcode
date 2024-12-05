#!/usr/bin/env python3
import sys
import re
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


def is_valid_update(update, rules):
    for u in update:
        update_index = update.index(u)
        if u not in rules:
            continue
        prior_elements = update[:update_index]
        for test in rules[u]:
            if test in prior_elements:
                return False
    return True


def solve(data):
    """Solve the puzzle and return the solution"""
    raw_rules = []
    updates = []
    for line in data:
        if "|" in line:
            raw_rules.append(list(map(lambda x: int(x), line.split("|"))))
        if "," in line:
            updates.append(list(map(lambda x: int(x), line.split(","))))

    rules = defaultdict(list)
    for rule in raw_rules:
        rules[rule[0]].append(rule[1])

    valid_updates = [u for u in updates if is_valid_update(u, rules)]

    return sum([u[(len(u) - 1) // 2] for u in valid_updates])


print("--> test data <--")
test_input = load_data_from_file("test_input")
assert solve(test_input) == 143

print()
print("--> real data <--")
my_input = load_data_from_file("input")
print(f"\nanswer: {solve(my_input)}")
