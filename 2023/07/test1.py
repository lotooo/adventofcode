#!/usr/bin/env python3
from collections import Counter


def load_data_from_file(filename):
  """Load the input from a file and return the transformed version"""
  with open(filename, "r") as f:
    data = list(map(prepare_data, f.readlines()))
  return data


def prepare_data(x):
  """transform the data the way we want it for the puzzle"""
  return Game(x)


class Game:
  def __init__(self, game):
    self.hand = game.strip().split()[0]
    self.bid = int(game.strip().split()[1])
    self.counter = Counter(self.hand)

  @property
  def base14score(self):
    mapping = {"T": 10, "J": 11, "Q": 12, "K": 13, "A": 14}
    base10number = 0
    for i, c in enumerate(reversed(self.hand)):
      if c in mapping:
        base10number += pow(14, i) * mapping[c]
      else:
        base10number += pow(14, i) * int(c)
    return base10number

  @property
  def base_score(self):
    if len(self.counter) == 5:
      # we have nothing
      return 0
    if len(self.counter) == 4:
      # we have one pair
      return 1
    if len(self.counter) == 3:
      if self.counter.most_common()[0][1] == 2:
        # It's a double pair
        return 2
      if self.counter.most_common()[0][1] == 3:
        # It's a the of a kind
        return 3
    if len(self.counter) == 2:
      if self.counter.most_common()[0][1] == 3:
        # It's a full house
        return 4
      if self.counter.most_common()[0][1] == 4:
        # It's a four of a kind
        return 5
    if len(self.counter) == 1:
      # It's a five of a kind
      return 6

  def __repr__(self):
    return self.hand

  def __str__(self):
    return f"hand={self.hand}/bid={self.bid}"

  def __gt__(self, another_game):
    if self.base_score > another_game.base_score:
      return True
    if self.base_score == another_game.base_score:
      if self.base14score > another_game.base14score:
        return True
      # print("Let's find a way")
    return False


def solve(data):
  """Solve the puzzle and return the solution"""
  sorted_game = sorted(data)
  score = 0
  for rank, game in enumerate(sorted_game):
    score += (rank + 1) * game.bid
  return score


print("--> test data <--")
test_input = load_data_from_file("test_input")
assert solve(test_input) == 6440

print()
print("--> real data <--")
my_input = load_data_from_file("input")
print(f"\nanswer: {solve(my_input)}")
