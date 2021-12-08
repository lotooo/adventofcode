#!/usr/bin/env python3
from collections import defaultdict

def load_data_from_file(filename):
    """ Load the input from a file and return the transformed version """
    with open(filename, 'r') as f:
        data = list(map(prepare_data, f.readlines()))
    return data


def prepare_data(x):
    """ transform the data the way we want it for the puzzle """
    signal_patterns, output = x.split(' | ')
    return signal_patterns.split(), output.split()

seven_segements_display_patterns = {
    0: {
        'a': True,
        'b': True,
        'c': True,
        'd': False,
        'e': True,
        'f': True,
        'g': True
    },
    1: {
        'a': False,
        'b': False,
        'c': True,
        'd': False,
        'e': False,
        'f': True,
        'g': False
    },
    2: {
        'a': True,
        'b': False,
        'c': True,
        'd': True,
        'e': True,
        'f': False,
        'g': True
    },
    3: {
        'a': True,
        'b': False,
        'c': True,
        'd': True,
        'e': False,
        'f': True,
        'g': True
    },
    4: {
        'a': False,
        'b': True,
        'c': True,
        'd': True,
        'e': False,
        'f': True,
        'g': False
    },
    5: {
        'a': True,
        'b': True,
        'c': False,
        'd': True,
        'e': False,
        'f': True,
        'g': True
    },
    6: {
        'a': True,
        'b': True,
        'c': False,
        'd': True,
        'e': True,
        'f': True,
        'g': True
    },
    7: {
        'a': True,
        'b': False,
        'c': True,
        'd': False,
        'e': False,
        'f': True,
        'g': False
    },
    8: {
        'a': True,
        'b': True,
        'c': True,
        'd': True,
        'e': True,
        'f': True,
        'g': True
    },
    9: {
        'a': True,
        'b': True,
        'c': True,
        'd': True,
        'e': False,
        'f': True,
        'g': True
    },

}

segments_count = defaultdict(list)

for digit, pattern in seven_segements_display_patterns.items():
    segments_count[list(pattern.values()).count(True)].append(digit)


def solve(data):
    """ Solve the puzzle and return the solution """
    count = 0
    for signal_patterns,output in data:
        for number in output:
            if len(segments_count[len(number)]) == 1:
                count += 1
    return count


print("--> test data <--")
test_input = load_data_from_file('test_input')
assert solve(test_input) == 26

print()
print("--> real data <--")
my_input = load_data_from_file('input')
print(f"\nanswer: {solve(my_input)}")
