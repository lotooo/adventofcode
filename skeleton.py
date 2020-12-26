def load_data_from_file(filename):
    #with open(filename, 'r') as f:
    #    raw_data = f.read()
    #data = re.split(r'\n\n', raw_data)
    with open(filename, 'r') as f:
        data = f.readlines()
    return data

def solve(data):
    return False

print("--> test data <--")
test_input = load_data_from_file('test_input')
assert solve(test_input) == 273

print()
print("--> real data <--")
my_input = load_data_from_file('input')
print(solve(my_input))
