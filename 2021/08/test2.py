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
    return list(map(set,signal_patterns.split())), output.split()


def solve(data):
    """ Solve the puzzle and return the solution """
    total = 0
    for signal_patterns,output in data:
        matched_patterns = {}
        while len(matched_patterns) != 10:
            for pattern in signal_patterns:
                if len(pattern) == 2:
                    matched_patterns[1] = pattern
                    continue
                if len(pattern) == 4:
                    matched_patterns[4] = pattern
                    continue
                if len(pattern) == 7:
                    matched_patterns[8] = pattern
                    continue
                if len(pattern) == 3:
                    matched_patterns[7] = pattern
                    continue
                if len(pattern) == 5:
                    # 2, 3 or 5
                    if 1 in matched_patterns and not 3 in matched_patterns and not 5 in matched_patterns:
                        if matched_patterns[1].issubset(pattern):
                            matched_patterns[3] = pattern
                            continue
                    if 9 in matched_patterns and 3 in matched_patterns and not 5 in matched_patterns and not 2 in matched_patterns:
                            pattern_to_test = matched_patterns[9] - matched_patterns[3]
                            if pattern_to_test.issubset(pattern):
                                matched_patterns[5] = pattern
                                continue
                    if 3 in matched_patterns and 5 in matched_patterns and not 2 in matched_patterns and 9 in matched_patterns:
                        pattern_to_test = matched_patterns[9] - matched_patterns[3]
                        if not pattern_to_test.issubset(pattern) and pattern != matched_patterns[3]:
                            matched_patterns[2] = pattern
                            continue
                if len(pattern) == 6:
                    # 0, 6 or 9
                    if 1 in matched_patterns and not 6 in matched_patterns and not 9 in matched_patterns and not 0 in matched_patterns:
                        if not matched_patterns[1].issubset(pattern):
                            matched_patterns[6] = pattern
                            continue
                    if 4 in matched_patterns and 6 in matched_patterns and not 9 in matched_patterns and not 0 in matched_patterns:
                        if matched_patterns[4].issubset(pattern):
                            matched_patterns[9] = pattern
                            continue
                    if 6 in matched_patterns and 9 in matched_patterns and not 0 in matched_patterns:
                        if matched_patterns[7].issubset(pattern):
                            matched_patterns[0] = pattern
                            continue
        printed_number = ""
        for displayed_number in output:
            for num, pattern in matched_patterns.items():
                if pattern == set(displayed_number):
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
