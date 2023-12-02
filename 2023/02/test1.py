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


def prepare_data(x):
    """transform the data the way we want it for the puzzle"""
    game_data = x.strip().split(":")
    game_sets = list(map(cleanup_set, game_data[1].split(";")))
    return game_sets


def solve(data):
    """Solve the puzzle and return the solution"""
    plausible_games_ids = []
    for game_id, game in enumerate(data):
        game_analysis = []
        for game_set in game:
            if game_set["red"] > 12 or game_set["green"] > 13 or game_set["blue"] > 14:
                game_analysis.append(False)
            else:
                game_analysis.append(True)
        if not False in game_analysis:
            plausible_games_ids.append(game_id + 1)
    return sum(plausible_games_ids)


print("--> test data <--")
test_input = load_data_from_file("test_input")
assert solve(test_input) == 8

print()
print("--> real data <--")
my_input = load_data_from_file("input")
print(f"\nanswer: {solve(my_input)}")
