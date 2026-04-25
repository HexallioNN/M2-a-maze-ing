import random


class Cell:
    wall_pairs = {'N': 'S', 'S': 'N', 'E': 'W', 'W': 'E'}

    def __init__(self, x, y):
        self.x, self.y = x, y
        self.walls = {'N': True, 'S': True, 'E': True, 'W': True}
        self.visited = False

    def open_path(self, other, wall):
        self.walls[wall] = False
        other.walls[Cell.wall_pairs[wall]] = False


class Maze:
    def __init__(self, nx, ny, ix=0, iy=0):
        self.nx, self.ny = nx, ny
        self.ix, self.iy = ix, iy
        self.maze_map = [[Cell(x, y) for y in range(ny)] for x in range(nx)]

    def cell_at(self, x, y):
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
        cx = (self.nx // 2) - 4
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

    def generate_maze(self, config: dict) -> None:
        if config["seed"] is not None:
            random.seed(config["seed"])
        else:
            random.seed()

        self.nx = config["width"]
        self.ny = config["height"]
        if config["42_pattern"]:
            self.embed_42() 
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
