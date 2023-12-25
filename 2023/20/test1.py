#!/usr/bin/env python3
import sys

sys.path.append("../../")
from utils import *


class Module:
  prevs = set()
  nexts = []
  name = "noname"
  inputs = {}
  outputs = {}
  state = None

  def init(self):
    self.outputs = {}

  def signal(self, s, prev_module=None):
    pass

  def send(self, s):
    for output_module in self.nexts:
      self.outputs[output_module] = s

  def __str__(self):
    return f"{self.name}: {self.prevs=} - {self.nexts=} - {self.outputs=}"


class FlipFlop(Module):
  def __init__(self):
    self.state = 0
    self.prevs = set()
    self.nexts = []
    self.name = "noname"
    self.inputs = {}
    self.outputs = {}

  def signal(self, s, prev_module=None):
    if s != 1:
      if self.state:
        self.send(0)
      else:
        self.send(1)
      self.state = (self.state + 1) % 2
    else:
      self.outputs = {}


class Conjunction(Module):
  def __init__(self):
    self.prevs = set()
    self.nexts = []
    self.name = "noname"
    self.inputs = {}
    self.outputs = {}

  def init(self):
    self.outputs = {}
    if self.inputs == {}:
      for input_module in self.prevs:
        self.inputs[input_module] = 0

  def signal(self, s, prev_module=None):
    if prev_module not in self.inputs:
      raise "This module is not linked"
    self.inputs[prev_module] = s
    if sum(self.inputs.values()) == len(self.prevs):
      self.send(0)
    else:
      self.send(1)


class Broadcaster(Module):
  def __init__(self):
    self.prevs = set()
    self.nexts = []
    self.name = "noname"
    self.inputs = {}
    self.outputs = {}

  def signal(self, s, prev_module=None):
    self.send(s)


def load_data_from_file(filename):
  """Load the input from a file and return the transformed version"""
  with open(filename, "r") as f:
    data = list(map(prepare_data, f.readlines()))
  return data


def prepare_data(x):
  """transform the data the way we want it for the puzzle"""
  return x.strip()


def solve(data, iterations):
  """Solve the puzzle and return the solution"""

  # First, let's build a beautiful dict of modules
  module_type = {
    "&": Conjunction,
    "%": FlipFlop,
    "b": Broadcaster,
  }
  modules = {}
  for module in data:
    label, outputs = module.split(" -> ")
    if label == "broadcaster":
      name = label
    else:
      name = label[1:]
    modules[name] = module_type[label[0]]()
    modules[name].name = name
    modules[name].nexts = outputs.split(", ")
  modules["output"] = Module()
  modules["output"].name = "output"
  modules["rx"] = Module()
  modules["rx"].name = "rx"

  # Now let's link them all together (we need the input for the Conjunction ones)
  for mod_name, mod in modules.items():
    for mod_next in mod.nexts:
      modules[mod_next].prevs.add(mod_name)

  lows = 0
  highs = 0
  for i in range(iterations):
    # don't forget the button
    lows += 1
    current_module = "broadcaster"
    for m in modules.values():
      m.init()
    to_process = [("broadcaster", 0, None)]
    while len(to_process) > 0:
      current_module, s, prev_module = to_process.pop(0)
      # print(f"Analysing {current_module}")
      modules[current_module].signal(s, prev_module=prev_module)
      for mod_next, signal in modules[current_module].outputs.items():
        to_process.append((mod_next, signal, current_module))
        if signal == 1:
          highs += 1
        if signal == 0:
          lows += 1
  return highs * lows


print("--> test data <--")
test_input = load_data_from_file("test_input")
assert solve(test_input, 1) == 32
assert solve(test_input, 1000) == 32000000

print("--> test data2 <--")
test_input = load_data_from_file("test_input2")
assert solve(test_input, 1000) == 11687500

print()
print("--> real data <--")
my_input = load_data_from_file("input")
print(f"\nanswer: {solve(my_input,1000)}")
