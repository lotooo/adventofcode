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
  boxes = [[] for i in range(256)]
  for init_seq in data[0]:
    if "-" in init_seq:
      label = init_seq.split("-")[0]
      box = hash(label)
      lens_in_box = [lid for lid, lens in enumerate(boxes[box]) if lens[0] == label]
      if lens_in_box:
        boxes[box].pop(lens_in_box[0])
    else:
      label = init_seq.split("=")[0]
      box = hash(label)
      focal = init_seq.split("=")[1]
      lens_in_box = [lid for lid, lens in enumerate(boxes[box]) if lens[0] == label]
      if lens_in_box:
        boxes[box][lens_in_box[0]] = (label, focal)
      else:
        boxes[box].append((label, focal))
  total_focusing_power = 0
  for bid, box in enumerate(boxes):
    for lid, lens in enumerate(box):
      lens_focusins_power = (1 + bid) * (lid + 1) * int(lens[1])
      total_focusing_power += lens_focusins_power
  return total_focusing_power


print("--> unit test <--")
assert hash("HASH") == 52

print("--> test data <--")
test_input = load_data_from_file("test_input")
assert solve(test_input) == 145

print()
print("--> real data <--")
my_input = load_data_from_file("input")
print(f"\nanswer: {solve(my_input)}")
