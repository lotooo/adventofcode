#!/usr/bin/env python3
import sys

def load_data_from_file(filename):
    """ Load the input from a file and return the transformed version """
    with open(filename, 'r') as f:
        data = list(map(prepare_data, f.readlines()))
    return data


class bcolors:
    RED = '\033[91m'
    ENDC = '\033[0m'

def prepare_data(x):
    """ transform the data the way we want it for the puzzle """
    return x.strip()


def solve(data):
    """ Solve the puzzle and return the solution """
    low_points = []
    for line_id, line in enumerate(data): 
        for col_id, value in enumerate(line):
            print(value, end="")
            if line_id != 0:
                if int(data[line_id-1][col_id]) <= int(value):
                    continue
            if line_id != len(data)-1:
                if int(data[line_id+1][col_id]) <= int(value):
                    continue
            if col_id != 0:
                if int(data[line_id][col_id-1]) <= int(value):
                    continue
            if col_id != len(line)-1:
                if int(data[line_id][col_id+1]) <= int(value):
                    continue
            # Erase last value
            sys.stdout.write("\033[D")
            sys.stdout.write("\033[K")
            # print it with color
            print(f"{bcolors.RED}{value}{bcolors.ENDC}", end="")
            low_points.append(int(value))
        print("\n", end="")
    return sum(list(map(lambda x: x+1,low_points)))


print("--> test data <--")
test_input = load_data_from_file('test_input')
assert solve(test_input) == 15

print()
print("--> real data <--")
my_input = load_data_from_file('input')
print(f"\nanswer: {solve(my_input)}")
