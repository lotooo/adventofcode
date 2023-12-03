#!/usr/bin/env python3
import re
from collections import defaultdict


def load_data_from_file(filename):
  """Load the input from a file and return the transformed version"""
  with open(filename, "r") as f:
    data = list(map(prepare_data, f.readlines()))
  return data


def prepare_data(x):
  """transform the data the way we want it for the puzzle"""
  return x.strip()


def gear_finder(grid, line_id, number, start_index):
  """Test if a number is valid"""
  debug = False
  gear = []
  start = grid[line_id][start_index:].find(number) + start_index
  end = start + len(number) - 1
  for x in [start - 1, end + 1]:
    for y in [line_id - 1, line_id, line_id + 1]:
      if x < 0 or y < 0 or x >= len(grid[0]) or y >= len(grid):
        continue
      if grid[y][x] == "*":
        gear.append((y, x))
  for x in range(start, end + 1):
    for y in [line_id - 1, line_id + 1]:
      if x < 0 or y < 0 or x >= len(grid[0]) or y >= len(grid):
        continue
      if grid[y][x] == "*":
        gear.append((y, x))
  return gear


def solve(data):
  """Solve the puzzle and return the solution"""
  gear_ratios = []
  gears = defaultdict(list)
  for line_id, line in enumerate(data):
    numbers = re.findall(r"\d+", line)
    # Just in case the same number appears twice, let's not scan the full line
    # But save the last posiion in the string instead
    start_index = 0
    for number in numbers:
      gear = gear_finder(data, line_id, number, start_index)
      start_index = data[line_id].find(number) + len(number)
      for g in gear:
        gears[g].append(number)
  for g, parts in gears.items():
    if len(parts) == 2:
      gear_ratios.append(int(parts[0]) * int(parts[1]))
  return sum(gear_ratios)


print("--> test data <--")
test_input = load_data_from_file("test_input")
assert solve(test_input) == 467835

print()
print("--> real data <--")
my_input = load_data_from_file("input")
print(f"\nanswer: {solve(my_input)}")
