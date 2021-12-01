def load_data_from_file(filename):
    with open(filename, 'r') as f:
        data = list(map(int, f.readlines()))
    return data


def solve(data):
    increase = 0
    # On verifie si x + x2 + x3 < x2 + x3 + x4
    # Donc x < x4
    # SmartGorio !
    for i in range(3, len(data)):
        if data[i] > data[i-3]:
            increase += 1
    return increase


print("--> test data <--")
test_input = load_data_from_file('test_input')
assert solve(test_input) == 5

print()
print("--> real data <--")
my_input = load_data_from_file('input')
print(solve(my_input))
