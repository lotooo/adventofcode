from collections import deque
from itertools import permutations,accumulate

with open('input', 'r') as f:
    my_input = [ int(line.strip()) for line in f.readlines() ]

test_input = [
    35,
    20,
    15,
    25,
    47,
    40,
    62,
    55,
    65,
    95,
    102,
    117,
    150,
    182,
    127,
    219,
    299,
    277,
    309,
    576
]

def find_entry_breaking_xmas(numbers, preamble_size):
    # Let's create a queue we can popleft 
    preamble = deque(numbers[0:preamble_size])
    data = deque(numbers[preamble_size:])

    while len(data) > 0:
        possible_sums = [ a+b for a,b in permutations(preamble,2) ]
        if data[0] not in possible_sums:
            return data[0]
        else:
            preamble.popleft()
            preamble.append(data.popleft())

def fin_continous_numbers_equal_to(numbers, sum_to_search):
    data = deque(numbers)
    while len(data) > 0:
        matching_range = list(accumulate(data))
        if sum_to_search in matching_range:     
            max_index = matching_range.index(sum_to_search)
            matching_list = list(data)[0:max_index+1]
            return min(matching_list) + max(matching_list)
        else:
            data.popleft()
     

print("test1_validation: %d" % find_entry_breaking_xmas(test_input,5))
test1_solution = find_entry_breaking_xmas(my_input,25)
print(f"test1_solution: {test1_solution}")

print("test2_validation: %d" % fin_continous_numbers_equal_to(test_input, find_entry_breaking_xmas(test_input,5)))

test2_solution = fin_continous_numbers_equal_to(my_input, test1_solution)
print(f"test2_solution: {test2_solution}")

