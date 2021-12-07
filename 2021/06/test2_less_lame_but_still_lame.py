#!/usr/bin/env python3
from collections import Counter
def load_data_from_file(filename):
    """ Load the input from a file and return the transformed version """
    with open(filename, 'r') as f:
        data = list(map(prepare_data, f.readlines()))
    return data[0]


def prepare_data(x):
    """ transform the data the way we want it for the puzzle """
    return list(map(int,x.split(',')))


def fish_counter(timer, last_day=18, day=0, fork=0):
        fish_count = 1
        while(day < last_day):
            if timer == 0:
                fish_count += fish_counter(8, last_day=last_day, day=day+1, fork=1)
                day_increment = 7
            else:
                timer -= 1
                day_increment = 1
            day += day_increment 
        return fish_count


def solve(data, total_days):
    """ Solve the puzzle and return the solution """
    fish_count = 0
    fish_spread = Counter(data)
    for fish_timer, count in fish_spread.items():
        print(f"{count} fishes with timer {fish_timer}")
        fish_count += count * fish_counter(fish_timer, last_day=total_days,day=0)
    print(f"total: {fish_count}")
    return fish_count


print("--> test data <--")
test_input = load_data_from_file('test_input')
print(f"Initial state: {test_input}")
assert solve([3], 18) == 5
assert solve([4], 18) == 4
assert solve([1], 18) == 7
assert solve([2], 18) == 5
assert solve(test_input, 18) == 26
assert solve(test_input, 80) == 5934
assert solve(test_input, 256) == 26984457539

print()
print("--> real data <--")
my_input = load_data_from_file('input')
print(f"\nanswer: {solve(my_input, 256)}")
