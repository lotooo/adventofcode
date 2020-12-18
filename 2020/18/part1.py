import re

with open('input', 'r') as f:
    my_input = [ line.strip() for line in f.readlines() ]

def evaluate(line):
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

    doable_operation = re.match(r"(\d+) ([+*]) (\d+)",line)
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


assert evaluate("1 + 2 * 3 + 4 * 5 + 6") == 71
assert evaluate("1 + (2 * 3) + (4 * (5 + 6))") == 51
assert evaluate("2 * 3 + (4 * 5)") == 26
assert evaluate("5 + (8 * 3 + 9 + 3 * 4 * 3)") == 437
assert evaluate("5 * 9 * (7 * 3 * 3 + 9 * 3 + (8 + 6 * 4))") == 12240
assert evaluate("((2 + 4 * 9) * (6 + 9 * 8 + 6) + 6) + 2 + 4 * 2") == 13632

result = 0
for line in my_input:
    line_result = evaluate(line)
    print(f"{line_result} = {line}")
    result += line_result
print(f"result: {result}")
