#!/usr/bin/env python3
import sys
from collections import defaultdict

sys.path.append("../../")
from utils import *


def load_data_from_file(filename):
  """Load the input from a file and return the transformed version"""
  with open(filename, "r") as f:
    data = list(map(prepare_data, f.readlines()))
  return data


def prepare_data(x):
  """transform the data the way we want it for the puzzle"""
  return x.strip()


def get_nexts(position, grid):
  nexts = []
  x, y = position
  if x > 0 and grid[y][x - 1] != "#":
    nexts.append((x - 1, y))
  if x < len(grid[y]) - 1 and grid[y][x + 1] != "#":
    nexts.append((x + 1, y))
  if y > 0 and grid[y - 1][x] != "#":
    nexts.append((x, y - 1))
  if y < len(grid) - 1 and grid[y + 1][x] != "#":
    nexts.append((x, y + 1))
  return nexts


def solve(data, steps):
  """Solve the puzzle and return the solution"""
  for y, line in enumerate(data):
    if "S" in line:
      x = line.index("S")
      break
  start = (x, y)
  to_process = [start]
  next_to_process = to_process.copy()
  for s in range(steps):
    to_process = next_to_process.copy()
    next_to_process = []
    while len(to_process) > 0:
      node = to_process.pop()
      for n in [n for n in get_nexts(node, data)]:
        if n not in next_to_process:
          next_to_process.append(n)
  return len(next_to_process)


print("--> test data <--")
test_input = load_data_from_file("test_input")
assert solve(test_input, 1) == 2
assert solve(test_input, 2) == 4
assert solve(test_input, 3) == 6
assert solve(test_input, 6) == 16

print()
print("--> real data <--")
my_input = load_data_from_file("input")
print(f"\nanswer: {solve(my_input,64)}")
