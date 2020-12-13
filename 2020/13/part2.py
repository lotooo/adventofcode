import math

test_input = [
    939,
    "7,13,x,x,59,x,31,19"
]

test_input2 = [
    939,
    "17,x,13,19"
]

test_input3 = [
    939,
    "67,7,59,61"
]
test_input4 = [
    939,
    "67,x,7,59,61"
]
test_input5 = [
    939,
    "67,7,x,59,61"
]
test_input6 = [
    939,
    "1789,37,47,1889"
]

with open('input', 'r') as f:
    my_input = [ line.strip() for line in f.readlines() ]

def lcm(a,b):
    return abs(a*b) // math.gcd(a, b)

def bus_schedule_checker(bus_ids, timestamp):
    resp = []
    for i in range(0,len(bus_ids)):
        if bus_ids[i] == 'x':
            resp.append(True)
            continue
        tested_timestamp = timestamp+i
        if tested_timestamp % int(bus_ids[i]) != 0:
            resp.append(False)
        else:
            resp.append(True)
    return resp


def what_is_my_next_bus(data):
    bus_in_service_ids = [ int(bus_id) for bus_id in data[1].split(',') if bus_id != 'x' ]
    startup_timestamp = min(bus_in_service_ids)
    timestamp = startup_timestamp

    # Lets increment timestamp by 1 at the begining
    increment = 1

    # Extract bus ids
    bus_ids = [ bus_id for bus_id in data[1].split(',') ]

    matching_buses = [ False ]

    while False in matching_buses:
        matching_buses = bus_schedule_checker(bus_ids, timestamp)
        if True in matching_buses:
            # At least one bus is fine
            matching_indexes = [ index for index,found in enumerate(matching_buses) if found == True ]
            for matching_index in matching_indexes:
                if bus_ids[matching_index] != 'x':
                    increment = lcm(increment, int(bus_ids[matching_index]))

        timestamp += increment
        
    print(f"timestamp: {timestamp-increment}")


what_is_my_next_bus(test_input)
what_is_my_next_bus(test_input2)
what_is_my_next_bus(test_input3)
what_is_my_next_bus(test_input4)
what_is_my_next_bus(test_input5)
what_is_my_next_bus(test_input6)
what_is_my_next_bus(my_input)
