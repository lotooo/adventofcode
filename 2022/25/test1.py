#!/usr/bin/env python3
from itertools import combinations,permutations,product
def load_data_from_file(filename):
    """ Load the input from a file and return the transformed version """
    with open(filename, 'r') as f:
        data = list(map(prepare_data, f.readlines()))
    return data


def prepare_data(x):
    """ transform the data the way we want it for the puzzle """
    return x.strip()

values = {
    '=': -2,
    '-': -1,
    '0': 0,
    '1': 1,
    '2': 2,
}

def convert_to_decimal(x):
    total = 0
    for i,symbol in enumerate(reversed(x)):
        #print(f"{i=}: {symbol=}: 5^{i}*{values[symbol]}")
        total +=2*values[symbol] * pow(5,i)
    return total


def convert_to_snafu(num):
    snafu = []
    i = 0
    while pow(5,i) < num:
        i+=1
    snafu =  i * ['=']
    snafu[0] = '2'
    for ind in range(1,len(snafu)):
        tmp = snafu.copy()
        for key in (reversed(list(values.keys()))):
            tmp[ind] = key
            #print(f"{tmp}: {convert_to_decimal(tmp)} > {num} = {convert_to_decimal(tmp) > num} ")
            if convert_to_decimal(tmp) == num:
                return ''.join(tmp)
            if convert_to_decimal(tmp) > num:
                continue
            else:
                snafu[ind] = key
                break
    return snafu

def solve(data):
    """ Solve the puzzle and return the solution """
    total = 0
    for number in data:
        total += convert_to_decimal(number)
    print(total)
    return convert_to_snafu(total)


print("--> test data <--")
test_input = load_data_from_file('test_input')
assert solve(test_input) == '2=-1=0'

print()
print("--> real data <--")
my_input = load_data_from_file('input')
print(f"\nanswer: {solve(my_input)}")
