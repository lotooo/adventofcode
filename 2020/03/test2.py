debug = False

def parse_map(lines, slope_x=3, slope_y=1):
    trees = 0
    pos_y = 0
    pos_x = 0
    for line in lines:
        if pos_y % slope_y != 0:
            # If we don't read EVERY line (IE: slope_y != 1)
            # We have to check if we are on the proper line
            # And skip it if needed
            pos_y += 1
            continue
        pattern_width = len(line.rstrip())

        if pos_x >= pattern_width:
            pos_x -= pattern_width

        if debug:
            print("Line %d: Checking if column %d contains a tree" % (pos_y, pos_x))
            print(line.rstrip())
            print(line.rstrip()[pos_x] == '#')

        if line.rstrip()[pos_x] == '#':
            trees += 1

        pos_y += 1
        pos_x += slope_x
    return trees

with open('input', 'r') as f:
    lines = f.readlines()

slopes_to_test = [ (1,1), (3,1), (5,1), (7,1), (1,2) ]

total_trees = 0

for slope_to_test in slopes_to_test:
    x,y = slope_to_test
    result = parse_map(lines,x,y)
    print("Found %d trees for (Right %d, down %d) slope" % (result,x,y))

    if total_trees == 0:
        total_trees = result
    else:
        total_trees *= result

print("Result: %d" % total_trees)
