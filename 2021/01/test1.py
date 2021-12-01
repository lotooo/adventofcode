def load_data_from_file(filename):
    #with open(filename, 'r') as f:
    #    raw_data = f.read()
    #data = re.split(r'\n\n', raw_data)
    with open(filename, 'r') as f:
        data = f.readlines()
    return data

def solve(data):
    increase = 0
    for i in range(1, len(data)):
        if int(data[i]) - int(data[i-1]) > 0:
            increase += 1
    return increase

print("--> test data <--")
test_input = load_data_from_file('test_input')
assert solve(test_input) == 7

print()
print("--> real data <--")
my_input = load_data_from_file('input')
print(solve(my_input))
