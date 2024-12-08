from itertools import product


def rotate_matrix(matrix):
    """Useful to get our matrix per column"""
    new_matrix = []
    for x in range(len(matrix[0])):
        new_line = ""
        for y in range(len(matrix)):
            new_line += matrix[y][x]
        new_matrix.append(new_line)
    return new_matrix


def rotate_matrix_right(matrix):
    new_matrix = []
    for x in range(len(matrix[0], -1, -1)):
        new_line = ""
        for y in range(len(matrix)):
            new_line += matrix[y][x]
        new_matrix.append(new_line)
    return new_matrix


def print_2d_grid(grid, marked_cells=[]):
    for y, line in enumerate(grid):
        for x, c in enumerate(line):
            if (x, y) in marked_cells:
                print(f"\033[2;31;43m{c}\033[0;0m", end="")
            else:
                print(c, end="")
        print("\n", end="")


class Grid2D:
    def __init__(self, grid):
        self.grid = grid
        self.max_y = len(grid)
        self.max_x = len(grid[0])

    def search(self, char):
        search = []
        for y, line in enumerate(self.grid):
            for x, cell in enumerate(line):
                if cell == char:
                    search.append((x, y))
        return search

    def get_nexts(self, x, y, direction):
        if direction == "U":
            return [(x, ny) for ny in range(y - 1, -1, -1)]
        if direction == "D":
            return [(x, ny) for ny in range(y + 1, self.max_y)]
        if direction == "L":
            return [(nx, y) for nx in range(x - 1, -1, -1)]
        if direction == "R":
            return [(nx, y) for nx in range(x + 1, self.max_x)]

    def get_neighboors_in_line(
        self,
        x,
        y,
        distance=1,
        include_self=False,
        include_horizontal=True,
        include_vertical=True,
        include_diagonal=True,
    ):
        out = []
        if include_horizontal:
            out.append(self.get_horizontal_neighboors(x, y, -distance, include_self))
            out.append(self.get_horizontal_neighboors(x, y, distance, include_self))
        if include_vertical:
            out.append(self.get_vertical_neighboors(x, y, -distance, include_self))
            out.append(self.get_vertical_neighboors(x, y, distance, include_self))
        if include_diagonal:
            out.extend(self.get_diagonal_neighboors(x, y, distance, include_self))
        return out

    def get_diagonal_neighboors(self, x, y, distance, include_self=False):
        out = []

        # bottom right
        points = []
        if include_self:
            points.append((x, y))
        points.extend(
            [
                (x + d, y + d)
                for d in range(1, distance + 1)
                if x + d < self.max_x
                and y + d < self.max_y
                and x + d >= 0
                and y + d >= 0
            ]
        )
        out.append(points)

        # top left
        points = []
        if include_self:
            points.append((x, y))
        points.extend(
            [
                (x - d, y - d)
                for d in range(1, distance + 1)
                if x - d < self.max_x
                and y - d < self.max_y
                and x - d >= 0
                and y - d >= 0
            ]
        )
        out.append(points)

        # bottom left
        points = []
        if include_self:
            points.append((x, y))
        points.extend(
            [
                (x - d, y + d)
                for d in range(1, distance + 1)
                if x - d < self.max_x
                and y + d < self.max_y
                and x - d >= 0
                and y + d >= 0
            ]
        )
        out.append(points)

        # top right
        points = []
        if include_self:
            points.append((x, y))
        points.extend(
            [
                (x + d, y - d)
                for d in range(1, distance + 1)
                if x + d < self.max_x
                and y - d < self.max_y
                and x + d >= 0
                and y - d >= 0
            ]
        )
        out.append(points)

        return out

    def get_horizontal_neighboors(self, x, y, dx, include_self=False):
        points = []
        if dx > 0:
            if include_self:
                points.append((x, y))
            points.extend(
                [(nx, y) for nx in range(x + 1, x + dx + 1) if nx < self.max_x]
            )
        else:
            points = [(nx, y) for nx in range(x + dx, x) if nx >= 0]
            if include_self:
                points.append((x, y))
        return points

    def get_vertical_neighboors(self, x, y, dy, include_self=False):
        points = []
        if dy > 0:
            if include_self:
                points.append((x, y))
            points.extend(
                [(x, ny) for ny in range(y + 1, y + dy + 1) if ny < self.max_y]
            )
        else:
            points = [(x, ny) for ny in range(y + dy, y) if ny >= 0]
            if include_self:
                points.append((x, y))
        return points

    def get_neighboors(self, x, y):
        candidates = [
            pos
            for pos in map(
                lambda n: (n[0] + x, n[1] + y), product((-1, 0, 1), repeat=2)
            )
            if pos != (x, y)
        ]
        return [
            (x, y)
            for (x, y) in candidates
            if x >= 0 and y >= 0 and x < self.max_x and y < self.max_y
        ]

    def print(self, marked_cells=[]):
        for y, line in enumerate(self.grid):
            for x, c in enumerate(line):
                if (x, y) in marked_cells:
                    print(f"\033[2;31;43m{c}\033[0;0m", end="")
                else:
                    print(c, end="")
            print("\n", end="")

    def value(self, x, y):
        return self.grid[y][x]

    def __str__(self):
        return "\n".join(self.grid)
