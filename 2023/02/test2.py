#!/usr/bin/env python3
import re


def load_data_from_file(filename):
    """Load the input from a file and return the transformed version"""
    with open(filename, "r") as f:
        data = list(map(prepare_data, f.readlines()))
    return data


def cleanup_set(game_set):
    """Transform a game set on something we can use"""
    clean_game_set = {"red": 0, "green": 0, "blue": 0}
    for color_pickup in game_set.split(","):
        m = re.search(r"(\d+) (red|green|blue)", color_pickup)
        if m:
            clean_game_set[m.group(2)] += int(m.group(1))
        else:
            print(f"ERROR: {color_pickup=}")
    return clean_game_set


def get_max(hands, color):
    return max([h[color] for h in hands if h[color] != 0])


def prepare_data(x):
    """transform the data the way we want it for the puzzle"""
    game_data = x.strip().split(":")
    game_sets = list(map(cleanup_set, game_data[1].split(";")))
    return game_sets


def solve(data):
    """Solve the puzzle and return the solution"""
    game_powers = []
    for game_id, game in enumerate(data):
        game_power = 1
        for color in ["red", "blue", "green"]:
            game_power *= get_max(game, color)
        game_powers.append(game_power)
    return sum(game_powers)


print("--> test data <--")
test_input = load_data_from_file("test_input")
assert solve(test_input) == 2286

print()
print("--> real data <--")
my_input = load_data_from_file("input")
print(f"\nanswer: {solve(my_input)}")
