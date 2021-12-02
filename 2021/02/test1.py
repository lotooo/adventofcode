def load_data_from_file(filename):
    #with open(filename, 'r') as f:
    #    raw_data = f.read()
    #data = re.split(r'\n\n', raw_data)
    with open(filename, 'r') as f:
        data = list(map(lambda x: x.split(), f.readlines()))
    return data


def solve(data):
    depth = 0
    horiz = 0
    for instruction, distance in data:
        if instruction == 'forward':
            horiz += int(distance)
        if instruction == 'down':
            depth += int(distance)
        if instruction == 'up':
            depth -= int(distance)
    return depth * horiz

print("--> test data <--")
test_input = load_data_from_file('test_input')
assert solve(test_input) == 150

print()
print("--> real data <--")
my_input = load_data_from_file('input')
print(solve(my_input))
