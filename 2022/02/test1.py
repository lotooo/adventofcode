#!/usr/bin/env python3
def load_data_from_file(filename):
    """ Load the input from a file and return the transformed version """
    with open(filename, 'r') as f:
        data = list(map(prepare_data, f.readlines()))
    return data


def prepare_data(x):
    """ transform the data the way we want it for the puzzle """
    return x.split()

score = {
    "A": 1, # Rock
    "B": 2, # Paper 
    "C": 3, # Scissor
    "X": 1, # Rock
    "Y": 2, # Paper 
    "Z": 3  # Scissor
}

DRAW=3
WIN=6
LOSE=0


def get_score(me, you):
    if score[me] == score[you]:
        # draw
        return score[me] + DRAW
    if you == 'A' and me == 'Z':
        return score[me] + LOSE
    if you == 'C' and me == 'X':
        return score[me] + WIN
    elif score[me] > score[you]:
        return score[me] + WIN
    else:
        return score[me] + LOSE


def solve(data):
    """ Solve the puzzle and return the solution """
    total = 0
    for you, me in data:
        total += get_score(me, you)
    return total


print("--> test data <--")
test_input = load_data_from_file('test_input')
assert solve(test_input) == 15

print()
print("--> real data <--")
my_input = load_data_from_file('input')
print(f"\nanswer: {solve(my_input)}")
