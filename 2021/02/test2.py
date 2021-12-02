def load_data_from_file(filename):
    with open(filename, 'r') as f:
        data = list(map(prepate_data, f.readlines()))
    return data


def prepate_data(x):
    instruction, distance = x.split()
    return (instruction, int(distance))


def solve(data):
    aim = 0
    depth = 0
    horiz = 0
    for instruction, distance in data:
        if instruction == 'forward':
            horiz += int(distance)
            depth += (aim * int(distance))
        if instruction == 'down':
            aim += int(distance)
        if instruction == 'up':
            aim -= int(distance)
    return depth * horiz


print("--> test data <--")
test_input = load_data_from_file('test_input')
assert solve(test_input) == 900

print()
print("--> real data <--")
my_input = load_data_from_file('input')
print(solve(my_input))
