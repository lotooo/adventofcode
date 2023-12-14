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


def solve(data):
  """Solve the puzzle and return the solution"""
  rotated = rotate_matrix(data)
  score = 0
  for column in rotated:
    new_column = []
    for block in column.split("#")[::-1]:
      # it might be stupid to reverse twice everything to properly count the load
      # Let's use the already reversed column
      new_column.append("".join(sorted(block)))
    r = [score + 1 for score, c in enumerate("#".join(new_column)) if c == "O"]
    score += sum(r)
  return score


print("--> test data <--")
test_input = load_data_from_file("test_input")
assert solve(test_input) == 136

print()
print("--> real data <--")
my_input = load_data_from_file("input")
print(f"\nanswer: {solve(my_input)}")
