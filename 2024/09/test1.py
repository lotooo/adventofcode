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


def unpack(string):
    """Extract file from compressed string"""
    out = []
    i = 0
    while i < len(string):
        if i % 2 == 0:
            out.extend([str(int(i / 2))] * int(string[i]))
        else:
            out.extend(int(string[i]) * ["."])
        i += 1
    return out


def move(file):
    while file[-1] == ".":
        file.pop()
    f = file
    if "." not in f:
        return f
    last_number = f[-1]
    f = f[:-1]
    f[f.index(".")] = last_number
    return f


def get_checksum(file):
    checksum = []
    for i, char in enumerate(file):
        checksum.append(i * int(char))
    return checksum


def solve(data):
    """Solve the puzzle and return the solution"""
    s = unpack(data[0])
    while "." in s:
        s = move(s)
    return sum(get_checksum(s))


print("--> unit test <--")
assert "".join(unpack("12345")) == "0..111....22222"
assert (
    "".join(unpack("2333133121414131402"))
    == "00...111...2...333.44.5555.6666.777.888899"
)
assert (
    solve(["12345"])
    == 0 * 0 + 2 * 1 + 2 * 2 + 1 * 3 + 1 * 4 + 1 * 5 + 2 * 6 + 2 * 7 + 2 * 8
)
assert solve(["123456789"]) == 897
assert solve(["123456789123456789"]) == 4606
# print("".join(unpack("123456789123456789123456789123456789")))
assert solve(["123456789123456789123456789123456789"]) == 37335
assert solve(["1234567891234567890123456789123456789"]) == 39134

print("--> test data <--")
test_input = load_data_from_file("test_input")
# assert move(test_input[0]) == "0099811188827773336446555566"
assert solve(test_input) == 1928

print()
print("--> real data <--")
my_input = load_data_from_file("input")
print(f"\nanswer: {solve(my_input)}")
