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

class TicketRules:
    def __init__(self, fields, my_ticket):
        self.fields = {}
        self.my_ticket = my_ticket.split(',')
        self.fields_possible_values = get_fields_range(fields)
        for field in fields:
            m = re.match("([a-zA-Z ]+): (\d+)-(\d+) or (\d+)-(\d+)", field)
            if m:
                rule_name = m.group(1)
                rule_range1_min = int(m.group(2))
                rule_range1_max = int(m.group(3))
                rule_range2_min = int(m.group(4))
                rule_range2_max = int(m.group(5))
            self.fields[rule_name] = { "rule": (rule_range1_min,rule_range1_max,rule_range2_min,rule_range2_max)}

    def filter_valid_tickets(self, tickets):
        valid_tickets = []
        for ticket in tickets:
            valid = True
            for v in ticket.split(','):
                if int(v) not in self.fields_possible_values:
                    valid = False
                    break
            if valid:
                valid_tickets.append(ticket)
            
        return valid_tickets

    @property
    def unknown_fields_indexes(self):
        return list(set(range(0,len(self.my_ticket))) - set(self.known_fields_indexes)) 

    @property
    def known_fields_indexes(self):
        return [ rule["index"] for rule_name,rule in self.fields.items() if "index" in rule ]
        
def test_rules(num, rules):
    possible_fields = []
    for rule_name,r in rules.items():
        min1,max1,min2,max2 = r['rule']
        if (num >= min1 and num <= max1) or (num >= min2 and num <= max2):
            possible_fields.append(rule_name)
    return possible_fields
                
def part2(data):
    fields, my_ticket, nearby_tickets = data
    tr = TicketRules(fields, my_ticket)
    valid_tickets = tr.filter_valid_tickets(nearby_tickets)
    valid_tickets.append(my_ticket)

    while len(tr.unknown_fields_indexes) > 0:
        for i in tr.unknown_fields_indexes:
            possible_rules = set([ rule for rule in tr.fields.keys() if not "index" in tr.fields[rule] ])
            for t in valid_tickets:
                ticket=t.split(",")
                working_rules = test_rules(int(ticket[i]), tr.fields)
                possible_rules &= set(working_rules)
                if len(possible_rules) == 1:
                    print(f"Index {i} is {possible_rules}")
                    tr.fields[possible_rules.pop()]["index"] = i
                    break

    # print only the result
    result = 1
    for rule in [ rule_name for rule_name,rule in tr.fields.items() if "departure" in rule_name ]:
        result *= int(tr.my_ticket[tr.fields[rule].get('index')])
    print(f"result: {result}")
        
my_input = read_data('input')
part2(my_input)

