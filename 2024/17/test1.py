#!/usr/bin/env python3
import sys

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


class Computer:
    def __init__(self, register):
        self.register = register
        self.o = []

    def combo(self, operand):
        if operand < 4:
            return operand
        if operand == 4:
            return self.register["A"]
        if operand == 5:
            return self.register["B"]
        if operand == 6:
            return self.register["C"]
        raise Exception(f"{operand} is not a valid operand")

    def adv(self, operand):
        self.register["A"] = self.register["A"] // pow(2, self.combo(operand))

    def bdv(self, operand):
        self.register["B"] = self.register["A"] // pow(2, self.combo(operand))

    def cdv(self, operand):
        self.register["C"] = self.register["A"] // pow(2, self.combo(operand))

    def bxl(self, operand):
        self.register["B"] = self.register["B"] ^ operand

    def bxc(self, operand):
        self.register["B"] = self.register["B"] ^ self.register["C"]

    def bst(self, operand):
        self.register["B"] = self.combo(operand) % 8

    def out(self, operand):
        self.o.append(self.combo(operand) % 8)

    def compute(self, opcode, operand):
        if opcode == 0:
            self.adv(operand)
        if opcode == 1:
            self.bxl(operand)
        if opcode == 2:
            self.bst(operand)
        if opcode == 4:
            self.bxc(operand)
        if opcode == 5:
            self.out(operand)
        if opcode == 6:
            self.bdv(operand)
        if opcode == 7:
            self.cdv(operand)

    def run(self, program):
        instruction_pointer = 0
        while instruction_pointer < len(program):
            opcode = program[instruction_pointer]
            operand = program[instruction_pointer + 1]
            self.compute(opcode, operand)
            if opcode == 3 and self.register["A"] != 0:
                instruction_pointer = operand
            else:
                instruction_pointer += 2

    def __repr__(self):
        return f"A: {self.register['A']} / B: {self.register['B']} / C: {self.register['C']} / out: {self.o}"

    def __str__(self):
        return ",".join(map(str, self.o))


def solve(data):
    """Solve the puzzle and return the solution"""
    register = {}
    register["A"] = int(data[0].split()[2])
    register["B"] = int(data[1].split()[2])
    register["C"] = int(data[2].split()[2])
    program = list(map(int, data[4].split()[1].split(",")))
    computer = Computer(register)
    computer.run(program)
    return str(computer)


print("--> unit test 1 <--")
c = Computer({"A": 0, "B": 0, "C": 9})
c.run([2, 6])
assert c.register["A"] == 0 and c.register["B"] == 1 and c.register["C"] == 9
print("--> unit test 2 <--")
c = Computer({"A": 10, "B": 0, "C": 0})
c.run([5, 0, 5, 1, 5, 4])
assert str(c) == "0,1,2"
print("--> unit test 3 <--")
c = Computer({"A": 2024, "B": 0, "C": 0})
c.run([0, 1, 5, 4, 3, 0])
assert str(c) == "4,2,5,6,7,7,7,7,3,1,0"
assert c.register["A"] == 0
print("--> unit test 4 <--")
c = Computer({"A": 0, "B": 29, "C": 0})
c.run([1, 7])
assert c.register["B"] == 26
print("--> unit test 5 <--")
c = Computer({"A": 0, "B": 2024, "C": 43690})
c.run([4, 0])
assert c.register["B"] == 44354

print("--> test data <--")
test_input = load_data_from_file("test_input")
assert solve(test_input) == "4,6,3,5,6,3,5,2,1,0"

print()
print("--> real data <--")
my_input = load_data_from_file("input")
print(f"\nanswer: {solve(my_input)}")
