from mlx import Mlx
from images_prerender import pre_render_tiles as pre_render_images
from images_prerender import pre_render_button, pre_render_ui_env, \
    pre_render_empty, ImgData, pre_loading
from random import shuffle
from config import load_config
from maze import Maze
from timeit import default_timer as timer


class Display():
    loading = False
    maze_displayed = False
    path_displayed = False
    display_path = False
    ui_displayed = False
    clear = False
    cleared = False
    logo_displayed = False
    offset_ver = 10
    offset_hor = offset_ver * 4
    start = 0
    end = 0
    logo_colours = [
        (0xEEBA1BAF).to_bytes(4, "little"),
        (0xEE49BA1B).to_bytes(4, "little"),
        (0xEE8F2B0E).to_bytes(4, "little"),
        (0xEE0E158F).to_bytes(4, "little"),
        ]
    colours = [
            {
                "wall_colour": (0xEE9850AF).to_bytes(4, 'little'),
                "tunnel_colour": (0xEE000000).to_bytes(4, 'little'),
                "logo_colour": logo_colours[0],
                "path_colour": (0xEE67AF50).to_bytes(4, "little")
            },
            {
                "wall_colour": (0xEEF6092A).to_bytes(4, 'little'),
                "tunnel_colour": (0xEE000000).to_bytes(4, 'little'),
                "logo_colour": logo_colours[0],
                "path_colour": (0xEE09F6D5).to_bytes(4, "little")
            },
            {
                "wall_colour": (0xEE22DD4D).to_bytes(4, 'little'),
                "tunnel_colour": (0xEE000000).to_bytes(4, 'little'),
                "logo_colour": logo_colours[0],
                "path_colour": (0xEEDD22B2).to_bytes(4, "little")
            },
            {
                "wall_colour": (0xEE1634E9).to_bytes(4, 'little'),
                "tunnel_colour": (0xEE000000).to_bytes(4, 'little'),
                "logo_colour": logo_colours[0],
                "path_colour": (0xEEE9CB16).to_bytes(4, "little")
            },
            ]
    neighbours = set()
    filled_in_cells = set()
    path_pos = 0

    def __init__(self, m: Mlx, mlx_ptr: int, win_ptr, dimensions: tuple):
        self.m = m
        self.mlx_ptr = mlx_ptr
        self.win_ptr = win_ptr
        self.dimensions = dimensions
        self.width, self.height, self.sidebar = dimensions
        self.parsing()
        self.calc_ratio()
        self.pre_render_images()
        self.pre_render_ui()
        self.display_ui()

    def img_to_window_mine(self, image: ImgData, x: int, y: int) -> int:
        self.m.mlx_put_image_to_window(self.mlx_ptr, self.win_ptr,
                                       image.img, x, y)
        return (0)

    def render_next_frame(self) -> int:
        self.m.mlx_mouse_hook(self.win_ptr, mymouse, self)
        self.m.mlx_key_hook(self.win_ptr, mykey, self)
        if not self.ui_displayed:
            self.display_ui()
            self.ui_displayed = True
        elif not self.maze_displayed:
            self.place_logo()
            self.grow_maze()
        elif self.display_path and not self.path_displayed:
            self.display_path()
        else:
            self.m.SYNC_WIN_COMPLETED
            self.m.SYNC_WIN_FLUSH

    def parsing(self):
        maze: list[list[int]] = []
        with open("config.txt", "r") as config_file:
            configs = dict(line.strip().split("=") for line in config_file)
            file_name = configs["OUTPUT_FILE"]
            cells_logo = set()
            valid_cells = set()
            x, y = (0, 0)
            maze_end = False
            with open(file_name, "r") as maze_text:
                for line in maze_text:
                    Row: list[int] = []
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

    def calc_ratio(self):
        effective_width = self.width - self.sidebar - \
            (self.offset_hor / 2)
        effective_height = self.height - (self.offset_ver * 2)
        ratio_hor = effective_width / self.maze_width
        ratio_ver = effective_height / self.maze_height
        # print("this", effective_height, effective_width)
        if ratio_hor < ratio_ver:
            self.ratio = int(ratio_hor)
        else:
            self.ratio = int(ratio_ver)
        self.maze_width_pixels = self.ratio * self.maze_width
        self.maze_height_pixels = self.ratio * self.maze_height
        self.path_coords = self.calc_pos(self.entry)

    def calc_pos(self, coords: tuple) -> tuple:
        x, y = coords
        x = (int(x) * self.ratio) + int(self.offset_hor / 4)
        y = (int(y) * self.ratio) + int(self.offset_ver)
        return (x, y)

    def pre_render_images(self) -> int:
        self.images = pre_render_images(self.m, self.mlx_ptr, self.ratio,
                                        self.colours[0])
        return (0)

    def pre_render_ui(self):
        self.buttons = pre_render_button(self.m, self.mlx_ptr)
        self.ui = pre_render_ui_env(self.m, self.mlx_ptr, self.dimensions,
                                    (self.maze_width_pixels,
                                     self.maze_height_pixels))
        self.maze_clear = pre_render_empty(self.m, self.mlx_ptr,
                                           ((self.maze_width_pixels),
                                            (self.maze_height_pixels)))
        self.loadning_img = pre_loading(self.m, self.mlx_ptr)

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

    def update_logo_colour(self, colour: int) -> int:
        for colourset in self.colours:
            colourset["logo_colour"] = colour
        return (0)


