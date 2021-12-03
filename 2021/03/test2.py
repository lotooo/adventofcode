from collections import Counter


def load_data_from_file(filename):
    with open(filename, 'r') as f:
        data = list(map(prepate_data, f.readlines()))
    return data


def prepate_data(x):
    return x.strip()


def filter_oxygen(diag_report, column_index):
    columns = list(map(list, zip(*diag_report)))
    column = columns[column_index]
    c = Counter(column)
    if column.count('1') == column.count('0'):
        col_oxygen_gen_rate = '1'
    else:
        col_oxygen_gen_rate = str(c.most_common(1)[0][0])
    return [ line for line in diag_report if line[column_index] == col_oxygen_gen_rate ]


def filter_co2(diag_report, column_index):
    columns = list(map(list, zip(*diag_report)))
    column = columns[column_index]
    c = Counter(column)
    if column.count('1') == column.count('0'):
        col_co2_gen_rate = '0'
    else:
        col_co2_gen_rate = str(c.most_common()[-1][0])
    return [ line for line in diag_report if line[column_index] == col_co2_gen_rate ]


def solve(data):
    oxygen_generator_rating = filter_oxygen(data,0)
    for col_index in range(0, len(data[0])):
        oxygen_generator_rating = filter_oxygen(oxygen_generator_rating,col_index)
    co2_generator_rating = filter_co2(data,0)
    for col_index in range(0, len(data[0])):
        co2_generator_rating = filter_co2(co2_generator_rating,col_index)
    return int(oxygen_generator_rating[0],2) * int(co2_generator_rating[0],2)


print("--> test data <--")
test_input = load_data_from_file('test_input')
assert solve(test_input) == 230

print()
print("--> real data <--")
my_input = load_data_from_file('input')
print(f"\nanswer: {solve(my_input)}")
