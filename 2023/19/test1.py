#!/usr/bin/env python3
import sys
import re

sys.path.append("../../")
from utils import *


def load_data_from_file(filename):
  """Load the input from a file and return the transformed version"""
  with open(filename, "r") as f:
    data = f.read().strip()
  return data.split("\n\n")


def prepare_workflows(x):
  """transform the data the way we want it for the puzzle"""
  w = x.strip()
  g = re.match(r"(\w+)\{(.*)\}", w)
  label = g.group(1)
  workflows = g.group(2).split(",")
  analysed_tests = []
  for workflow in workflows:
    analysed_tests.append(workflow.split(":"))
  return (label, analysed_tests)


def get_next(part, workflow):
  x = part["x"]
  m = part["m"]
  a = part["a"]
  s = part["s"]
  default = workflow[-1][0]
  for test in workflow[:-1]:
    if eval(test[0]):
      return test[1]
  return default


def prepare_parts(x):
  """transform the data the way we want it for the puzzle"""
  parts = x.strip()
  g = re.match(r"{x=(\d+),m=(\d+),a=(\d+),s=(\d+)", parts)
  return {
    "x": int(g.group(1)),
    "m": int(g.group(2)),
    "a": int(g.group(3)),
    "s": int(g.group(4)),
  }


def solve(data):
  """Solve the puzzle and return the solution"""
  wflws = list(map(prepare_workflows, data[0].split("\n")))
  workflows = {}
  for label, tests in wflws:
    workflows[label] = tests
  parts = list(map(prepare_parts, data[1].split("\n")))
  accepted = []
  for part in parts:
    workflow = "in"
    npart = part
    while workflow not in ["A", "R"]:
      workflow = get_next(npart, workflows[workflow])
    if workflow == "A":
      accepted.append(part)
  return sum([sum(a.values()) for a in accepted])


print("--> test data <--")
test_input = load_data_from_file("test_input")
assert solve(test_input) == 19114

print()
print("--> real data <--")
my_input = load_data_from_file("input")
print(f"\nanswer: {solve(my_input)}")
