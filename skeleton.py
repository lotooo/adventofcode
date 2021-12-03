def load_data_from_file(filename):
    with open(filename, 'r') as f:
        data = list(map(prepate_data, f.readlines()))
    return data


def prepate_data(x):
    return x


def solve(data):
    return False


print("--> test data <--")
test_input = load_data_from_file('test_input')
assert solve(test_input) == 273

print()
print("--> real data <--")
my_input = load_data_from_file('input')
print(f"\nanswer: {solve(my_input)}")
