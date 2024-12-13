#!/usr/bin/env python3
import re
import sys
from itertools import batched
from math import gcd

sys.path.append("../../")
from utils import cramer_2x2


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
        self.px = 10000000000000 + int(p[0])
        self.py = 10000000000000 + int(p[1])

    def __repr__(self):
        return f"{self.ax=}/{self.ay=}|{self.bx=}{self.by=}|{self.px=}/{self.py=}"


def solve(data):
    """Solve the puzzle and return the solution"""
    solutions = []
    for claw_machine in batched(data, 4):
        solution = None
        c = ClawMachine(claw_machine)
        solution = cramer_2x2(c.ax, c.bx, c.px, c.ay, c.by, c.py)
        if solution is not None:
            if solution[0] < 0 or solution[1] < 0:
                continue
            if not solution[0].is_integer() or not solution[1].is_integer():
                continue
            solutions.append(solution)
    cost = map(lambda x: x[0] * 3 + x[1], solutions)
    return int(sum(cost))


print("--> test data <--")
# test_input = load_data_from_file("test_input")
# assert solve(test_input) == 480

print()
print("--> real data <--")
my_input = load_data_from_file("input")
print(f"\nanswer: {solve(my_input)}")
