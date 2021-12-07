#!/usr/bin/env python3
def load_data_from_file(filename):
    """ Load the input from a file and return the transformed version """
    with open(filename, 'r') as f:
        data = list(map(prepare_data, f.readlines()))
    return data[0]


def prepare_data(x):
    """ transform the data the way we want it for the puzzle """
    return list(map(int,x.split(',')))

class Fishes:
    def __init__(self, fishes):
        self.fishes = fishes
        self.day = 0

    def __str__(self):
        return f"After day {self.day}: {self.fishes}"

    @property
    def total(self):
        return len(self.fishes)

    def wait_24_hours(self):
        self.new_fishes = self.fishes.copy()
        for fish_id, fish in enumerate(self.fishes):
            if fish == 0:
                self.new_fishes.append(8)
                self.new_fishes[fish_id] = 6
            else:
                self.new_fishes[fish_id] = fish-1
        self.fishes = self.new_fishes
        self.day += 1


def solve(data):
    """ Solve the puzzle and return the solution """
    fishes = Fishes(data)
    for day in range(0,80):
        fishes.wait_24_hours()
    return fishes.total


print("--> test data <--")
test_input = load_data_from_file('test_input')
print(f"Initial state: {test_input}")
assert solve(test_input) == 5934

print()
print("--> real data <--")
my_input = load_data_from_file('input')
print(f"\nanswer: {solve(my_input)}")
