#!/usr/bin/env python3
#import re
import regex
import re
def load_data_from_file(filename):
    """ Load the input from a file and return the transformed version """
    with open(filename, 'r') as f:
        data = list(map(prepare_data, f.readlines()))
    return data

numbers = {
    "one": 1,
    "two": 2,
    "three": 3,
    "four": 4,
    "five": 5,
    "six": 6,
    "seven": 7,
    "eight": 8,
    "nine": 9
}

def prepare_data(line):
    """ transform the data the way we want it for the puzzle """
    # That's a pain, we need to take care of overlapping regex so a simple re.findall
    # doesn't work
    matches = []
    for i,x in enumerate(line):
      m = re.search(r'\d|one|two|three|four|five|six|seven|eight|nine',line[i:])
      if m:
        matches.append(m.group(0))
    return matches

def solve(data):
    """ Solve the puzzle and return the solution """
    result = 0
    for i,line in enumerate(data):
      n1 = numbers.get(line[0])
      if not n1:
        n1 = int(line[0])
      n2 = numbers.get(line[-1])
      if not n2:
        n2 = int(line[-1])
      result += (10*n1 + n2)
    return result


print("--> test data <--")
test_input = load_data_from_file('test_input2')
assert solve(test_input) == 281

print()
print("--> real data <--")
my_input = load_data_from_file('input')
print(f"\nanswer: {solve(my_input)}")
