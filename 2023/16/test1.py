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


def get_next(direction, position, grid):
  x, y = position
  if grid[y][x] == ".":
    if direction == ">":
      return [(direction, (x + 1, y))]
    if direction == "<":
      return [(direction, (x - 1, y))]
    if direction == "^":
      return [(direction, (x, y - 1))]
    if direction == "v":
      return [(direction, (x, y + 1))]
  if grid[y][x] == "-":
    if direction == ">":
      return [(direction, (x + 1, y))]
    if direction == "<":
      return [(direction, (x - 1, y))]
    if direction in ["^", "v"]:
      nexts = []
      if x > 0:
        nexts.append(("<", (x - 1, y)))
      if x < len(grid[0]) - 1:
        nexts.append((">", (x + 1, y)))
      return nexts
  if grid[y][x] == "|":
    if direction in [">", "<"]:
      nexts = []
      if y > 0:
        nexts.append(("^", (x, y - 1)))
      if y < len(grid) - 1:
        nexts.append(("v", (x, y + 1)))
      return nexts
    if direction == "^":
      return [(direction, (x, y - 1))]
    if direction == "v":
      return [(direction, (x, y + 1))]
  if grid[y][x] == "/":
    if direction == ">":
      return [("^", (x, y - 1))]
    if direction == "<":
      return [("v", (x, y + 1))]
    if direction == "^":
      return [(">", (x + 1, y))]
    if direction == "v":
      return [("<", (x - 1, y))]
  if grid[y][x] == "\\":
    if direction == ">":
      return [("v", (x, y + 1))]
    if direction == "<":
      return [("^", (x, y - 1))]
    if direction == "^":
      return [("<", (x - 1, y))]
    if direction == "v":
      return [(">", (x + 1, y))]
  raise "WTF am I supposed to do ?"


def solve(data):
  """Solve the puzzle and return the solution"""
  energy = [(0, 0)]
  processed = []
  to_be_processed = [(">", (0, 0))]
  while len(to_be_processed) > 0:
    node = to_be_processed.pop()
    direction = node[0]
    x, y = node[1]
    if x < 0 or x >= len(data[0]) or y < 0 or y >= len(data):
      continue
    nexts = get_next(direction, (x, y), data)
    for n in nexts:
      nx, ny = n[1]
      if nx < 0 or nx >= len(data[0]) or ny < 0 or ny >= len(data):
        continue
      if not n[1] in energy:
        energy.append(n[1])
      if not (n[0], n[1]) in to_be_processed and (n[0], n[1]) not in processed:
        to_be_processed.append((n[0], n[1]))
    processed.append((node[0], node[1]))
  return len(energy)


print("--> test data <--")
test_input = load_data_from_file("test_input")
assert get_next(">", (0, 0), test_input) == [(">", (1, 0))]
assert get_next(">", (1, 0), test_input) == [("v", (1, 1))]
assert solve(test_input) == 46

print()
print("--> real data <--")
my_input = load_data_from_file("input")
print(f"\nanswer: {solve(my_input)}")
