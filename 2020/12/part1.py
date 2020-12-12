import re

with open('input', 'r') as f:
    my_input = [ line.strip() for line in f.readlines() ]

test_input = [
    'F10',
    'N3',
    'F7',
    'R90',
    'F11'
]

class Boat:
    def __init__(self,x=0,y=0,angle=0):
        self.x = 0
        self.y = 0
        self.angle = 0 # EAST

    @property
    def manhattan_distance(self):
        return abs(self.x) + abs(self.y)

    def move_east(self,x):
        self.x += x

    def move_west(self,x):
        self.x -= x

    def move_north(self, y):
        self.y += y

    def move_south(self, y):
        self.y -= y

    def turn_left(self, angle):
        if angle % 90 != 0:
            raise Exception("BadAngle", angle)
        self.angle += angle

    def turn_right(self, angle):
        if angle % 90 != 0:
            raise Exception("BadAngle", angle)
        self.angle -= angle

    def move_forward(self, l):
        direction = {
            0: self.move_east,
            90: self.move_north,
            180: self.move_west,
            270: self.move_south
        }
        direction[self.angle%360](l)

    def action(self, action):
        get_action = re.match(r"([A-Z])(\d+)", action)
        if not get_action:
            raise Exception("WrongAction", action)
        
        instruction = get_action.group(1)
        value = int(get_action.group(2))

        do_something = {
            "E": self.move_east,
            "W": self.move_west,
            "N": self.move_north,
            "S": self.move_south,
            "F": self.move_forward,
            "L": self.turn_left,
            "R": self.turn_right
        }

        do_something[instruction](value)

def let_s_sail(instructions):     
    """ test 1 """
    b = Boat()
    for instr in instructions:
        b.action(instr)
    print(f"manhattan_distance: {b.manhattan_distance}")


let_s_sail(test_input)
let_s_sail(my_input)
