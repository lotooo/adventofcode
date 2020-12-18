import re

with open('input', 'r') as f:
    my_input = [ line.strip() for line in f.readlines() ]

def evaluate(line):
    print(f"start: {line}")
    is_over = re.fullmatch(r"\d+", line)
    if is_over:
        return int(line)

    parenthesis = re.search(r"\(([0-9+* ]*?)\)", line)
    if parenthesis:
        line = line.replace(f"({parenthesis.group(1)})", str(evaluate(parenthesis.group(1))), 1)

    simple_op = re.fullmatch(r"(\d+) ([+*]) (\d+)",line)
    if simple_op:
        n1 = int(simple_op.group(1))
        op = simple_op.group(2)
        n2 = int(simple_op.group(3))
        if op == '+':
            return n1 + n2
        if op == '*':
            return n1 * n2

    doable_sum = re.search(r"(\d+) \+ (\d+)",line)
    if doable_sum:
        n1 = int(doable_sum.group(1))
        n2 = int(doable_sum.group(2))
        line = line.replace(f"{n1} + {n2}", f"{n1+n2}", 1)
        return evaluate(line)

    doable_operation = re.match(r"(\d+) ([*]) (\d+)",line)
    if doable_operation:
        n1 = int(doable_operation.group(1))
        op = doable_operation.group(2)
        n2 = int(doable_operation.group(3))
        if op == '+':
            line = line.replace(f"{n1} + {n2}", f"{n1+n2}",1)
        if op == '*':
            line = line.replace(f"{n1} * {n2}", f"{n1*n2}", 1)
        return evaluate(line)

    return evaluate(line)

assert evaluate("1 + 2 * 3 + 4 * 5 + 6") == 231
assert evaluate("1 + (2 * 3) + (4 * (5 + 6))") == 51
assert evaluate("2 * 3 + (4 * 5)") == 46
assert evaluate("5 + (8 * 3 + 9 + 3 * 4 * 3)") == 1445
assert evaluate("5 * 9 * (7 * 3 * 3 + 9 * 3 + (8 + 6 * 4))") == 669060
assert evaluate("((2 + 4 * 9) * (6 + 9 * 8 + 6) + 6) + 2 + 4 * 2") == 23340

result = 0
for line in my_input:
    line_result = evaluate(line)
    print(f"{line_result} = {line}")
    result += line_result
print(f"result: {result}")