def mymouse(button, x, y, displaydata):
    # buttons = displaydata.buttons
    m = displaydata.m
    win_ptr = displaydata.win_ptr
    mlx_ptr = displaydata.mlx_ptr
    print(f"Got mouse event! button {button} at {x},{y}.")
    if x > 1800:
        if y < 100:
            displaydata.loading = True
            displaydata.clear = True
            # new_maze_stuff(displaydata)
            displaydata.path_displayed = False
            displaydata.display_path = False
            # call maze gen
        elif y < 200:
            if displaydata.display_path:
                displaydata.display_path = False
                displaydata.maze_displayed = False
                displaydata.path_displayed = False
            else:
                displaydata.display_path = True
        elif y < 300:
            pre_colour = displaydata.colours[0]
            while pre_colour == displaydata.colours[0]:
                shuffle(displaydata.colours)
            m.mlx_sync(mlx_ptr, displaydata.pre_render_images(), win_ptr)
            m.mlx_sync(mlx_ptr, displaydata.maze_update(), win_ptr)
            if displaydata.display_path:
                displaydata.path_displayed = False
                while not displaydata.path_displayed:
                    displaydata.path_display()
        elif y < 400:
            pre_colour = displaydata.logo_colours[0]
            while pre_colour == displaydata.logo_colours[0]:
                shuffle(displaydata.logo_colours)
            displaydata.update_logo_colour(displaydata.logo_colours[0])
            m.mlx_sync(mlx_ptr, displaydata.pre_render_images(), win_ptr)
            m.mlx_sync(mlx_ptr, displaydata.maze_update(), win_ptr)
            if displaydata.display_path:
                displaydata.path_displayed = False
                while not displaydata.path_displayed:
                    displaydata.path_display()
    # scroll up is button 4
    # scroll down is button 5


