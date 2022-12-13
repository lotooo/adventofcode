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
    #if len(list2) < len(list1):
    #    return False
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
    signals = ['[[2]]', '[[6]]']
    for i in [ x for x in range(0, len(data)) if x % 3 == 0 ]:
        signals.append(data[i])
        signals.append(data[i+1])
    sorted_signals = [ signals.pop() ]
    while len(signals) > 0:
        signal_to_sort = signals.pop()
        sig_sorted = False
        i = 0
        while not sig_sorted:
            if is_right_order(signal_to_sort, sorted_signals[i]):
                sorted_signals.insert(i, signal_to_sort)
                sig_sorted = True
            else:
                # if we are at the end of our list
                # insert it
                if i+1 == len(sorted_signals):
                    sorted_signals.append(signal_to_sort)
                    sig_sorted = True
            i+=1
    return (sorted_signals.index('[[2]]')+1) * (sorted_signals.index('[[6]]')+1)


print("--> test data <--")
test_input = load_data_from_file('test_input')
assert solve(test_input) == 140

print()
print("--> real data <--")
my_input = load_data_from_file('input')
print(f"\nanswer: {solve(my_input)}")
