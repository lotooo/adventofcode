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


closing_characters = {
    ')': 1,
    ']': 2,
    '}': 3,
    '>': 4
}
opening_characters = {
    '(': 1,
    '[': 2,
    '{': 3,
    '<': 4
}


def solve(data):
    """ Solve the puzzle and return the solution """
    scores = []
    for line in data:
        score = 0
        last_size = 0
        chunks = line
        while last_size != len(line):
            last_size = len(line)
            line = line.replace('<>','').replace('[]','').replace('{}','').replace('()','')
        if any(map(lambda x: x in closing_characters, line)):
            # corrupted
            continue
        for i in line[::-1]:
            if i in opening_characters:
                score = (5 * score) + opening_characters[i]
        scores.append(score)
    return sorted(scores)[len(scores)//2]


print("--> test data <--")
test_input = load_data_from_file('test_input')
assert solve(test_input) == 288957

print()
print("--> real data <--")
my_input = load_data_from_file('input')
print(f"\nanswer: {solve(my_input)}")
