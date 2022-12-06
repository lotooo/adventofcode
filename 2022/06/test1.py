#!/usr/bin/env python3
from collections import Counter 
def load_data_from_file(filename):
    """ Load the input from a file and return the transformed version """
    with open(filename, 'r') as f:
        data = list(map(prepare_data, f.readlines()))
    return data[0]


def prepare_data(x):
    """ transform the data the way we want it for the puzzle """
    return x.strip()


def solve(data):
    """ Solve the puzzle and return the solution """
    for i in range(len(data)):
        marker = Counter(data[i:i+4])
        element, occ = marker.most_common()[0]
        if occ == 1:
            return i+4
    return False


print("--> test data <--")
test_input = load_data_from_file('test_input')
assert solve(test_input) == 7

print()
print("--> real data <--")
my_input = load_data_from_file('input')
print(f"\nanswer: {solve(my_input)}")
