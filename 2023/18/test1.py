#!/usr/bin/env python3
import sys
import re

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


def build_lagoon(grid):
  min_y = min([g[1] for g in grid])
  min_x = min([g[0] for g in grid])
  max_y = max([g[1] for g in grid])
  max_x = max([g[0] for g in grid])
  lagoon = []
  for y in range(min_y, max_y + 1):
    l = []
    for x in range(min_x, max_x + 1):
      if x in [g[0] for g in grid if g[1] == y]:
        l.append("#")
      else:
        l.append(".")
    lagoon.append("".join(l))
  return lagoon


def get_inside_nodes(grid):
  inside = set()
  outside = set()
  loop = set()
  columns = rotate_matrix(grid)
  for y, line in enumerate(grid):
    score = 0
    for x, c in enumerate(line):
      if c == ".":
        left_nodes = grid[y][0:x]
        right_nodes = grid[y][x:]
        top_nodes = columns[x][0:y]
        bottom_nodes = columns[x][y:]
        if (
          "#" in left_nodes
          and "#" in right_nodes
          and "#" in top_nodes
          and "#" in bottom_nodes
        ):
          inside.add((x, y))
          score += 1
        else:
          outside.add((x, y))
      else:
        loop.add((x, y))
  # Let's remove our bad nodes
  # (the one considered inside while they have an outside neighboor)
  done = False
  while not done:
    done = True
    for x, y in inside.copy():
      if (
        (x + 1, y) in outside
        or (x - 1, y) in outside
        or (x, y - 1) in outside
        or (x, y + 1) in outside
      ):
        inside.remove((x, y))
        outside.add((x, y))
        done = False
  return inside | loop


def solve(data):
  """Solve the puzzle and return the solution"""
  grid = []
  position = (0, 0)
  grid.append(position)
  for rule in data:
    direction, distance, color = rule.split()
    if direction == "R":
      for i in range(int(distance)):
        grid.append((position[0] + 1 + i, position[1]))
      position = grid[-1]
    if direction == "L":
      for i in range(int(distance)):
        grid.append((position[0] - 1 - i, position[1]))
      position = grid[-1]
    if direction == "D":
      for i in range(int(distance)):
        grid.append((position[0], position[1] + 1 + i))
      position = grid[-1]
    if direction == "U":
      for i in range(int(distance)):
        grid.append((position[0], position[1] - 1 - i))
      position = grid[-1]
  print("Building Lagoon")
  lagoon = build_lagoon(set(grid))
  print("Getting inside nodes")
  inside_nodes = get_inside_nodes(lagoon)
  print_2d_grid(lagoon, inside_nodes)
  result = len(inside_nodes)
  return result


print("--> test data <--")
test_input = load_data_from_file("test_input")
assert solve(test_input) == 62

print()
print("--> real data <--")
my_input = load_data_from_file("input")
print(f"\nanswer: {solve(my_input)}")