def mykey(keynum, displaydata):
    m = displaydata.m
    win_ptr = displaydata.win_ptr
    mlx_ptr = displaydata.mlx_ptr
    # ratio = displaydata.ratio
    print(f"Got key {keynum}, and got my stuff back:")
    if keynum == 32:
        m.mlx_mouse_hook(win_ptr, None, None)
    elif keynum == 65307:
        print("closing")
        m.mlx_destroy_window(mlx_ptr, win_ptr)
        m.mlx_loop_exit(mlx_ptr)
    elif keynum == 97:
        displaydata.clear = False
    elif keynum == 114:
        displaydata.clear = False
        displaydata.path_displayed = False
    elif keynum == 112:
        if displaydata.display_path:
            displaydata.display_path = False
            displaydata.maze_displayed = False
            displaydata.path_displayed = False
        else:
            displaydata.display_path = True
    elif keynum == 99:
        pre_colour = displaydata.colours[0]
        while pre_colour == displaydata.colours[0]:
            shuffle(displaydata.colours)
        m.mlx_sync(mlx_ptr, displaydata.pre_render_images(), win_ptr)
        m.mlx_sync(mlx_ptr, displaydata.maze_update(), win_ptr)
        if displaydata.display_path:
            displaydata.path_displayed = False
            while not displaydata.path_displayed:
                displaydata.path_display()
    # elif keynum == 108:
    #     m.mlx_loop_hook(mlx_ptr, render_next_frame, displaydata)
    # elif keynum == 103:
    #     m.mlx_clear_window(mlx_ptr, win_ptr)
    #     m.mlx_sync(mlx_ptr, grow_maze(displaydata),a
    #                win_ptr)
    return displaydata


def render_next_frame(display: Display) -> int:
    if not display.ui_displayed:
        display.display_ui()
        display.ui_displayed = True
    if display.clear and not display.cleared:
        display.clear_maze()
        if display.loading:
            display.img_to_window_mine(display.loadning_img, 400, 420)
        display.cleared = True
    elif display.cleared:
        display.clear = False
        display.cleared = False
    elif display.loading:
        new_maze_stuff(display)
        display.clear = True
    elif not display.maze_displayed:
        if not display.logo_displayed:
            display.start = timer()
            display.place_logo()
            display.logo_displayed = True
        display.end = timer()
        if (display.end - display.start) < 30:
            display.grow_maze()
        else:
            display.maze_update()
    elif display.display_path and not display.path_displayed:
        display.path_display()
    else:
        display.m.mlx_mouse_hook(display.win_ptr, mymouse, display)
        display.m.mlx_key_hook(display.win_ptr, mykey, display)
        display.m.SYNC_WIN_COMPLETED
        display.m.SYNC_WIN_FLUSH


def new_maze_stuff(displaydata: Display):
    try:
        config = load_config("config.txt")
    except FileNotFoundError:
        print("Config file not found")
        quit()
    maze = Maze(config["width"], config["height"])
    maze.generate_maze(config)
    maze.to_hex()
    maze.write_output(config, "not yet done")
    displaydata.parsing()
    displaydata.loading = False


def start_visualisation():
    m = Mlx()
    mlx_ptr = m.mlx_init()
    window_width = 2000
    window_height = 1000
    sidebar_width = 200
    win_ptr = m.mlx_new_window(mlx_ptr, window_width, window_height,
                               "test window")
    (ret, w, h) = m.mlx_get_screen_size(mlx_ptr)
    display = Display(m, mlx_ptr, win_ptr, (window_width, window_height,
                                            sidebar_width))
    print(f"Got screen size: {w} x {h} . and whatever this is {ret}")
    # dimensions = {
    #     "window_width": window_width,
    #     "window_height": window_height,
    #     "sidebar_width": sidebar_width,
    #     "window_width_effective": window_width_effective,
    #     "Mlx": m,
    #     "mlx_ptr": mlx_ptr,
    #     "win_ptr": win_ptr,
    #     "offset_horizontal": 10,
    #     "offset_vertical": 10
    # }
    # mouse_data = {
    #     "sidebar_width": sidebar_width,
    #     "Mlx": m,
    #     "mlx_ptr": mlx_ptr,
    #     "win_ptr": win_ptr
    # }
    # display_data = parser(dimensions)
    m.mlx_loop_hook(display.mlx_ptr, render_next_frame, display)
    m.mlx_loop(mlx_ptr)


if __name__ == "__main__":
    start_visualisation()
