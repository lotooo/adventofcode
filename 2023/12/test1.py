#!/usr/bin/env python3
import re
from itertools import product


def load_data_from_file(filename):
  """Load the input from a file and return the transformed version"""
  with open(filename, "r") as f:
    data = list(map(prepare_data, f.readlines()))
  return data


def prepare_data(x):
  """transform the data the way we want it for the puzzle"""
  return x.strip().split()


def solve(data):
  """Solve the puzzle and return the solution"""
  result = 0
  for springs, stats in data:
    unknowns = re.findall(r"\?", springs)
    replacements = product("#.", repeat=len(unknowns))
    for r in replacements:
      replacement = list(r)
      new_springs = ""
      for i in springs:
        if i == "?":
          new_springs += replacement.pop(0)
        else:
          new_springs += i
      groups = re.findall(r"#+", new_springs)
      pattern = ",".join([str(len(g)) for g in groups])
      if pattern == stats:
        result += 1
  return result


print("--> test data <--")
test_input = load_data_from_file("test_input")
assert solve(test_input) == 21

print()
print("--> real data <--")
my_input = load_data_from_file("input")
print(f"\nanswer: {solve(my_input)}")
