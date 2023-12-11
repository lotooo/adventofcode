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

  def expand(self):
    new_line_size = len(self.lines[0]) + len(self.empty_cols)
    new_col_size = len(self.lines) + len(self.empty_lines)
    new_tmp_universe = self.lines.copy()
    for offset, num_line in enumerate(self.empty_lines):
      new_tmp_universe.insert(num_line + offset, new_line_size * ".")
    new_universe = []
    for y, line in enumerate(new_tmp_universe):
      if len(line) != new_line_size:
        tmp_line = list(line)
        for offset, num_col in enumerate(self.empty_cols):
          tmp_line.insert(1 + num_col + offset, ".")
          new_line = "".join(tmp_line)
      else:
        new_line = line
      new_universe.append(new_line)
    self.lines = new_universe

  def __str__(self):
    result = ""
    for y, line in enumerate(self.lines):
      for x, c in enumerate(line):
        result += c
      result += "\n"
    return result


def solve(data):
  """Solve the puzzle and return the solution"""
  u = Universe(data)
  u.expand()
  pairs = combinations(u.galaxies, 2)
  distances = []
  for galaxy1, galaxy2 in pairs:
    d = abs(galaxy1[0] - galaxy2[0]) + abs(galaxy1[1] - galaxy2[1])
    distances.append(d)
  return sum(distances)


print("--> test data <--")
test_input = load_data_from_file("test_input")
assert solve(test_input) == 374

print()
print("--> real data <--")
my_input = load_data_from_file("input")
print(f"\nanswer: {solve(my_input)}")
