#!/usr/bin/env python3
def load_data_from_file(filename):
    """ Load the input from a file and return the transformed version """
    with open(filename, 'r') as f:
        data = list(map(prepare_data, f.readlines()))
    return data[0]


def prepare_data(x):
    """ transform the data the way we want it for the puzzle """
    return list(map(int,x.split(',')))


def solve(data):
    """ Solve the puzzle and return the solution """
    min_fuel_cost = None
    for pos in range(1, len(data)+1):
        cost = 0
        print(f"Aligning to {pos}")
        for crab in data:
            full_calculation = False
            cost += abs(crab-pos)
            if min_fuel_cost is not None and cost >= min_fuel_cost:
                # We don't have to calculate more than that
                break
            full_calculation = True
        if not full_calculation:
            print(f"I stopped at {cost}")
            break
        print(f"fuel cost: {cost}")
        if min_fuel_cost is None or min_fuel_cost > cost:
            min_fuel_cost = cost
    return min_fuel_cost


print("--> test data <--")
test_input = load_data_from_file('test_input')
assert solve(test_input) == 37

print()
print("--> real data <--")
my_input = load_data_from_file('input')
print(f"\nanswer: {solve(my_input)}")
