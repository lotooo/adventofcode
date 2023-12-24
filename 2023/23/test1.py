#!/usr/bin/env python3
import sys

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


def get_nexts(path, grid):
  position = path[-1]
  x, y = position
  nexts_paths = []
  if grid[y][x] in ["<", ">", "v", "^"]:
    if grid[y][x] == "<" and grid[y][x - 1] != "#" and (x - 1, y) not in path:
      tmp_path = path.copy()
      tmp_path.append((x - 1, y))
      nexts_paths.append(tmp_path)
      return nexts_paths
    if grid[y][x] == ">" and grid[y][x + 1] != "#" and (x + 1, y) not in path:
      tmp_path = path.copy()
      tmp_path.append((x + 1, y))
      nexts_paths.append(tmp_path)
      return nexts_paths
    if grid[y][x] == "^" and grid[y - 1][x] != "#" and (x, y - 1) not in path:
      tmp_path = path.copy()
      tmp_path.append((x, y - 1))
      nexts_paths.append(tmp_path)
      return nexts_paths
    if grid[y][x] == "v" and grid[y + 1][x] != "#" and (x, y + 1) not in path:
      tmp_path = path.copy()
      tmp_path.append((x, y + 1))
      nexts_paths.append(tmp_path)
      return nexts_paths
    return nexts_paths
  if y > 0 and grid[y - 1][x] != "#" and (x, y - 1) not in path:
    # UP
    tmp_path = path.copy()
    tmp_path.append((x, y - 1))
    nexts_paths.append(tmp_path)
  if y < len(grid) - 1 and grid[y + 1][x] != "#" and (x, y + 1) not in path:
    # DOWN
    tmp_path = path.copy()
    tmp_path.append((x, y + 1))
    nexts_paths.append(tmp_path)
  if x > 0 and grid[y][x - 1] != "#" and (x - 1, y) not in path:
    # LEFT
    tmp_path = path.copy()
    tmp_path.append((x - 1, y))
    nexts_paths.append(tmp_path)
  if x < len(grid[0]) - 1 and grid[y][x + 1] != "#" and (x + 1, y) not in path:
    # RIGHT
    tmp_path = path.copy()
    tmp_path.append((x + 1, y))
    nexts_paths.append(tmp_path)
  return nexts_paths


def solve(data):
  """Solve the puzzle and return the solution"""
  start = (data[0].index("."), 0)
  end = (data[-1].index("."), len(data) - 1)
  starting_path = [start]
  to_process = [starting_path]
  valid_paths = []
  while len(to_process) > 0:
    path = to_process.pop()
    for p in get_nexts(path, data):
      if p[-1] == end:
        valid_paths.append(p)
      else:
        to_process.append(p)
  return max([len(p) - 1 for p in valid_paths])


print("--> test data <--")
test_input = load_data_from_file("test_input")
assert solve(test_input) == 94

print()
print("--> real data <--")
my_input = load_data_from_file("input")
print(f"\nanswer: {solve(my_input)}")
