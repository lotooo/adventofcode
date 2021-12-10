#!/usr/bin/env python3
from collections import Counter

def load_data_from_file(filename):
    """ Load the input from a file and return the transformed version """
    with open(filename, 'r') as f:
        data = list(map(prepare_data, f.readlines()))
    return data


def prepare_data(x):
    """ transform the data the way we want it for the puzzle """
    return x.strip()


illegal_characters = {
    ')': 3,
    ']': 57,
    '}': 1197,
    '>': 25137
}

def solve(data):
    """ Solve the puzzle and return the solution """
    score = 0
    for line in data:
        last_size = 0
        while last_size != len(line):
            last_size = len(line)
            line = line.replace('<>','').replace('[]','').replace('{}','').replace('()','')
        for i in line:
            if i in illegal_characters:
                score += illegal_characters[i]
                break
    return score


print("--> test data <--")
test_input = load_data_from_file('test_input')
assert solve(test_input) == 26397

print()
print("--> real data <--")
my_input = load_data_from_file('input')
print(f"\nanswer: {solve(my_input)}")
