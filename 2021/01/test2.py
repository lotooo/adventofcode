def load_data_from_file(filename):
    #with open(filename, 'r') as f:
    #    raw_data = f.read()
    #data = re.split(r'\n\n', raw_data)
    with open(filename, 'r') as f:
        data = f.readlines()
    return data

def solve(data):
    increase = 0
    last_sum = None
    for i in range(2, len(data)):
      this_sum = int(data[i]) + int(data[i-1]) + int(data[i-2])
      if last_sum and this_sum - last_sum > 0:
        increase += 1
      last_sum = this_sum
    return increase

print("--> test data <--")
test_input = load_data_from_file('test_input')
assert solve(test_input) == 5

print()
print("--> real data <--")
my_input = load_data_from_file('input')
print(solve(my_input))
