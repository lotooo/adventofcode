import re

def read_data(input_file):
    with open(input_file, 'r') as f:
        raw = f.read()
    my_input = re.split(r"\n\n", raw)
    fields = my_input[0].splitlines()
    my_ticket = my_input[1].splitlines()[1]
    nearby_tickets = my_input[2].splitlines()[1:]
    return (fields, my_ticket, nearby_tickets)


def get_fields_range(fields):
    fields_possible_values = []
    for field in fields:
        for field_part in re.findall(r"\d+-\d+", field):
            range_start = field_part.split('-')[0]
            range_end = field_part.split('-')[1]
            field_part_values = list(range(int(range_start), int(range_end)+1))
            fields_possible_values.extend(field_part_values)
    return fields_possible_values
            

def get_scanning_error_rate(data):
    not_valid_fields = []
    fields, my_ticket, nearby_tickets = data
    possible_values = get_fields_range(fields)
    for ticket in nearby_tickets:
        for v in ticket.split(','):
            if int(v) not in possible_values:
                not_valid_fields.append(int(v))
    return sum(not_valid_fields)

test_input = read_data('test_input')
assert get_scanning_error_rate(test_input) == 71

my_input = read_data('input')
print(get_scanning_error_rate(my_input))

