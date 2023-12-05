#!/usr/bin/env python3
import re


def load_data_from_file(filename):
  """Load the input from a file and return the transformed version"""
  with open(filename, "r") as f:
    # data = list(map(prepare_data, f.readlines()))
    data = re.split(r"\n\n", f.read())
  return data


def prepare_data(x):
  """transform the data the way we want it for the puzzle"""
  return x.strip()


def get_next(item, mappings):
  i = 0
  done = False
  target, source, myrange = map(lambda x: int(x), mappings[0].split())
  if item < source:
    return item
  while i < len(mappings):
    target, source, myrange = map(lambda x: int(x), mappings[i].split())
    if item - source < 0:
      done = True
      break
    i += 1
  if item > target + myrange and item > source > myrange:
    done = True
    return item
  if not done:
    print("ERROR: Something to investigate ?")
  target, source, myrange = map(lambda x: int(x), mappings[i - 1].split())
  return target + item - source


def solve(data):
  """Solve the puzzle and return the solution"""
  seeds = list(map(lambda x: int(x), re.findall("\d+", data[0])))
  mappings = []
  for m in data[1:]:
    d = m.strip().split("\n")
    mappings.append(sorted(d[1:], key=lambda x: int(x.split()[1])))
  locations = []
  for item in seeds:
    for step, mapping in enumerate(mappings):
      item = get_next(item, mapping)
    locations.append(item)
  return min(locations)


print("--> test data <--")
test_input = load_data_from_file("test_input")
assert solve(test_input) == 35

print()
print("--> real data <--")
my_input = load_data_from_file("input")
print(f"\nanswer: {solve(my_input)}")
