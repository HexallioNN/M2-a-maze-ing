from mlx import Mlx
from images_prerender import pre_render_tiles
from images_prerender import pre_render_button, pre_render_ui_env, \
    pre_render_empty, ImgData, pre_loading
"""
This module Holds the Display Class for use in the Maze_visualisation program
"""


class Display():
    """
    This class governs a Display managed by an instance mini library X

    This class hold various flag to tract the state of the display in
    relation to the rendering of the maze and handles the internal logic
    of the animation with this project.
    """
    loading = True
    start_up = True
    maze_displayed = False
    path_displayed = False
    display_path = False
    ui_displayed = False
    running = False
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
    neighbours: set[tuple[int, int]] = set()
    filled_in_cells: set[tuple[int, int]] = set()
    path_pos = 0

    def __init__(self, m: Mlx, mlx_ptr: int, win_ptr: int,
                 dimensions: tuple[int, int]) -> None:
        """
        This function initializes the Display opening a window

        this function handles a window based on the provided arguments

        Args:
            m: this represent an Mlx object, an instance of the mini lib x
            module
            mlx_ptr: this represents a pointer to this same object, as the
            mlx module has a primitive python wrapper this is stored as an int
            win_ptr: is the pointer to a window created by the Mlx module
            dimensions: is a tuple holding the height and width of the window
            in pixels

        This function then stores this data internally for ready acces for all
          operations on this window
        """
        self.m = m
        self.mlx_ptr = mlx_ptr
        self.win_ptr = win_ptr
        self.width, self.height = dimensions
        self.dimensions = (self.width, self.height, self.sidebar)
        self.loading_img = pre_loading(self.m, self.mlx_ptr)

    def img_to_window_mine(self, image: ImgData, x: int, y: int) -> int:
        """This function places a picture on the window at the given \
            coordinates"""
        self.m.mlx_put_image_to_window(self.mlx_ptr, self.win_ptr,
                                       image.img, x, y)
        return (0)

    def parsing(self) -> None:
        """
        This function reads the maze.txt file to generate the base maze

        This function takes no arguments directly but it does rely on
        the presence of the confix.txt file

        if config.txt is present and complete it will read the maze in the
        designated output file from where it stores this internally in an
        two dimensional array for later referencing.

        afterwards it calls on the functions:
            calc_ratio
            pre_render_images
            pre_render_ui
            display_ui
        """
        maze: list[list[str]] = []
        try:
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
        except FileNotFoundError as e:
            print(f"Error parsing the maze: {e}")
        else:
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
        """This function determines the size of the tiles of the maze"""
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

    def calc_pos(self, coords: tuple[int, int]) -> tuple[int, int]:
        """this function turn an x, y coordinate into its tile equivalent"""
        x, y = coords
        x = (int(x) * self.ratio) + int(self.offset_hor / 4)
        y = (int(y) * self.ratio) + int(self.offset_ver)
        return (x, y)

    def pre_render_images(self) -> int:
        """
        This function call on the pre_render_tiles

        this uses the file images_prerender together with the calculated
        ratios to create the tiles used in the later display
        """
        self.images = pre_render_tiles(self.m, self.mlx_ptr, self.ratio,
                                       self.colours[0])
        return (0)

    def pre_render_ui(self) -> None:
        """"This function governs the rendering of the ui enviroment"""
        self.buttons = pre_render_button(self.m, self.mlx_ptr)
        self.ui = pre_render_ui_env(self.m, self.mlx_ptr, self.dimensions,
                                    (self.maze_width_pixels,
                                     self.maze_height_pixels))
        self.maze_clear = pre_render_empty(self.m, self.mlx_ptr,
                                           ((self.maze_width_pixels),
                                            (self.maze_height_pixels)))
        self.loading_img = pre_loading(self.m, self.mlx_ptr)

    def clear_maze(self) -> int:
        """This function governs the clearing of the maze from the display"""
        self.logo_displayed = False
        self.maze_displayed = False
        self.img_to_window_mine(self.maze_clear, int(self.offset_hor / 4),
                                self.offset_ver)
        return (0)

    def place_logo(self) -> int:
        """This function places the logo cells on the display"""
        for cell in self.logo_cells:
            x, y = cell
            x = (x * self.ratio) + int((self.offset_hor / 4) -
                                       (self.offset_hor / 16))
            y = (y * self.ratio) + int(self.offset_ver - (self.offset_ver / 4))
            self.img_to_window_mine(self.images[15].image, x, y)
        return (0)

    def grow_maze(self) -> int:
        """"
        This function governs the maze growth animation

        When ever this function is called it goes through one cycle
        of maze growth
        to this end it keeps a set of neighbour cells that hold all
        cells the maze connects too through a path and whose neighbour
        is currently displayed.

        the first iteration this set will be empty so it will be
        populated based on the size of the maze, if it will take more than
        500 tiles to fill wholly the starting points are top left and
        bottom right
        more then a 1000 it will start in all four corners
        else it will start only top left

        after displaying all tile it will call place_entry_exit
        """
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
        """
        Places the entry and exit points of the maze

        this function places the entry and exit points
        of the maze on the display after whichi it flags
        the maze as displayed
        """
        x_start, y_start = self.calc_pos(self.entry)
        x_end, y_end = self.calc_pos(self.exit)
        start = self.images[20]
        end = self.images[21]
        self.img_to_window_mine(start.image, x_start, y_start)
        self.img_to_window_mine(end.image, x_end, y_end)
        self.maze_displayed = True
        return (0)

    def maze_update(self) -> int:
        """
        This function governs the wholesale update of the maze visual

        Whereas the maze_grow function exists to slowly grow the maze in an
        animation this function exists to place and update the entire maze
        instantly
        this is used both to finish up should the maze grow take too long
        as it is used to update the colour of the maze
        """
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
        """
        This function governs the animating of the path

        every call this function grows the shortest path through
        the maze by one step, until the path reaches its end upon which
        the function flags it as complete
        """
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
        """This function displays the ui enviroment"""
        x, y = (int(self.width - self.sidebar), 0)
        self.img_to_window_mine(self.ui, 0, 0)
        for button in self.buttons:
            self.img_to_window_mine(button.image, x, y)
            y += 100
        return (0)

    def update_logo_colour(self, colour: bytes) -> int:
        """This function updates the Colour of the logo Tiles"""
        for colourset in self.colours:
            colourset["logo_colour"] = colour
        return (0)
