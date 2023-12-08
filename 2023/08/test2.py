#!/usr/bin/env python3
import re
from math import lcm


def load_data_from_file(filename):
  """Load the input from a file and return the transformed version"""
  with open(filename, "r") as f:
    data = list(map(prepare_data, f.readlines()))
  return data


def prepare_data(x):
  """transform the data the way we want it for the puzzle"""
  return x.strip()


def find_next(item, instruction, maps):
  return maps[item][instruction]


def solve(data):
  """Solve the puzzle and return the solution"""
  instructions = data[0]
  maps = {}
  for line in data[2:]:
    key, left, right = re.findall(r"[0-9A-Z]+", line)
    maps[key] = {}
    maps[key]["L"] = left
    maps[key]["R"] = right

  # Find starting positions of ghosts
  ghosts = [k for k in maps.keys() if k[2] == "A"]

  final = []
  for ghost in ghosts:
    i = 0
    while ghost[2] != "Z":
      ghost = find_next(ghost, instructions[i % len(instructions)], maps)
      i += 1
    final.append(i)
  return lcm(*final)


print("--> test data <--")
test_input = load_data_from_file("test_input_step2")
assert solve(test_input) == 6

print()
print("--> real data <--")
my_input = load_data_from_file("input")
print(f"\nanswer: {solve(my_input)}")
