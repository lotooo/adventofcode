import re

def load_data_from_file(filename):
    with open(filename, 'r') as f:
        raw_data = f.read()
    data = re.split(r'\n\n', raw_data)
    return prepare_data(data)


def prepare_data(data):
    drawn_numbers = data.pop(0).split(',')
    boards = list(map(lambda x: x.split('\n'), data))
    return (drawn_numbers, boards)

class Board:
    def __init__(self, cells):
        self.lines  = []
        self.column = []
        self.drawn_numbers = []
        for line in [ c for c in cells if c != '']:
            self.lines.append(line.split())
        # generate columns
        self.columns = list(map(list, list(zip(*self.lines))))

    def draw(self, number):
        for line in self.lines:
            if number in line:
                line.remove(number)
        for column in self.columns:
            if number in column:
                column.remove(number)

    def is_winner(self):
        for line in self.lines:
            if len(line) == 0:
                return True
        for column in self.columns:
            if len(column) == 0:
                return True
        return False

    def sum(self):
        total = 0
        for line in self.lines: 
            total += sum(list(map(int, line)))
        return total 

def solve(data):
    drawn_numbers, boards = data
    print(f"Found {len(drawn_numbers)} drawn numbers")
    print(f"Found {len(boards)} boards")
    print(f"\nStarting game\n")
    games = [ Board(b) for b in boards]
    for drawn_number in drawn_numbers:
        print(f"Drawn {drawn_number}")
        for board in games:
            board.draw(drawn_number)
            if board.is_winner():
                print("I win !")
                print(f"Sum of unmarked cells: {board.sum()}")
                return int(drawn_number) * board.sum()
                break
    return False


print("--> test data <--")
test_input = load_data_from_file('test_input')
assert solve(test_input) == 4512

print()
print("--> real data <--")
my_input = load_data_from_file('input')
print(f"\nanswer: {solve(my_input)}")
