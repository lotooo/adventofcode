from itertools import permutations
with open('input', 'r') as f:
    expenses = f.readlines()

perms = permutations(expenses, 3)

for perm in perms:
    a,b,c = perm
    if int(a) + int(b) + int(c) == 2020:
        print(perm)
        print(int(a)*int(b)*int(c))
