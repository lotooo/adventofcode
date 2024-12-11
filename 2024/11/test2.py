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
    return x.strip().split()


def single_stone_move(stone):
    new_stones = []
    if stone == "0":
        new_stones.append("1")
    elif len(stone) % 2 == 0:
        middle_index = len(stone) // 2
        left_stone = stone[:middle_index]
        right_stone = stone[middle_index:]
        if int(left_stone) != 0:
            new_stones.append(left_stone.lstrip("0"))
        else:
            new_stones.append("0")
        if int(right_stone) != 0:
            new_stones.append(right_stone.lstrip("0"))
        else:
            new_stones.append("0")
    elif len(stone) % 2 == 1:
        new_stones.append(str(2024 * int(stone)))

    return new_stones


def move(stones):
    new_stones = []
    for stone in stones:
        if stone == "0":
            new_stones.append("1")
        elif len(stone) % 2 == 0:
            middle_index = len(stone) // 2
            left_stone = stone[:middle_index]
            right_stone = stone[middle_index:]
            if int(left_stone) != 0:
                new_stones.append(left_stone.lstrip("0"))
            else:
                new_stones.append("0")
            if int(right_stone) != 0:
                new_stones.append(right_stone.lstrip("0"))
            else:
                new_stones.append("0")
        elif len(stone) % 2 == 1:
            new_stones.append(str(2024 * int(stone)))
    return new_stones


def get_result(stone, iteration, cache, cache_per_iteration):
    cache_key = f"{stone}_{iteration}"
    if cache_key in cache_per_iteration:
        return cache_per_iteration[cache_key]
    if iteration == 1:
        return len(cache[stone])
    else:
        result = 0
        for s in cache[stone]:
            result += get_result(s, iteration - 1, cache, cache_per_iteration)
        cache_per_iteration[cache_key] = result
        return result


def solve(data, iteration=25):
    """Solve the puzzle and return the solution"""
    stones = data[0]
    print(f"Start: {stones} / {iteration=}")
    print("Building cache")
    cache = {}
    to_process = []
    for s in stones:
        to_process.append(s)
    while len(to_process) > 0:
        stone = to_process.pop()
        if stone in cache:
            continue
        else:
            nexts = move([stone])
            cache[stone] = nexts
            for n in nexts:
                if n not in cache:
                    to_process.append(n)
    result = 0
    cache_per_iteration = {}
    for stone in stones:
        print(f"Getting result for {stone}")
        result += get_result(stone, iteration, cache, cache_per_iteration)
    return result


print("--> test data <--")
test_input = load_data_from_file("test_input")
test_input2 = load_data_from_file("test_input2")
assert solve(test_input, 1) == 7
assert solve(test_input2, 6) == 22
assert solve(test_input2, 25) == 55312

print()
print("--> real data <--")
my_input = load_data_from_file("input")
print(f"\nanswer: {solve(my_input,75)}")
