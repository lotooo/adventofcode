#!/usr/bin/env python3
import re
import sys


def load_data_from_file(filename):
  """Load the input from a file and return the transformed version"""
  with open(filename, "r") as f:
    # data = list(map(prepare_data, f.readlines()))
    data = re.split(r"\n\n", f.read())
  return data


def prepare_data(x):
  """transform the data the way we want it for the puzzle"""
  return x.strip()


def get_next_range(initial_range_list, mappings, debug=False):
  if debug:
    print(f"{initial_range_list=}")
  next_ranges = []
  for initial_range in initial_range_list:
    if debug:
      print(f"{initial_range=}")
    result_range = []
    paused_at = None
    m = [(int(m[0]), int(m[1]), int(m[2])) for m in map(lambda x: x.split(), mappings)]
    if debug:
      print(f"{m=}")
    for i, (t, s, r) in enumerate(m):
      source_range = (s, s + r - 1)
      offset = t - s
      if initial_range[0] >= s and initial_range[1] < s + r:
        if debug:
          print(
            f"{initial_range} self_contained in the {source_range} range ({t=}/{offset=})"
          )
        result_range.append((initial_range[0] + offset, initial_range[1] + offset))
        continue
      if initial_range[1] < s or initial_range[0] >= s + r:
        if debug:
          print(f"{initial_range} is not contained in the {source_range} range")
        continue
      if initial_range[0] >= s and initial_range[1] >= s + r:
        if debug:
          print(f"{initial_range} starts in {source_range}")
          print(
            f"=> Adding {(initial_range[0]+offset,source_range[1]+offset)} ({t=}/{offset=})"
          )
        result_range.append((initial_range[0] + offset, source_range[1] + offset))
        if i == len(m) - 1:
          if debug:
            print("We are on last mapping. Adding the rest of the range now")
            print(f"=> Adding {(source_range[1]+1,initial_range[1])} ({t=}/{offset=})")
          result_range.append((source_range[1] + 1, initial_range[1]))
        continue
      if initial_range[0] < s and initial_range[1] >= s + r:
        if debug:
          print(f"{initial_range} is bigger than {source_range}")
        if i == 0:
          if debug:
            print("We are on first mapping. Adding the beggining of the initial range")
            print(f"==> Adding {(initial_range[0],source_range[0]-1)}")
          result_range.append((initial_range[0], source_range[0] - 1))
        if debug:
          print(
            f"=> Adding {(source_range[0]+offset, source_range[1] + offset)} ({t=}/{offset=})"
          )
        result_range.append((source_range[0] + offset, source_range[1] + offset))
        # debug=True
        continue
      if initial_range[1] < s + r:
        if debug:
          print(f"{initial_range} ends in {source_range}")
        if i == 0:
          if debug:
            print("We are on first mapping. Adding the beggining of the initial range")
            print(f"==> Adding {(initial_range[0],source_range[0]-1)}")
          result_range.append((initial_range[0], source_range[0] - 1))
        if debug:
          print(
            f"==> Adding {(source_range[0]+offset,initial_range[1]+offset)} ({t=}/{offset=})"
          )
        result_range.append((source_range[0] + offset, initial_range[1] + offset))
        continue
    if len(result_range) == 0:
      if debug:
        print(f"{initial_range} was out of the mappings. Adding it 'as is'")
      result_range.append((initial_range[0], initial_range[1]))
    if debug:
      print(f"{result_range=}")
    next_ranges.extend(result_range)

  if debug:
    for r in next_ranges:
      print(f"DEBUG: {r} => {len(range(r[0],r[1]+1))}")
    sys.exit(1)
  return next_ranges


def solve(data):
  """Solve the puzzle and return the solution"""
  debug = False
  seeds = list(map(lambda x: int(x), re.findall("\d+", data[0])))
  mappings = []
  for m in data[1:]:
    d = m.strip().split("\n")
    mappings.append(sorted(d[1:], key=lambda x: int(x.split()[1])))
  locations = []
  for i in range(0, len(seeds) - 1, 2):
    this_range = [(seeds[i], seeds[i] + seeds[i + 1] - 1)]
    for step, mapping in enumerate(mappings):
      this_range = get_next_range(this_range, mapping, debug)
    for r in this_range:
      locations.append(r[0])
  print(locations)
  return min(locations)


print("--> test data <--")
test_input = load_data_from_file("test_input")
assert solve(test_input) == 46

print()
print("--> real data <--")
my_input = load_data_from_file("input")
print(f"\nanswer: {solve(my_input)}")
