#!/usr/bin/env python3
from collections import defaultdict
import sys

def load_data_from_file(filename):
    """ Load the input from a file and return the transformed version """
    with open(filename, 'r') as f:
        data = list(map(prepare_data, f.readlines()))
    return data


def prepare_data(x):
    """ transform the data the way we want it for the puzzle """
    signal_patterns, output = x.split(' | ')
    return signal_patterns.split(), output.split()


def solve(data):
    """ Solve the puzzle and return the solution """
    total = 0
    for signal_patterns,output in data:
        matched_patterns = {}
        while len(matched_patterns) != 10:
            for pattern in signal_patterns:
                if len(pattern) == 2:
                    matched_patterns[1] = sorted(pattern)
                if len(pattern) == 4:
                    matched_patterns[4] = sorted(pattern)
                if len(pattern) == 7:
                    matched_patterns[8] = sorted(pattern)
                if len(pattern) == 3:
                    matched_patterns[7] = sorted(pattern)
                if len(pattern) == 5:
                    # 2, 3 or 5
                    if 1 in matched_patterns and not 3 in matched_patterns:
                        if set(matched_patterns[1]).issubset(set(pattern)):
                            matched_patterns[3] = sorted(pattern)
                            continue
                    if 9 in matched_patterns and 3 in matched_patterns:
                        if 5 not in matched_patterns:
                            pattern_to_test = set(matched_patterns[9]) - set(matched_patterns[3])
                            if pattern_to_test.issubset(set(pattern)):
                                matched_patterns[5] = sorted(pattern)
                                continue
                    if 3 in matched_patterns and 5 in matched_patterns and not 2 in matched_patterns:
                        matched_patterns[2] = sorted(pattern)
                        continue
                if len(pattern) == 6:
                    # 0, 6 or 9
                    if 1 in matched_patterns and not 6 in matched_patterns:
                        if not set(matched_patterns[1]).issubset(set(pattern)):
                            matched_patterns[6] = sorted(pattern)
                    if 4 in matched_patterns and not 9 in matched_patterns:
                        if set(matched_patterns[4]).issubset(set(pattern)):
                            matched_patterns[9] = sorted(pattern)
                    if 6 in matched_patterns and 9 in matched_patterns and not 0 in matched_patterns:
                            matched_patterns[0] = sorted(pattern)
        printed_number = ""
        for displayed_number in output:
            for num, pattern in matched_patterns.items():
                if set(pattern) == set(displayed_number):
                    printed_number += str(num)
                    break
        total += int(printed_number)
    return total


print("--> test data <--")
test_input = load_data_from_file('test_input')
assert solve(test_input) == 61229

print()
print("--> real data <--")
my_input = load_data_from_file('input')
print(f"\nanswer: {solve(my_input)}")
