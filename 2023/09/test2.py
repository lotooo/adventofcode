#!/usr/bin/env python3
def load_data_from_file(filename):
  """Load the input from a file and return the transformed version"""
  with open(filename, "r") as f:
    data = list(map(prepare_data, f.readlines()))
  return data


def prepare_data(x):
  """transform the data the way we want it for the puzzle"""
  return list(map(lambda x: int(x), x.strip().split()))


def get_next(history, debug=False):
  old = [history]
  while False in map(lambda x: x == 0, old[-1]):
    tmp = []
    for i in range(len(old[-1]) - 1):
      tmp.append(old[-1][i + 1] - old[-1][i])
    old.append(tmp)

  # Discover next now !
  old[-1].insert(0, 0)
  for i in range(len(old) - 2, -1, -1):
    old[i].insert(0, old[i][0] - old[i + 1][0])
  if debug:
    # Print it for debugging
    for h in old:
      print(h)
    print("")
  return old[0][0]


def solve(data):
  """Solve the puzzle and return the solution"""
  nexts = []
  debug = False
  for history in data:
    nexts.append(get_next(history, debug))
  return sum(nexts)


print("--> test data <--")
test_input = load_data_from_file("test_input")
assert solve(test_input) == 2

print()
print("--> real data <--")
my_input = load_data_from_file("input")
print(f"\nanswer: {solve(my_input)}")
