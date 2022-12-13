#!/usr/bin/env python3
import json
import sys

def load_data_from_file(filename):
    """ Load the input from a file and return the transformed version """
    with open(filename, 'r') as f:
        data = list(map(prepare_data, f.readlines()))
    return data


def prepare_data(x):
    """ transform the data the way we want it for the puzzle """
    return x.strip()

def compare(element1, element2):
    print(f"Comparing {element1} and {element2}")
    if type(element1) == list and type(element2) == list:
        for i, e in enumerate(element1):
            try:
                a = element2[i]
            except IndexError:
                return False
            test = compare(element1[i], element2[i])
            if test is not None:
                return test
        # No more element
        # No choice made
        # Packets are in the right order
        if len(element1) < len(element2):
            return True
        return None
    if type(element1) == list and type(element2) == int:
        test = compare(element1,[element2])
        if test is not None:
            return test
    if type(element1) == int and type(element2) == list:
        test = compare([element1],element2)
        if test is not None:
            return test
    if type(element1) == int and type(element2) == int:
        if element1 < element2:
            return True
        elif element2 < element1:
            return False
    return None

def is_right_order(p1,p2):
    list1=json.loads(p1)
    list2=json.loads(p2)
    test = None
    for i, element in enumerate(list1):
        try:
            a = list2[i]
        except IndexError:
            return False
        test = compare(list1[i],list2[i])
        if test is not None:
            return test
    # No more element
    # No choice made
    # Packets are in the right order
    if len(list1) < len(list2):
        return True
    return None

def solve(data):
    """ Solve the puzzle and return the solution """
    right_order_pairs = []
    for i in [ x for x in range(len(data)) if x % 3 == 0 ]:
        pair_number = (i//3)+1
        print(f"== Pair {pair_number }==")
        p1=data[i]
        p2=data[i+1]
        right_order = is_right_order(p1,p2)
        print(f"{right_order}")
        if right_order is None:
            print("ERROR")
            sys.exit(1)
        if right_order:
            right_order_pairs.append(pair_number)
    print(right_order_pairs)
    return sum(right_order_pairs)


print("--> test data <--")
test_input = load_data_from_file('test_input')
assert solve(test_input) == 13

print()
print("--> real data <--")
my_input = load_data_from_file('input')
print(f"\nanswer: {solve(my_input)}")
