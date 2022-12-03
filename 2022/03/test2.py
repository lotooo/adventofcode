#!/usr/bin/env python3
import sys

alpha = "_abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ"

def load_data_from_file(filename):
    """ Load the input from a file and return the transformed version """
    with open(filename, 'r') as f:
        data = list(map(prepare_data, f.readlines()))
    return data


def prepare_data(x):
    """ transform the data the way we want it for the puzzle """
    return x.strip()


def solve(data):
    """ Solve the puzzle and return the solution """
    total = 0
    for gid in range(len(data) // 3):
        r1 = data[gid*3]
        r2 = data[gid*3+1]
        r3 = data[gid*3+2]
        item = set(r1) & set(r2) & set(r3)
        total += alpha.index(item.pop())
    return total


print("--> test data <--")
test_input = load_data_from_file('test_input')
assert solve(test_input) == 70

print()
print("--> real data <--")
my_input = load_data_from_file('input')
print(f"\nanswer: {solve(my_input)}")
