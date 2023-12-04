#!/usr/bin/env python3
import re


def load_data_from_file(filename):
  """Load the input from a file and return the transformed version"""
  with open(filename, "r") as f:
    data = list(map(prepare_data, f.readlines()))
  return data


class Card:
  """Define a card in thei Dec 04th game"""

  def __init__(self, data):
    self.winning_numbers = re.findall(r"\d+", data.split("|")[0].split(":")[1])
    self.my_numbers = re.findall(r"\d+", data.split("|")[1])

  @property
  def score(self):
    my_winning_numbers = [n for n in self.my_numbers if n in self.winning_numbers]
    if len(my_winning_numbers) == 0:
      return 0
    return pow(2, len(my_winning_numbers) - 1)


def prepare_data(x):
  """transform the data the way we want it for the puzzle"""
  return Card(x.strip())


def solve(data):
  """Solve the puzzle and return the solution"""
  return sum([card.score for card in data])


print("--> test data <--")
test_input = load_data_from_file("test_input")
assert solve(test_input) == 13

print()
print("--> real data <--")
my_input = load_data_from_file("input")
print(f"\nanswer: {solve(my_input)}")
