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


def get_next_range(initial_range_list, mappings):
  debug = False
  print(f"{initial_range_list=}")
  ## Note for future self
  ## We must re-init that list or change our test
  ## to validate we are are the begining of the string or not
  result_range = []
  for initial_range in initial_range_list:
    beginning = True
    m = [(int(m[0]), int(m[1]), int(m[2])) for m in map(lambda x: x.split(), mappings)]
    # print(f"{m=}")
    paused_at = None
    for i, (t, s, r) in enumerate(m):
      source_range = (s, s + r - 1)
      offset = t - s
      if initial_range[0] >= s and initial_range[1] < s + r:
        print(
          f"{initial_range} self_contained in the {source_range} range ({t=}/{offset=})"
        )
        return [(initial_range[0] + offset, initial_range[1] + offset)]
      if initial_range[-1] < s:
        print(f"{initial_range} is not contained in the {source_range} range")
        continue
      if initial_range[0] >= s + r:
        print(f"{initial_range} is not contained in the {source_range} range")
        continue
      if initial_range[0] >= s and initial_range[1] >= s + r:
        print(f"{initial_range} starts in {source_range}")
        print(
          f"=> Adding {(initial_range[0]+offset,source_range[1]+offset)} ({t=}/{offset=})"
        )
        result_range.append((initial_range[0] + offset, source_range[1] + offset))
        # beginning = False
        paused_at = s + r
        continue
      if initial_range[0] < s and initial_range[1] >= s + r:
        print(f"{initial_range} is bigger than {source_range}")
        if beginning:
          print(f"==> Adding {(initial_range[0],source_range[0])}")
          result_range.append((initial_range[0], source_range[0] - 1))
          beginning = False
        result_range.append((source_range[0] + offset, source_range[1] + offset))
        # debug=True
        continue
      if initial_range[-1] < s + r:
        print(f"{initial_range} ends in {source_range}")
        if beginning:
          print(f"==> Adding {(initial_range[0],source_range[0])}")
          result_range.append((initial_range[0], source_range[0] - 1))
          beginning = False
        print(
          f"==> Adding {(source_range[0]+offset,initial_range[1]+offset)} ({t=}/{offset=})"
        )
        result_range.append((source_range[0] + offset, initial_range[1] + offset))
        continue
  if debug:
    print(result_range)
    sys.exit(1)
  if len(result_range) > 0 and paused_at:
    # print("not sure")
    # print(result_range)
    result_range.append((paused_at, initial_range[1]))
    # print(f"{result_range=}")
    return result_range
  elif len(result_range) > 0:
    return result_range
  else:
    return initial_range_list


def solve(data):
  """Solve the puzzle and return the solution"""
  seeds = list(map(lambda x: int(x), re.findall("\d+", data[0])))
  mappings = []
  for m in data[1:]:
    d = m.strip().split("\n")
    mappings.append(sorted(d[1:], key=lambda x: int(x.split()[1])))
  locations = []
  for i in range(0, len(seeds) - 1, 2):
    # print(f"Group {i}")
    this_range = [(seeds[i], seeds[i] + seeds[i + 1] - 1)]
    for step, mapping in enumerate(mappings):
      this_range = get_next_range(this_range, mapping)
      # print(f"{step=}")
      # print(f"Result: {this_range}")
      # for r in this_range:
      #  print(f"Min: {r[0]}")
      # print("")
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
