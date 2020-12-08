from collections import defaultdict
import json
import re

with open('input', 'r') as f:
    rules = f.readlines()
#with open('test2', 'r') as f:
#    rules = f.readlines()

bags = defaultdict(list)

def w(color):
    number_of_bags = 0
    print("'%s' bags contain %s" % (color, bags[color]))
    if len(bags[color]) == 0:
        return 0
    for child_bag in bags[color]:
        child_bag_color, child_bag_count = child_bag
        child_total_count = child_bag_count * w(child_bag_color)
        number_of_bags += child_bag_count + child_total_count
        print("Number of '%s' bags: %d" % (child_bag_color, child_total_count))
    return number_of_bags

for rule in rules:
    if rule.strip() == '':
        continue
    r = re.match(r"([a-zA-Z0-9_ ]*) bags contain ([0-9a-zA-Z ,]*).", rule.strip())
    color = r.group(1)

    for sub_bag in r.group(2).split(','):
        curated_sub_bag = re.sub(r"[ 0-9]*([a-zA-Z ]*)bag[s]*", r"\1", sub_bag)
        curated_sub_bag_count = re.sub(r"([ 0-9]*).*", r"\1", sub_bag)
        if "no other" in curated_sub_bag:
            curated_sub_bag_count = 0
        else:
            curated_sub_bag_count = int(curated_sub_bag_count.strip())
            bags[color].append((curated_sub_bag.strip(), curated_sub_bag_count))
    
total_bags = w('shiny gold')
print("Total bags: %d" % total_bags)

