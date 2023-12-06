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
  times = list(map(lambda x: int(x), re.findall("\d+", data[0])))
  distances = list(map(lambda x: int(x), re.findall("\d+", data[1])))
  for race in range(len(times)):
    winning_games_options = 0
    race_duration = times[race]
    distance_to_beat = distances[race]
    done = False
    wait = 1
    last_d = 0
    while not done:
      d = (race_duration - wait) * wait
      if last_d <= d:
        growing = True
      else:
        growing = False
      if d > distance_to_beat:
        winning_games_options += 1
      elif growing == False:
        # it's not a winning game and the distance is decreasing
        # let's stop
        break
      if wait == race_duration:
        break
      wait += 1
      last_d = d
    result *= winning_games_options
  return result


print("--> test data <--")
test_input = load_data_from_file("test_input")
assert solve(test_input) == 288

print()
print("--> real data <--")
my_input = load_data_from_file("input")
print(f"\nanswer: {solve(my_input)}")
