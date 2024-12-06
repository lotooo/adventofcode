#!/usr/bin/env python3
import sys
from itertools import takewhile

sys.path.append("../../")
from utils import Grid2D


def load_data_from_file(filename):
    """Load the input from a file and return the transformed version"""
    with open(filename, "r") as f:
        data = list(map(prepare_data, f.readlines()))
    return data


def prepare_data(x):
    """transform the data the way we want it for the puzzle"""
    return x.strip()


def test_path(data, x, y, debug=False):
    m = Grid2D(data)
    my_way = [(x, y)]
    orders = "URDL"
    walked = []
    i = -1
    while True:
        i += 1
        x, y = my_way[-1]
        nexts = list(
            takewhile(
                lambda n: m.value(n[0], n[1]) != "#", m.get_nexts(x, y, orders[i % 4])
            )
        )
        my_way.extend(nexts)
        if len(nexts) == len(m.get_nexts(x, y, orders[i % 4])):
            return True
        if (nexts, orders[i % 4]) in walked and len(nexts) > 0:
            if debug:
                print((nexts, orders[i % 4]))
                m.print(my_way)
            return False
        walked.append((nexts, orders[i % 4]))


def solve(data):
    """Solve the puzzle and return the solution"""
    m = Grid2D(data)
    sx, sy = m.search("^")[0]
    my_way = [(sx, sy)]
    orders = "URDL"
    i = -1
    while True:
        i += 1
        x, y = my_way[-1]
        nexts = list(
            takewhile(
                lambda n: m.value(n[0], n[1]) != "#", m.get_nexts(x, y, orders[i % 4])
            )
        )
        my_way.extend(nexts)
        if nexts == m.get_nexts(x, y, orders[i % 4]):
            break
    wrong = 0
    initial_path = set(my_way)
    for new_obstruction in [(x, y) for x, y in initial_path if (x, y) != (sx, sy)]:
        new_test = data.copy()
        tmp = list(new_test[new_obstruction[1]])
        tmp[new_obstruction[0]] = "#"
        new_test[new_obstruction[1]] = "".join(tmp)
        if not test_path(new_test, sx, sy):
            wrong += 1
    return wrong


print("--> test data <--")
test_input = load_data_from_file("test_input")
assert solve(test_input) == 6

print()
print("--> real data <--")
my_input = load_data_from_file("input")
print(f"\nanswer: {solve(my_input)}")
