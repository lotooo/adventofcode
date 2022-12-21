#!/usr/bin/env python3
import re
import json
def load_data_from_file(filename):
    """ Load the input from a file and return the transformed version """
    with open(filename, 'r') as f:
        data = list(map(prepare_data, f.readlines()))
    return data


def prepare_data(x):
    """ transform the data the way we want it for the puzzle """
    return x.strip().split(': ')


def get_monkey(monkey_name, monkeys):
    iteration = 1
    previous_monkeys =None
    while True:
        replacement = False
        if type(monkeys[monkey_name]) == int:
            return monkeys[monkey_name]
        for m_name, monkey in monkeys.copy().items():
            operation = monkeys[m_name]
            if type(monkeys[m_name]) in [int, float]:
                # nothing to do
                continue
            m = re.findall(r'([a-z]{4})', operation)
            if m:
                for monkey1 in m:
                    if type(monkeys[monkey1]) in [int, float]:
                        replacement = True
                        monkeys[m_name] = operation.replace(monkey1, str(monkeys[monkey1]))
            m2 = re.match(r'(\d+) ([+\-*/]) (\d+)', operation)
            if m2:
                replacement = True
                if m2.group(2) == '+':
                    monkeys[m_name] = int(m2.group(1)) + int(m2.group(3))
                if m2.group(2) == '-':
                    monkeys[m_name] = int(m2.group(1)) - int(m2.group(3))
                if m2.group(2) == '*':
                    monkeys[m_name] = int(m2.group(1)) * int(m2.group(3))
                if m2.group(2) == '/':
                    monkeys[m_name] = int(int(m2.group(1)) / int(m2.group(3)))
            if replacement:
                break
        iteration+=1
        if previous_monkeys and previous_monkeys == monkeys:
            print(json.dumps(monkeys, indent=2))
            sys.exit(1)
        previous_monkeys = monkeys.copy()

def solve(data):
    """ Solve the puzzle and return the solution """
    monkeys = {}
    for monkey in data:
        monkey_name = monkey[0]
        operations = monkey[1]
        try:
            monkeys[monkey_name] = int(operations)
        except:
            monkeys[monkey_name] = operations
    return get_monkey('root', monkeys)


print("--> test data <--")
test_input = load_data_from_file('test_input')
assert solve(test_input) == 152

print()
print("--> real data <--")
my_input = load_data_from_file('input')
print(f"\nanswer: {solve(my_input)}")
