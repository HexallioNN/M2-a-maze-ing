import random


class Cell:
    wall_pairs = {'N': 'S', 'S': 'N', 'E': 'W', 'W': 'E'}

    def __init__(self, x, y):
        self.x, self.y = x, y
        self.walls = {'N': True, 'S': True, 'E': True, 'W': True}
        self.visited = False
        self.logo_cells = set()

    def open_path(self, other, wall):
        self.walls[wall] = False
        other.walls[Cell.wall_pairs[wall]] = False


class Maze:
    def __init__(self, nx: int, ny: int, ix: int = 0, iy: int = 0):
        self.nx, self.ny = nx, ny
        self.ix, self.iy = ix, iy
        self.maze_map = [[Cell(x, y) for y in range(ny)] for x in range(nx)]

    def cell_at(self, x: int, y: int) -> Cell:
        return self.maze_map[x][y]

    def get_unvisited_neighbors(self, cell) -> list:
        neighbors = []
        delta = {'N': (0, -1), 'S': (0, 1), 'E': (1, 0), 'W': (-1, 0)}
        for direction, (dx, dy) in delta.items():
            nx, ny = cell.x + dx, cell.y + dy
            if 0 <= nx < self.nx and 0 <= ny < self.ny:
                neighbor = self.cell_at(nx, ny)
                if not neighbor.visited:
                    neighbors.append((direction, neighbor))
        return neighbors

    def embed_42(self):
        logo_cells = set()
        cx = (self.nx // 2) - 3
        cy = (self.ny // 2) - 2

        for y in range(cy, cy + 3):
            logo_cells.add((cx, y))
        for x in range(cx, cx + 3):
            logo_cells.add((x, cy + 2))
        for y in range(cy + 3, cy + 5):
            logo_cells.add((cx + 2, y))

        ox = cx + 4
        for x in range(ox, ox + 3):
            logo_cells.add((x, cy))
        for y in range(cy, cy + 3):
            logo_cells.add((ox + 2, y))
        for x in range(ox, ox + 3):
            logo_cells.add((x, cy + 2))
        for y in range(cy + 2, cy + 5):
            logo_cells.add((ox, y))
        for x in range(ox, ox + 3):
            logo_cells.add((x, cy + 4))

        for (x, y) in logo_cells:
            if 0 <= x < self.nx and 0 <= y < self.ny:
                self.cell_at(x, y).visited = True

        self.logo_cells = logo_cells

    def seal_logo_borders(self):
        opposite = {'N': 'S', 'S': 'N', 'E': 'W', 'W': 'E'}
        delta = {'N': (0, -1), 'S': (0, 1), 'E': (1, 0), 'W': (-1, 0)}
        for (x, y) in self.logo_cells:
            for direction, (dx, dy) in delta.items():
                nx, ny = x + dx, y + dy
                if 0 <= nx < self.nx and 0 <= ny < self.ny:
                    self.cell_at(nx, ny).walls[opposite[direction]] = True

    def has_large_open_area(self, x: int, y: int) -> bool:
        for dx in range(-1, 2):
            for dy in range(-1, 2):
                bx, by = x + dx, y + dy
                if 0 <= bx < self.nx - 1 and 0 <= by < self.ny - 1:
                    a = self.cell_at(bx, by)
                    b = self.cell_at(bx + 1, by)
                    c = self.cell_at(bx, by + 1)
                    if (not a.walls['E'] and not a.walls['S'] and not
                       b.walls['S'] and not c.walls['E']):
                        return True
        return False

    def make_imperfect(self):
        walls = []
        for x in range(self.nx):
            for y in range(self.ny):
                cell = self.cell_at(x, y)
                if cell.walls['E'] and x + 1 < self.nx:
                    if (x + 1, y) not in self.logo_cells and (x, y) not in \
                          self.logo_cells:
                        walls.append((cell, 'E', self.cell_at(x + 1, y)))
                if cell.walls['S'] and y + 1 < self.ny:
                    if (x, y + 1) not in self.logo_cells and (x, y) not in \
                       self.logo_cells:
                        walls.append((cell, 'S', self.cell_at(x, y + 1)))
        random.shuffle(walls)
        target = len(walls) // 4
        broken = 0
        for cell, direction, neighbor in walls:
            if broken > target:
                break
            cell.open_path(neighbor, direction)
            if self.has_large_open_area(cell.x, cell.y):
                cell.walls[direction] = True
                neighbor.walls[Cell.wall_pairs[direction]] = True
            else:
                broken += 1

    def generate_maze(self, config: dict) -> None:
        self.logo_cells = set()
        if config["seed"] is not None:
            random.seed(config["seed"])
        else:
            random.seed()

        self.nx = config["width"]
        self.ny = config["height"]
        if config["42_pattern"]:
            self.embed_42()
            entry = (config["entry"][0], config["entry"][1])
            exit_ = (config["exit"][0], config["exit"][1])
            if entry in self.logo_cells:
                raise ValueError("ENTRY point conflicts with the 42 pattern")
            if exit_ in self.logo_cells:
                raise ValueError("EXIT point conflicts with the 42 pattern")
        n = self.nx * self.ny
        if config["42_pattern"]:
            n -= 18

        cell_stack = []
        current_cell = self.cell_at(self.ix, self.iy)
        current_cell.visited = True
        nv = 1

        while nv < n:
            neighbours = self.get_unvisited_neighbors(current_cell)
            if not neighbours:
                if not cell_stack:
                    break
                current_cell = cell_stack.pop()
                continue
            direction, next_cell = random.choice(neighbours)
            current_cell.open_path(next_cell, direction)
            cell_stack.append(current_cell)
            current_cell = next_cell
            next_cell.visited = True
            nv += 1
        if config["42_pattern"]:
            self.seal_logo_borders()
        if not config["perfect"]:
            self.make_imperfect()

    def to_hex(self) -> list[str]:
        lines = []
        for y in range(self.ny):
            row = ""
            for x in range(self.nx):
                cell = self.cell_at(x, y)
                val = 0
                if cell.walls['N']:
                    val |= 1
                if cell.walls['E']:
                    val |= 2
                if cell.walls['S']:
                    val |= 4
                if cell.walls['W']:
                    val |= 8
                row += format(val, 'X')
            lines.append(row)
        return lines

    def write_output(self, config: dict, path: str) -> None:
        lines = self.to_hex()
        entry = config["entry"]
        exit_ = config["exit"]

        with open(config["output_file"], "w") as f:
            for line in lines:
                f.write(line + '\n')
            f.write('\n')
            f.write(f"{entry[0]},{entry[1]}\n")
            f.write(f"{exit_[0]},{exit_[1]}\n")
            f.write(f"{path}\n")
