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
    self.id = int(re.search(r"(\d+)", data.split("|")[0].split(":")[0]).group(1))
    self.winning_numbers = re.findall(r"\d+", data.split("|")[0].split(":")[1])
    self.my_numbers = re.findall(r"\d+", data.split("|")[1])

  @property
  def score(self):
    return len([n for n in self.my_numbers if n in self.winning_numbers])


def prepare_data(x):
  """transform the data the way we want it for the puzzle"""
  return Card(x.strip())


def solve(data):
  """Solve the puzzle and return the solution"""
  cards = {c.id: 1 for c in data}
  for i in range(1, len(data) + 1):
    for doubling_card_id in range(i + 1, i + data[i - 1].score + 1):
      cards[doubling_card_id] += cards[i]
  return sum(cards.values())


print("--> test data <--")
test_input = load_data_from_file("test_input")
assert solve(test_input) == 30

print()
print("--> real data <--")
my_input = load_data_from_file("input")
print(f"\nanswer: {solve(my_input)}")
