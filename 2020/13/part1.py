test_input = [
    939,
    "7,13,x,x,59,x,31,19"
]

with open('input', 'r') as f:
    my_input = [ line.strip() for line in f.readlines() ]

def bus_schedule_checker(bus_id, timestamp):
    return timestamp % bus_id == 0

def what_is_my_next_bus(data):
    timestamp = int(data[0])
    startup_timestamp = timestamp
    bus_in_service_ids = [ int(bus_id) for bus_id in data[1].split(',') if bus_id != 'x' ]

    print(bus_in_service_ids)
    
    while True:
        which_bus_is_passing = list(map(lambda x: bus_schedule_checker(x, timestamp), bus_in_service_ids))
        try:
            my_bus = which_bus_is_passing.index(True)
            break
        except ValueError:
            timestamp += 1
            continue

    my_bus_id = bus_in_service_ids[my_bus]
    waiting_time = timestamp - startup_timestamp

    print(f"bus_id: {my_bus_id} ts:{timestamp} waiting:{waiting_time} response:{waiting_time*my_bus_id}")

what_is_my_next_bus(test_input)
what_is_my_next_bus(my_input)
