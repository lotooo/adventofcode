import re
from itertools import product
from  collections import Counter

with open('input', 'r') as f:
    my_input = [ line.strip() for line in f.readlines() ]

with open('test_input_part2', 'r') as f:
    test_input = [ line.strip() for line in f.readlines() ]

#test_input = [
#    '0: 1 2',
#    '1: "a"',
#    '2: 1 3 | 3 1',
#    '3: "b"'
#]

test_input2 = [
    '0: 4 1 5',
    '1: 2 3 | 3 2',
    '2: 4 4 | 5 5',
    '3: 4 5 | 5 4',
    '4: "a"',
    '5: "b"'
    '',
    'ababbb',
    'bababa',
    'abbbab',
    'aaabbb',
    'aaaabbb'
]

def extract_rules_dict(rules):
    rules_dict = {}
    for rule in rules:
        m = re.match(r"(\d+): (.*)", rule)
        if m:
            index = m.group(1)
            data = m.group(2)
            if "a" in data:
                rules_dict[index] = 'a'
                continue
            if "b" in data:
                rules_dict[index] = 'b'
                continue

            subrules = data.split('|')
            if len(subrules) > 1:
                rules_dict[index] = [ subrules[0].strip(), subrules[1].strip() ]
                continue

            # It's not a special case
            # Let's write the rule
            rules_dict[index] = data
    return rules_dict

def get_values(rules, i, longest_message=None):
    if rules[i] == "8 11":
        rule42 = get_values(rules, "42")
        rule31 = get_values(rules, "31")
        return (rule42,rule31)

    if isinstance(rules[i], list):
        values1 = rules[i][0]
        subrules1 = values1.split()
        values2 = rules[i][1]
        subrules2 = values2.split()

        # Some lines are using this format '94: 105 | 23'
        # We don't have to create a product for them
        if len(subrules1) > 1:
            res1=[get_values(rules, subrules1[0]),get_values(rules, subrules1[1])]
        else:
            res1=[get_values(rules, values1)]
        if len(subrules2) > 1:
            res2=[get_values(rules, subrules2[0]),get_values(rules, subrules2[1])]
        else:
            res2=[get_values(rules, values2)]

        joined_list1 = list(
            map(
                lambda x: ''.join(x),
                product(*res1)
            )
        )
        joined_list2 = list(
            map(
                lambda x: ''.join(x),
                product(*res2)
            )
        )
        return joined_list1 + joined_list2
    else:
        if rules[i] == 'a' or rules[i] == 'b':
            return rules[i]
        else:
            subrules = rules[i].split()
            result = list(
                map(
                    lambda x: get_values(rules,x),
                    subrules
                )
            )
            updog = list(
                map(
                    lambda x: ''.join(x),
                    product(*result)
                )
            )
            return updog

def solve(data):
    raw_rules = list(
        filter(lambda x: re.match(r"\d+", x), data)
    )
    messages = list(
        filter(lambda x: re.match(r"[ab]+", x), data)
    )
    rules = extract_rules_dict(raw_rules)
    longest_message = max(list(
        map(len, messages)
    ))
    rule42, rule31 = get_values(rules,"0",longest_message)
    rule42_elements_sizes = max(map(len,rule42))
    wrong_messages = []
    for message in messages:
        print(f"testing message: {message}")
        c = Counter()
        if len(message) % rule42_elements_sizes != 0:
            wrong_messages.append(message)
            continue
        i = 0
        has_31_started = False
        wrong = False
        while i < len(message):
            # rule42 and rule31 size is rule42_elements_sizes,
            # Let's analyse the messages
            # rule42_elements_sizes by rule42_elements_sizes characters and test if it's part of rule42 or rule31 patterns
            substring = message[i:i+rule42_elements_sizes]
            if substring in rule42:
                c.update(["42"])
                if has_31_started:
                    wrong_messages.append(message)
                    wrong = True
                    break
            elif substring in rule31:
                c.update(["31"])
                has_31_started = True
            else:
                wrong_messages.append(message)
                wrong = True
                break
            i += rule42_elements_sizes
        if wrong:
            continue
        # Let's check if we had at least 1 31
        if c["31"] == 0:
            wrong_messages.append(message)
            continue
        # We need at least 2 42 (one for rule 8 and one for 11)
        if c["42"] < 2:
            wrong_messages.append(message)
            continue
        # We can't have the same number of 42 ane 31 (because at least 1 42 on rule 8 and then 1 42 + 1 31 for rule 11)
        # + we can't have more 31 than 42
        if c["31"] >= c["42"]:
            wrong_messages.append(message)
            continue
            
    print(len(messages))
    print(len(wrong_messages))
    print(f"-> {len(messages)-len(wrong_messages)}")

solve(test_input)
#solve(test_input2)
solve(my_input)
