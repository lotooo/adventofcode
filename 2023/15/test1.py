#!/usr/bin/env python3
import sys

sys.path.append("../../")
from utils import *


def load_data_from_file(filename):
  """Load the input from a file and return the transformed version"""
  with open(filename, "r") as f:
    data = list(map(prepare_data, f.readlines()))
  return data


def hash(string):
  result = 0
  for c in string:
    result += ord(c)
    result *= 17
    result = result % 256
  return result


def prepare_data(x):
  """transform the data the way we want it for the puzzle"""
  return x.strip().split(",")


def solve(data):
  """Solve the puzzle and return the solution"""
  result = []
  for init_seq in data[0]:
    result.append(hash(init_seq))
  return sum(result)


print("--> unit test <--")
assert hash("HASH") == 52

print("--> test data <--")
test_input = load_data_from_file("test_input")
assert solve(test_input) == 1320

print()
print("--> real data <--")
my_input = load_data_from_file("input")
print(f"\nanswer: {solve(my_input)}")
