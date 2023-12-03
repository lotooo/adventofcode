#!/usr/bin/env python3
import re


def load_data_from_file(filename):
  """Load the input from a file and return the transformed version"""
  with open(filename, "r") as f:
    data = list(map(prepare_data, f.readlines()))
  return data


def prepare_data(x):
  """transform the data the way we want it for the puzzle"""
  return x.strip()


def is_valid(grid, line_id, number, start_index):
  """Test if a number is valid"""
  is_valid = []
  start = grid[line_id][start_index:].find(number) + start_index
  end = start + len(number) - 1
  for x in [start - 1, end + 1]:
    for y in [line_id - 1, line_id, line_id + 1]:
      if x < 0 or y < 0 or x >= len(grid[0]) or y >= len(grid):
        continue
      if grid[y][x] != ".":
        is_valid.append(True)
      else:
        is_valid.append(False)
  for x in range(start, end + 1):
    for y in [line_id - 1, line_id + 1]:
      if x < 0 or y < 0 or x >= len(grid[0]) or y >= len(grid):
        continue
      if grid[y][x] != ".":
        is_valid.append(True)
      else:
        is_valid.append(False)
  return True in is_valid


def solve(data):
  """Solve the puzzle and return the solution"""
  part_numbers = []
  for line_id, line in enumerate(data):
    numbers = re.findall(r"\d+", line)
    # Just in case the same number appears twice, let's not scan the full line
    # But save the last posiion in the string instead
    start_index = 0
    for number in numbers:
      if is_valid(data, line_id, number, start_index):
        part_numbers.append(int(number))
      start_index = data[line_id].find(number) + len(number)
  return sum(part_numbers)


print("--> test data <--")
test_input = load_data_from_file("test_input")
assert solve(test_input) == 4361

print()
print("--> real data <--")
my_input = load_data_from_file("input")
print(f"\nanswer: {solve(my_input)}")
