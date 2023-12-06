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


def solve(data):
  """Solve the puzzle and return the solution"""
  result = 1
  race_duration = int("".join(re.findall("\d+", data[0])))
  distance_to_beat = int("".join(re.findall("\d+", data[1])))
  done = False
  wait = 1
  while not done:
    d = (race_duration - wait) * wait
    if d > distance_to_beat:
      done = True
    else:
      wait += 1
  # Add 1 because we didn't try the "don't push the button option
  return race_duration - wait * 2 + 1


print("--> test data <--")
test_input = load_data_from_file("test_input")
assert solve(test_input) == 71503

print()
print("--> real data <--")
my_input = load_data_from_file("input")
print(f"\nanswer: {solve(my_input)}")
