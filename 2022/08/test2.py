#!/usr/bin/env python3
from itertools import takewhile

def load_data_from_file(filename):
    """ Load the input from a file and return the transformed version """
    with open(filename, 'r') as f:
        data = list(map(prepare_data, f.readlines()))
    return data


def prepare_data(x):
    """ transform the data the way we want it for the puzzle """
    return x.strip()


def get_scenic_score(x,y,trees):
    tree_height = int(trees[x][y])

    tree_line = list(trees[x])

    tree_column = [ line[y] for line in trees ]

    left_trees = list(reversed(tree_line[0:y]))
    left_view = list(takewhile(lambda h: int(h) < tree_height, left_trees))
    left_score = len(left_view)
    if len(left_trees) != len(left_view):
        left_score += 1

    right_trees = tree_line[y+1:]
    right_view = list(takewhile(lambda h: int(h) < tree_height, right_trees))
    right_score = len(right_view)
    if len(right_trees) != len(right_view):
        right_score += 1

    top_trees = list(reversed(tree_column[0:x]))
    top_view = list(takewhile(lambda h: int(h) < tree_height, top_trees))
    top_score = len(top_view)
    if len(top_trees) != len(top_view):
        top_score += 1

    bottom_trees = tree_column[x+1:]
    bottom_view = list(takewhile(lambda h: int(h) < tree_height, bottom_trees))
    bottom_score = len(bottom_view)
    if len(bottom_trees) != len(bottom_view):
        bottom_score += 1

    return left_score * right_score * top_score * bottom_score


def solve(data):
    """ Solve the puzzle and return the solution """
    scenic_scores = []
    for x in range(1,len(data[0])-1):
        for y in range(1, len(data)-1):
            scenic_scores.append(get_scenic_score(x,y,data))
    return max(scenic_scores)


print("--> test data <--")
test_input = load_data_from_file('test_input')
assert solve(test_input) == 8

print()
print("--> real data <--")
my_input = load_data_from_file('input')
print(f"\nanswer: {solve(my_input)}")
