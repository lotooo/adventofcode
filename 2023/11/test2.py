#!/usr/bin/env python3
from itertools import combinations


def load_data_from_file(filename):
  """Load the input from a file and return the transformed version"""
  with open(filename, "r") as f:
    data = list(map(prepare_data, f.readlines()))
  return data


def prepare_data(x):
  """transform the data the way we want it for the puzzle"""
  return x.strip()


class Universe:
  def __init__(self, data):
    self.lines = data

  @property
  def cols(self):
    cols = []
    for x, c in enumerate(self.lines[0]):
      col = ""
      for y, line in enumerate(self.lines):
        col += line[x]
      cols.append(col)
    return cols

  @property
  def empty_lines(self):
    empty_lines = []
    for y, line in enumerate(self.lines):
      if not "#" in line:
        empty_lines.append(y)
    return empty_lines

  @property
  def empty_cols(self):
    empty_cols = []
    for x, col in enumerate(self.cols):
      if not "#" in col:
        empty_cols.append(x)
    return empty_cols

  @property
  def galaxies(self):
    galaxies = []
    for y, line in enumerate(self.lines):
      for x, c in enumerate(line):
        if c == "#":
          galaxies.append((x, y))
    return galaxies

  def __str__(self):
    result = ""
    for y, line in enumerate(self.lines):
      for x, c in enumerate(line):
        result += c
      result += "\n"
    return result


def solve(data, expansion_ratio):
  """Solve the puzzle and return the solution"""
  u = Universe(data)
  pairs = list(combinations(u.galaxies, 2))
  distances = []
  for pair_id, (galaxy1, galaxy2) in enumerate(pairs):
    expanded_cols = [
      empty_col
      for empty_col in u.empty_cols
      if empty_col
      in range(min(galaxy1[0], galaxy2[0] + 1), max(galaxy1[0], galaxy2[0] + 1))
    ]
    expanded_lines = [
      empty_line
      for empty_line in u.empty_lines
      if empty_line
      in range(min(galaxy1[1], galaxy2[1] + 1), max(galaxy1[1], galaxy2[1] + 1))
    ]
    extra_horiz_distance = (expansion_ratio - 1) * len(expanded_cols)
    extra_vert_distance = (expansion_ratio - 1) * len(expanded_lines)
    d = abs(galaxy1[0] - galaxy2[0]) + abs(galaxy1[1] - galaxy2[1])
    distances.append(d + extra_horiz_distance + extra_vert_distance)
  return sum(distances)


print("--> test data <--")
test_input = load_data_from_file("test_input")
assert solve(test_input, 2) == 374

print("--> test data <--")
test_input = load_data_from_file("test_input")
assert solve(test_input, 10) == 1030

print("--> test data <--")
test_input = load_data_from_file("test_input")
assert solve(test_input, 100) == 8410

print()
print("--> real data <--")
my_input = load_data_from_file("input")
print(f"\nanswer: {solve(my_input,1000000)}")
