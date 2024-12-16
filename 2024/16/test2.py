#!/usr/bin/env python3
import sys
from collections import defaultdict

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


def solve(data):
    """Solve the puzzle and return the solution"""
    g = Grid2D(data)
    s = g.search("S")[0]
    start = [(s[0], s[1], "R", 0)]
    print(f"Starting at {start}")
    to_process = [start]
    minimum_cost = None
    working_paths = []
    saved_results = defaultdict(list)
    cache = {}
    while len(to_process) > 0:
        working_node = to_process.pop()
        x, y, d, cost = working_node[-1]
        if minimum_cost is not None and cost > minimum_cost:
            # Cost is already too high, let's skip it
            continue
        visited_nodes = [(n[0], n[1]) for n in working_node]
        if g.value(x, y) == "E":
            # This is the end
            # My only friend, the end
            if minimum_cost is None:
                minimum_cost = cost
                working_paths.append(working_node)
                print(f"Found a path with a {cost} cost")
                saved_results[cost].append(working_node)
            else:
                if cost < minimum_cost:
                    minimum_cost = cost
                    print(
                        f"Found a path with a smaller cost : {cost} (but still {len(to_process)} paths to analyse)"
                    )
                    working_paths.append(working_node)
                if cost == minimum_cost:
                    print(f"Found a path with equal cost : {cost}")
                    saved_results[cost].append(working_node)
        else:
            cache[(x, y, d)] = cost
        for next_direction in ["U", "D", "L", "R"]:
            tmp_working_node = working_node.copy()
            next = g.get_nexts(x, y, next_direction)[0]
            nx, ny = next
            if (nx, ny) in visited_nodes:
                continue
            if g.value(nx, ny) != "#":
                if d in ["U", "D"]:
                    if next_direction in ["U", "D"]:
                        next_cost = 1
                    else:
                        next_cost = 1001  # 1000 to turn + 1 to move
                if d in ["L", "R"]:
                    if next_direction in ["L", "R"]:
                        next_cost = 1
                    else:
                        next_cost = 1001  # 1000 to turn + 1 to move
                tmp_working_node.append((nx, ny, next_direction, cost + next_cost))
                if (nx, ny, next_direction) not in cache:
                    to_process.append(tmp_working_node)
                else:
                    if cost + next_cost <= cache[(nx, ny, next_direction)]:
                        to_process.append(tmp_working_node)
    wp = working_paths[-1]
    visited_nodes = [(n[0], n[1]) for n in wp]
    sit_candidates = []
    for best_path in saved_results[wp[-1][3]]:
        for n in best_path:
            x, y, d, c = n
            if (x, y) not in sit_candidates:
                sit_candidates.append((x, y))
    return len(sit_candidates)


print("--> test data <--")
test_input = load_data_from_file("test_input")
assert solve(test_input) == 45
print("--> test data2 <--")
test_input2 = load_data_from_file("test_input2")
assert solve(test_input2) == 64

print()
print("--> real data <--")
my_input = load_data_from_file("input")
print(f"\nanswer: {solve(my_input)}")
