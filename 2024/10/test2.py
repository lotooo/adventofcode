#!/usr/bin/env python3
import sys

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


def nexts():
    """Find next trail"""
    return True


def solve(data):
    """Solve the puzzle and return the solution"""
    g = Grid2D(data)
    trailheads = g.search("0")
    good_trails = []
    for trailhead in trailheads:
        to_process = [[trailhead]]
        while len(to_process) > 0:
            trail = to_process.pop()
            x, y = trail[-1]
            if g.value(x, y) == "9":
                good_trails.append(trail)
            else:
                for n in [
                    next[0]
                    for next in g.get_neighboors_in_line(x, y, include_diagonal=False)
                    if len(next) > 0
                ]:
                    nx, ny = n
                    if g.value(nx, ny) == ".":
                        continue
                    if int(g.value(nx, ny)) == int(g.value(x, y)) + 1:
                        if (nx, ny) not in trail:
                            ntrail = trail.copy()
                            ntrail.append((nx, ny))
                            to_process.append(ntrail)
    scores = []
    for trailhead in trailheads:
        score = len([g for g in good_trails if g[0] == trailhead])
        scores.append(score)

    return sum(scores)


print("--> test data <--")
test_input = load_data_from_file("test_input_part2_1")
assert solve(test_input) == 3
test_input = load_data_from_file("test_input_part2_2")
assert solve(test_input) == 13
test_input = load_data_from_file("test_input_part2_3")
assert solve(test_input) == 227
test_input = load_data_from_file("test_input5")
assert solve(test_input) == 81

print()
print("--> real data <--")
my_input = load_data_from_file("input")
print(f"\nanswer: {solve(my_input)}")
