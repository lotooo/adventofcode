#!/usr/bin/env python3
def load_data_from_file(filename):
    """ Load the input from a file and return the transformed version """
    with open(filename, 'r') as f:
        data = list(map(prepare_data, f.readlines()))
    return data


def prepare_data(x):
    """ transform the data the way we want it for the puzzle """
    return int(x.strip()) if x.strip() else ""


def solve(data):
    """ Solve the puzzle and return the solution """
    deers = []
    deer_calory = 0
    for calory in data:
        if calory == '':
            deers.append(deer_calory)
            deer_calory = 0
        else:
            deer_calory += calory
    # Add the last deer
    deers.append(deer_calory)
    return sum(sorted(deers)[-3:])


print("--> test data <--")
test_input = load_data_from_file('test_input')
assert solve(test_input) == 45000

print()
print("--> real data <--")
my_input = load_data_from_file('input')
print(f"\nanswer: {solve(my_input)}")
