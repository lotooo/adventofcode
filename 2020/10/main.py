from itertools import product, accumulate, groupby
import operator



with open('input', 'r') as f:
    my_input = [ int(line.strip()) for line in f.readlines() ]

test_input = [
    16,
    10,
    15,
    5,
    1,
    11,
    7,
    19,
    6,
    12,
    4
]

test_input2 = [
    28,
    33,
    18,
    42,
    31,
    14,
    46,
    20,
    48,
    47,
    24,
    23,
    49,
    45,
    19,
    38,
    39,
    11,
    1,
    32,
    25,
    35,
    8,
    17,
    7,
    9,
    4,
    2,
    34,
    10,
    3
]

class Adapter():
    def __init__(self,rating):
        self.rating = rating

    def plug(self, joltage_input):
        self.joltage_input = joltage_input
        self.joltage_output1 = joltage_input+1
        self.joltage_output2 = joltage_input+2
        self.joltage_output3 = joltage_input+3

def plug_my_device(adapters_list):
    device_rating = max(adapters_list) + 3

    charging_outlet_joltage = 0

    adapters = [ Adapter(r) for r in sorted(adapters_list) ]

    joltage_output = 0
    joltage_input = charging_outlet_joltage

    total_plug1 = 0
    total_plug2 = 0
    total_plug3 = 0


    for adapter in adapters:
        adapter.plug(joltage_input)
        if adapter.joltage_output1 in adapters_list:
            total_plug1 += 1
            joltage_output = adapter.joltage_output1
            #print(f"in:{joltage_input} - I can plug it - out:{joltage_output} ({total_plug1}|{total_plug2}|{total_plug3})")
            joltage_input = joltage_output
            continue
        if adapter.joltage_output2 in adapters_list:
            total_plug2 += 1
            joltage_output = adapter.joltage_output2
            #print(f"in:{joltage_input} - I can plug it - out:{joltage_output} ({total_plug1}|{total_plug2}|{total_plug3})")
            joltage_input = joltage_output
            continue
        if adapter.joltage_output3 in adapters_list:
            total_plug3 += 1
            joltage_output = adapter.joltage_output3
            #print(f"in:{joltage_input} - I can plug it - out:{joltage_output} ({total_plug1}|{total_plug2}|{total_plug3})")
            joltage_input = joltage_output
            continue
        if joltage_output > max(adapters_list):
            break
    total_plug3 += 1
    print(f"jolt_diff1: {total_plug1} | jolt_diff2: {total_plug2} | jolt_diff3: {total_plug3} | TOTAL: {total_plug1*total_plug3}")

    
# step 1
plug_my_device(test_input)
plug_my_device(test_input2)
plug_my_device(my_input)


# step 2
def find_prev(adapters, current_jolt):
    current_index = adapters.index(current_jolt)
    prev = []
    if current_index < 3:
        start_index = 0
    else:
        start_index = current_index-3

    if current_jolt-1 in adapters[start_index:current_index+1]:
        prev.append(current_jolt-1)
    if current_jolt-2 in adapters[start_index:current_index+1]:
        prev.append(current_jolt-2)
    if current_jolt-3 in adapters[start_index:current_index+1]:
        prev.append(current_jolt-3)
    return prev

def how_many_ways_can_i_plug_this_crap(adapters_list):
    adapters = sorted(adapters_list)
    adapters.insert(0,0)
    possible_ancestors = {0: 1}
    for j in adapters[1:]:
        total = 0
        ancestors = find_prev(adapters, j)
        #print(f"{j}: {len(ancestors)} ancestors: {ancestors}")
        for a in ancestors:
            #print(f"  {possible_ancestors[a]} ancestors of {a}")
            total += possible_ancestors[a]
        possible_ancestors[j] = total
        #print(f"  Score for {j}: {total}")
    print(total)

how_many_ways_can_i_plug_this_crap(test_input)
how_many_ways_can_i_plug_this_crap(test_input2)
how_many_ways_can_i_plug_this_crap(my_input)
