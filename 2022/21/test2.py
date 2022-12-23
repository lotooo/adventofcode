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
        if type(monkeys[monkey_name]) in [int, float]:
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
            m2 = re.match(r'(-?\d+\.?\d*) ([+\-*/]) (-?\d+\.?\d*)', operation)
            if m2:
                replacement = True
                if m2.group(2) == '+':
                    monkeys[m_name] = float(m2.group(1)) + float(m2.group(3))
                if m2.group(2) == '-':
                    monkeys[m_name] = float(m2.group(1)) - float(m2.group(3))
                if m2.group(2) == '*':
                    monkeys[m_name] = float(m2.group(1)) * float(m2.group(3))
                if m2.group(2) == '/':
                    monkeys[m_name] = float(m2.group(1)) / float(m2.group(3))
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
    root = monkeys['root']
    mkys = root.split(' + ')
    monkeys.pop('root')
    i = 1
    step=10000000000000
    my_min=1
    my_max=1000000000000000
    tmp_monkeys = monkeys.copy()
    mky2 = get_monkey(mkys[1], tmp_monkeys)
    while True:
        not_enough = False
        print(f"=============================")
        print(f"{my_min=}/{my_max=}/{step=}")
        print(f"=============================")
        for i in range(my_min, my_max, step):
            tmp_monkeys = monkeys.copy()
            print(f"testing: {i:,}")
            tmp_monkeys['humn'] = i
            mky1 = get_monkey(mkys[0], tmp_monkeys)
            print(f"testing: {mky1:,}/{mky2:,}")
            if mky1 == mky2:
                return i
            if mky1 > mky2:
                print("not enough")
                my_min = i
                not_enough = True
            else:
                #                print("too much")
                step = max(1,step//10)
                if not_enough:
                    my_max = i
                    print(f"Going back to {my_min}")
                    break

#print("--> test data <--")
#test_input = load_data_from_file('test_input')
#assert solve(test_input) == 301

print()
print("--> real data <--")
my_input = load_data_from_file('input')
print(f"\nanswer: {solve(my_input)}")
