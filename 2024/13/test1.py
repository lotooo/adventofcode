#!/usr/bin/env python3
import re
import sys
from itertools import batched

sys.path.append("../../")
from utils import *


def load_data_from_file(filename):
    """Load the input from a file and return the transformed version"""
    with open(filename, "r") as f:
        data = list(map(prepare_data, f.readlines()))
    return data


def prepare_data(x):
    """transform the data the way we want it for the puzzle"""
    return x.strip()


class ClawMachine:
    def __init__(self, claw_machine):
        a = re.findall(r"\d+", claw_machine[0])
        b = re.findall(r"\d+", claw_machine[1])
        p = re.findall(r"\d+", claw_machine[2])

        self.ax = int(a[0])
        self.ay = int(a[1])
        self.bx = int(b[0])
        self.by = int(b[1])
        self.px = int(p[0])
        self.py = int(p[1])

    def __repr__(self):
        return f"{self.ax=}/{self.ay=}|{self.bx=}{self.by=}|{self.px=}/{self.py=}"


def solve(data, max_push=100):
    """Solve the puzzle and return the solution"""
    solutions = []
    for claw_machine in batched(data, 4):
        solution = None
        c = ClawMachine(claw_machine)
        ai = 1
        while ai < max_push + 1:
            bi = 1
            if solution is not None:
                break
            while bi < max_push + 1:
                posx = ai * c.ax + bi * c.bx
                posy = ai * c.ay + bi * c.by
                if posx == c.px and posy == c.py:
                    solution = (ai, bi)
                    break
                bi += 1
            ai += 1
        if solution is not None:
            solutions.append(solution)
    cost = map(lambda x: x[0] * 3 + x[1], solutions)
    return sum(cost)


print("--> test data <--")
test_input = load_data_from_file("test_input")
assert solve(test_input) == 480

print()
print("--> real data <--")
my_input = load_data_from_file("input")
print(f"\nanswer: {solve(my_input)}")
