with open('input', 'r') as f:
    lines = f.readlines()

trees = 0
pos_y = 0

for line in lines:
    pattern_width = len(line.rstrip())

    pos_x = (3*pos_y)%(pattern_width)

    print("Line %d: Checking if pos %d has a tree" % (pos_y,pos_x))

    if line.rstrip()[pos_x] == '#':
        trees += 1

    pos_y += 1

print("Found %d trees" % trees)
