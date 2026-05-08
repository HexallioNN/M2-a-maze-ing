from mlx import Mlx
from images_prerender import pre_render_tiles as pre_render_images
from images_prerender import pre_render_button, pre_render_ui_env, \
    pre_render_empty, ImgData, pre_loading


class Display():
    loading = True
    start_up = True
    maze_displayed = False
    path_displayed = False
    display_path = False
    ui_displayed = False
    clear = False
    cleared = False
    logo_displayed = False
    offset_ver = 10
    offset_hor = offset_ver * 4
    start = float(0)
    end = float(0)
    sidebar = 200
    algo_change = False
    logo_colours: list[bytes] = [
        (0xEEBA1BAF).to_bytes(4, "little"),
        (0xEE49BA1B).to_bytes(4, "little"),
        (0xEE8F2B0E).to_bytes(4, "little"),
        (0xEE0E158F).to_bytes(4, "little"),
        ]
    colours = [
            {
                "wall_colour": (0xEE9850AF).to_bytes(4, 'little'),
                "tunnel_colour": (0xEE000000).to_bytes(4, 'little'),
                "logo_colour": (0xEEBA1BAF).to_bytes(4, "little"),
                "path_colour": (0xEE67AF50).to_bytes(4, "little")
            },
            {
                "wall_colour": (0xEEF6092A).to_bytes(4, 'little'),
                "tunnel_colour": (0xEE000000).to_bytes(4, 'little'),
                "logo_colour": (0xEEBA1BAF).to_bytes(4, "little"),
                "path_colour": (0xEE09F6D5).to_bytes(4, "little")
            },
            {
                "wall_colour": (0xEE22DD4D).to_bytes(4, 'little'),
                "tunnel_colour": (0xEE000000).to_bytes(4, 'little'),
                "logo_colour": (0xEEBA1BAF).to_bytes(4, "little"),
                "path_colour": (0xEEDD22B2).to_bytes(4, "little")
            },
            {
                "wall_colour": (0xEE1634E9).to_bytes(4, 'little'),
                "tunnel_colour": (0xEE000000).to_bytes(4, 'little'),
                "logo_colour": (0xEEBA1BAF).to_bytes(4, "little"),
                "path_colour": (0xEEE9CB16).to_bytes(4, "little")
            },
            ]
    neighbours: set[tuple] = set()
    filled_in_cells: set[tuple] = set()
    path_pos = 0

    def __init__(self, m: Mlx, mlx_ptr: int, win_ptr: int,
                 dimensions: tuple) -> None:
        self.m = m
        self.mlx_ptr = mlx_ptr
        self.win_ptr = win_ptr
        self.width, self.height = dimensions
        self.dimensions = (self.width, self.height, self.sidebar)
        self.loading_img = pre_loading(self.m, self.mlx_ptr)

    def img_to_window_mine(self, image: ImgData, x: int, y: int) -> int:
        self.m.mlx_put_image_to_window(self.mlx_ptr, self.win_ptr,
                                       image.img, x, y)
        return (0)

    def parsing(self) -> None:
        maze: list[list[str]] = []
        with open("config.txt", "r") as config_file:
            configs = dict(line.strip().split("=") for line in config_file)
            file_name = configs["OUTPUT_FILE"]
            cells_logo = set()
            valid_cells = set()
            x, y = (0, 0)
            maze_end = False
            with open(file_name, "r") as maze_text:
                for line in maze_text:
                    Row: list[str] = []
                    if line != "\n" or "," in line:
                        for char in line:
                            if char != "\n":
                                cell = char
                                Row.append(cell)
                                if char == "F" and not maze_end:
                                    cells_logo.add((x, y))
                                elif not maze_end:
                                    valid_cells.add((x, y))
                                x += 1
                        y += 1
                        x = 0
                    if line == "\n":
                        maze_end = True
                    elif "," in line:
                        Row = line.strip().split(',')
                    if len(Row) != 0:
                        maze.append(Row)
        self.logo_cells = cells_logo
        self.valid_cells = valid_cells
        entry = maze[-3]
        self.entry = (int(entry[0]), int(entry[1]))
        exit = maze[-2]
        self.exit = (int(exit[0]), int(exit[1]))
        self.path = maze[-1]
        self.maze = maze[:-3]
        self.maze_width = len(maze[0])
        self.maze_height = len(self.maze)
        self.calc_ratio()
        self.pre_render_images()
        self.pre_render_ui()
        self.display_ui()

    def calc_ratio(self) -> None:
        effective_width = self.width - self.sidebar - \
            (self.offset_hor / 2)
        effective_height = self.height - (self.offset_ver * 2)
        ratio_hor = effective_width / self.maze_width
        ratio_ver = effective_height / self.maze_height
        if ratio_hor < ratio_ver:
            self.ratio = int(ratio_hor)
        else:
            self.ratio = int(ratio_ver)
        self.maze_width_pixels = self.ratio * self.maze_width
        self.maze_height_pixels = self.ratio * self.maze_height
        self.path_coords = self.calc_pos(self.entry)
        self.center_x = int((self.maze_width_pixels / 2) + self.offset_hor)
        self.center_y = int((self.maze_height_pixels / 2) + self.offset_ver)

    def calc_pos(self, coords: tuple) -> tuple:
        x, y = coords
        x = (int(x) * self.ratio) + int(self.offset_hor / 4)
        y = (int(y) * self.ratio) + int(self.offset_ver)
        return (x, y)

    def pre_render_images(self) -> int:
        self.images = pre_render_images(self.m, self.mlx_ptr, self.ratio,
                                        self.colours[0])
        return (0)

    def pre_render_ui(self) -> None:
        self.buttons = pre_render_button(self.m, self.mlx_ptr)
        self.ui = pre_render_ui_env(self.m, self.mlx_ptr, self.dimensions,
                                    (self.maze_width_pixels,
                                     self.maze_height_pixels))
        self.maze_clear = pre_render_empty(self.m, self.mlx_ptr,
                                           ((self.maze_width_pixels),
                                            (self.maze_height_pixels)))
        self.loading_img = pre_loading(self.m, self.mlx_ptr)

    def clear_maze(self) -> int:
        self.logo_displayed = False
        self.maze_displayed = False
        self.img_to_window_mine(self.maze_clear, int(self.offset_hor / 4),
                                self.offset_ver)
        return (0)

    def place_logo(self) -> int:
        for cell in self.logo_cells:
            x, y = cell
            x = (x * self.ratio) + int((self.offset_hor / 4) -
                                       (self.offset_hor / 16))
            y = (y * self.ratio) + int(self.offset_ver - (self.offset_ver / 4))
            self.img_to_window_mine(self.images[15].image, x, y)
        return (0)

    def grow_maze(self) -> int:
        new_neighbours = set()
        if self.valid_cells - self.filled_in_cells == set():
            self.filled_in_cells = set()
            self.neighbours = set()
            self.place_entry_exit()
        else:
            if self.neighbours == set():
                if (self.maze_width * self.maze_height) > 500:
                    self.neighbours.add((self.maze_width - 1,
                                         self.maze_height - 1))
                    if (self.maze_width * self.maze_height) > 1000:
                        self.neighbours.add((self.maze_width - 1, 0))
                        self.neighbours.add((0, self.maze_height - 1))
                self.neighbours.add((0, 0))
            for neighbour in self.neighbours:
                x, y = neighbour
                if x >= self.maze_width or y >= self.maze_height:
                    # self.valid_cells = self.valid_cells.remove((x, y))
                    continue
                value = int(self.maze[y][x], 16)
                if (value >> 0 & 1 != 1):
                    new_neighbours.add((x, y - 1))
                if (value >> 1 & 1 != 1):
                    new_neighbours.add((x + 1, y))
                if (value >> 2 & 1 != 1):
                    new_neighbours.add((x, y + 1))
                if (value >> 3 & 1 != 1):
                    new_neighbours.add((x - 1, y))
                self.filled_in_cells.add((x, y))
                x = (x * self.ratio) + int(self.offset_hor / 4)
                y = (y * self.ratio) + self.offset_ver
                for tile in self.images:
                    if value == tile.value:
                        self.img_to_window_mine(tile.image, x, y)
            self.neighbours = new_neighbours
        return (0)

    def place_entry_exit(self) -> int:
        x_start, y_start = self.calc_pos(self.entry)
        x_end, y_end = self.calc_pos(self.exit)
        start = self.images[20]
        end = self.images[21]
        self.img_to_window_mine(start.image, x_start, y_start)
        self.img_to_window_mine(end.image, x_end, y_end)
        self.maze_displayed = True
        return (0)

    def maze_update(self) -> int:
        x = int(self.offset_hor / 4)
        y = self.offset_ver
        self.m.mlx_do_sync(self.mlx_ptr)
        self.m.mlx_sync(self.mlx_ptr, self.place_logo(), self.win_ptr)
        for row in self.maze:
            for cell in row:
                for tile in self.images:
                    if int(cell, 16) == tile.value:
                        if (int(cell, 16) != 0b1111):
                            self.img_to_window_mine(tile.image, x, y)
                        x += self.ratio
                        break
            y += self.ratio
            x = int(self.offset_hor / 4)
        self.m.mlx_sync(self.mlx_ptr, self.place_entry_exit(), self.win_ptr)
        return (0)

    def path_display(self) -> int:
        x, y = self.path_coords
        pos = self.path_pos
        step_size = self.ratio
        path = self.path
        tiles = self.images
        half_step = int(step_size / 2)
        second_half = step_size - half_step
        if pos == len(path):
            self.path_coords = self.calc_pos(self.entry)
            self.path_pos = 0
            self.path_displayed = True
            return (1)
        match path[pos]:
            case "N":
                y -= half_step
                tile = tiles[16]
                self.img_to_window_mine(tile.image, x, y)
                y -= second_half
            case "E":
                x += half_step
                tile = tiles[17]
                self.img_to_window_mine(tile.image, x, y)
                x += second_half
            case "S":
                y += half_step
                tile = tiles[18]
                self.img_to_window_mine(tile.image, x, y)
                y += second_half
            case "W":
                x -= half_step
                tile = tiles[19]
                self.img_to_window_mine(tile.image, x, y)
                x -= second_half
        self.path_coords = (x, y)
        self.path_pos += 1
        return (0)

    def display_ui(self) -> int:
        x, y = (int(self.width - self.sidebar), 0)
        self.img_to_window_mine(self.ui, 0, 0)
        for button in self.buttons:
            self.img_to_window_mine(button.image, x, y)
            y += 100
        return (0)

    def update_logo_colour(self, colour: bytes) -> int:
        for colourset in self.colours:
            colourset["logo_colour"] = colour
        return (0)
