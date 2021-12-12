#!/usr/bin/env python3
from collections import defaultdict
import itertools

def load_data_from_file(filename):
    """ Load the input from a file and return the transformed version """
    with open(filename, 'r') as f:
        data = list(map(prepare_data, f.readlines()))
    return data


def prepare_data(x):
    """ transform the data the way we want it for the puzzle """
    begin, end = x.strip().split('-')
    return begin,end

def is_small_cave(cave):
    return cave.lower() == cave and cave not in ["start", "end"]


def visit(cave="start", my_path=""):
    if my_path == "":
        my_path = "start"
    else:
        my_path += f"-{cave}"
    if cave == "end":
        print(my_path)
        return my_path 
    else:
        ways = []
        for p in paths[cave]:
            # small cave check
            if is_small_cave(p) and p in my_path:
                # Don't go back in small cave
                continue
            if p == "start":
                # Don't go back at the begining
                continue
            elif f"{cave}-{p}-{cave}" in my_path:
                # don't loop
                continue
            else:
                ways.append(visit(cave=p, my_path=my_path))
    return ways

def paths_cleanup(paths):
    print("Cleaning up path")
    for cave, possibilities in paths.copy().items():
        print(f"Analysing path to and from {cave}")
        for p in possibilities:
            if is_small_cave(p) and is_small_cave(cave) and len(possibilities) == 1:
                print(f"Removing {cave} from {p}")
                paths[p].remove(cave)


def solve(data):
    """ Solve the puzzle and return the solution """
    global paths
    paths = defaultdict(set)
    for path in data:
        p1, p2 = path
        paths[p1].add(p2)
        paths[p2].add(p1)
    paths_cleanup(paths)
    ways = visit()
    # our ways variable is a crappy list of list of lists
    # Too lazy to investigate and correct
    flatten=lambda l: sum(map(flatten,l),[]) if isinstance(l,list) else [l]
    return len(flatten(ways))


print("--> test data <--")
test_input = load_data_from_file('test_input')
assert solve(test_input) == 10
test_input = load_data_from_file('test_input2')
assert solve(test_input) == 19
test_input = load_data_from_file('test_input3')
assert solve(test_input) == 226


print()
print("--> real data <--")
my_input = load_data_from_file('input')
print(f"\nanswer: {solve(my_input)}")
