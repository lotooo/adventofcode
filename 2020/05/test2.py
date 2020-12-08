from collections import defaultdict

with open('input', 'r') as f:
    lines = f.readlines()

taken_seats = set()

for line in lines:
    raw_row = line[0:7]
    binary_row = raw_row.replace('F','0').replace('B', '1')
    row = int(binary_row,2)

    raw_col = line[7:10]
    binary_col = raw_col.replace('L','0').replace('R', '1')
    col = int(binary_col,2)

    taken_seats.add(row*8+col)

min_seat_id = min(taken_seats)
max_seat_id = max(taken_seats)
seats = set(range(min_seat_id,max_seat_id))

available_seats = seats - taken_seats

print("Your seat_id is in this set %s" % available_seats)
