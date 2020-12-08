import json
import re

with open('input', 'r') as f:
    myinput = f.read()

groups = myinput.split('\n\n')

total_questions_answered_by_yes = 0

for group in groups:
    responses = set()
    forms = group.split('\n')
    for form in forms:
        responses.update(list(form))
    total_questions_answered_by_yes += len(responses)

print("Total questions answer by yes: %d" % total_questions_answered_by_yes)
        
