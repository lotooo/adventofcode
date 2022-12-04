#!/usr/bin/env python3
def load_data_from_file(filename):
    """ Load the input from a file and return the transformed version """
    with open(filename, 'r') as f:
        data = list(map(prepare_data, f.readlines()))
    return data


def prepare_data(x):
    """ transform the data the way we want it for the puzzle """
    return x.strip().split(',')

def get_seats(section):
    return set(range(int(section.split('-')[0]), int(section.split('-')[1])+1))

def solve(data):
    """ Solve the puzzle and return the solution """
    total = 0
    for s1,s2 in data:
        seats_section_1 = get_seats(s1)
        seats_section_2 = get_seats(s2)
        if seats_section_1 & seats_section_2:
            total += 1
    return total


print("--> test data <--")
test_input = load_data_from_file('test_input')
assert solve(test_input) == 4

print()
print("--> real data <--")
my_input = load_data_from_file('input')
print(f"\nanswer: {solve(my_input)}")
