import json
import re

with open('input', 'r') as f:
    lines = f.readlines()

seat_ids = []

for line in lines:
    raw_row = line[0:7]
    binary_row = raw_row.replace('F','0').replace('B', '1')
    row = int(binary_row,2)

    raw_col = line[7:10]
    binary_col = raw_col.replace('L','0').replace('R', '1')
    col = int(binary_col,2)

    seat_ids.append(row*8+col)

print("Highest seat_id: %d" % max(seat_ids))
