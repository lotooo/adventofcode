from collections import Counter


def load_data_from_file(filename):
    with open(filename, 'r') as f:
        data = list(map(prepate_data, f.readlines()))
    return data


def prepate_data(x):
    return x.strip()


def solve(data):
    gamma_rate = ''
    epsilon_rate = ''
    columns = map(list, zip(*data))
    for column in columns:
        c = Counter(column)
        gamma_rate += str(c.most_common(1)[0][0])
        epsilon_rate += str(c.most_common()[-1][0])
    print(f"gamma rate: {gamma_rate}")
    print(f"epsilon rate: {epsilon_rate}")
    return int(gamma_rate,2) * int(epsilon_rate,2)


print("--> test data <--")
test_input = load_data_from_file('test_input')
assert solve(test_input) == 198

print()
print("--> real data <--")
my_input = load_data_from_file('input')
print(f"\nanswer: {solve(my_input)}")
