#!/usr/bin/env python3
def load_data_from_file(filename):
    """ Load the input from a file and return the transformed version """
    with open(filename, 'r') as f:
        data = list(map(prepare_data, f.readlines()))
    return data


def prepare_data(x):
    """ transform the data the way we want it for the puzzle """
    return x

class Monkey:
    def __init__(self, data):
        self.items = list(map(lambda x: int(x.replace(',','')), data[1].split()[2:]))
        self.op = ''.join(data[2].split()[3:])
        self.test = int(data[3].split()[-1])
        self.true = int(data[4].split()[-1])
        self.false = int(data[5].split()[-1])

        self.inspected_items = 0

    def inspect(self):
        self.inspected_items += 1
        item = self.items.pop(0)
        result = eval(self.op.replace('old',str(item)))
        worry_level = result // 3
        if worry_level % self.test == 0:
            return (worry_level, self.true)
        else:
            return (worry_level, self.false)

    def __str__(self):
        return ','.join(map(lambda x: str(x), self.items))


def solve(data):
    """ Solve the puzzle and return the solution """
    monkeys = []
    for i in [ x for x in range(len(data)) if x % 7 == 0]:
        monkey = Monkey(data[i:i+6])
        monkeys.append(monkey)
    for round in range(0,20):
        for i, monkey in enumerate(monkeys):
            while len(monkey.items) > 0:
                worry_level, target_monkey = monkey.inspect()
                monkeys[target_monkey].items.append(worry_level)
    result = sorted([ monkey.inspected_items for monkey in monkeys ])[-2:]
    return result[0] * result[1]


print("--> test data <--")
test_input = load_data_from_file('test_input')
assert solve(test_input) == 10605

print()
print("--> real data <--")
my_input = load_data_from_file('input')
print(f"\nanswer: {solve(my_input)}")














