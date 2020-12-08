from collections import defaultdict
import json
import re

with open('input', 'r') as f:
    rules = f.readlines()

containers = defaultdict(list)

possible_bags = set()

def w(color):
    global possible_bags
    print("%s can be contained in %s bags" % (color, containers[color]))
    for possible_color in containers[color]:
        possible_bags.add(possible_color)
        w(possible_color)

for rule in rules:
    if rule.strip() == '':
        continue
    r = re.match(r"([a-zA-Z0-9_ ]*) bags contain ([0-9a-zA-Z ,]*).", rule.strip())
    container = r.group(1)

    for sub_bag in r.group(2).split(','):
        curated_sub_bag = re.sub(r"[ 0-9]*([a-zA-Z ]*)bag[s]*", r"\1", sub_bag)
        containers[curated_sub_bag.strip()].append(container)
    
    #print(json.dumps(containers, indent=2))

#for possible in containers['shiny gold']:
#    print(containers[possible])

        
w('shiny gold')

print(len(possible_bags))
