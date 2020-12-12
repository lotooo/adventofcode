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

class Waypoint:
    def __init__(self, initial_waypoint):
        if initial_waypoint.get('E'):
            self.x = initial_waypoint.get('E')
        if initial_waypoint.get('W'):
            self.x = - initial_waypoint.get('W')
        if initial_waypoint.get('N'):
            self.y = initial_waypoint.get('N')
        if initial_waypoint.get('S'):
            self.y = - initial_waypoint.get('S')

    def move_east(self,x):
        self.x += x

    def move_west(self,x):
        self.x -= x

    def move_north(self, y):
        self.y += y

    def move_south(self, y):
        self.y -= y

    def rotate90degres_left(self):
        previous_x = self.x
        previous_y = self.y
        self.x = - previous_y
        self.y = previous_x

    def rotate_left(self, angle):
        for i in range(0, angle//90):
            self.rotate90degres_left()

    def rotate_right(self, angle):
        for i in range(0, angle//90):
            self.rotate90degres_right()

    def rotate90degres_right(self):
        previous_x = self.x
        previous_y = self.y
        self.x = previous_y
        self.y = - previous_x
        

class Boat:
    def __init__(self,initial_waypoint):
        self.x = 0
        self.y = 0
        self.waypoint = Waypoint(initial_waypoint)
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
        for x in range(0,l):
            if self.waypoint.x > 0:
                self.move_east(abs(self.waypoint.x))
            else:
                self.move_west(abs(self.waypoint.x))
        for y in range(0,l):
            if self.waypoint.y > 0:
                self.move_north(abs(self.waypoint.y))
            else:
                self.move_south(abs(self.waypoint.y))


    def action(self, action):
        """ Move the waypoint or do something """
        get_action = re.match(r"([A-Z])(\d+)", action)
        if not get_action:
            raise Exception("WrongAction", action)
        
        instruction = get_action.group(1)
        value = int(get_action.group(2))

        do_something = {
            "E": self.waypoint.move_east,
            "W": self.waypoint.move_west,
            "N": self.waypoint.move_north,
            "S": self.waypoint.move_south,
            "F": self.move_forward,
            "L": self.waypoint.rotate_left,
            "R": self.waypoint.rotate_right
        }

        do_something[instruction](value)

def let_s_sail(instructions):     
    """ test 1 """
    initial_waypoint = {"E": 10, "N": 1}
    b = Boat(initial_waypoint)
    for instr in instructions:
        b.action(instr)
    print(f"manhattan_distance: {b.manhattan_distance}")

let_s_sail(test_input)
let_s_sail(my_input)
