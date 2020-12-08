from itertools import permutations
with open('input', 'r') as f:
    expenses = f.readlines()

perms = permutations(expenses, 2)

for perm in perms:
    a,b = perm
    if int(a) + int(b) == 2020:
        print(perm)
        print(int(a)*int(b))
