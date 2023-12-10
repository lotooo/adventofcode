#!/usr/bin/env python3
def load_data_from_file(filename):
  """Load the input from a file and return the transformed version"""
  with open(filename, "r") as f:
    data = list(map(prepare_data, f.readlines()))
  return data


def prepare_data(x):
  """transform the data the way we want it for the puzzle"""
  return list(map(lambda x: int(x), x.strip().split()))


def get_next(history):
  old = [history]
  while sum(old[-1]) != 0:
    tmp = []
    for i in range(len(old[-1]) - 1):
      tmp.append(old[-1][i + 1] - old[-1][i])
    old.append(tmp)
  # Discover next now !
  old[-1].append(0)
  for i in range(len(old) - 2, -1, -1):
    old[i].append(old[i][-1] + old[i + 1][-1])
  # Print it for debugging
  for h in old:
    print(h)
  print("")
  return old[0][-1]


def solve(data):
  """Solve the puzzle and return the solution"""
  nexts = []
  for history in data:
    nexts.append(get_next(history))
  print(f"{nexts=}")
  return sum(nexts)


print("--> test data <--")
test_input = load_data_from_file("test_input")
assert solve(test_input) == 114

print()
print("--> real data <--")
my_input = load_data_from_file("input")
print(f"\nanswer: {solve(my_input)}")
