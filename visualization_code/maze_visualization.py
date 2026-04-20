from mlx import Mlx
from images_prerender import pre_render_tiles as pre_render_images
from random import shuffle


def mymouse(button, x, y, mystuff):
    print(f"Got mouse event! button {button} at {x},{y}.")
    # scroll up is button 4
    # scroll down is button 5


colours = [
            {
                "wall_colour": (0xEEFFFFFF).to_bytes(4, 'little'),
                "tunnel_colour": (0xEE000000).to_bytes(4, 'little'),
                "logo_colour": (0xEEFF00FF).to_bytes(4, "little"),
                "path_colour": (0xEEFFFF00).to_bytes(4, "little")
            },
            {
                "wall_colour": (0xEEFF0000).to_bytes(4, 'little'),
                "tunnel_colour": (0xEE000000).to_bytes(4, 'little'),
                "logo_colour": (0xEEFF00FF).to_bytes(4, "little"),
                "path_colour": (0xEEFFFF00).to_bytes(4, "little")
            },
            {
                "wall_colour": (0xEE00FF00).to_bytes(4, 'little'),
                "tunnel_colour": (0xEE000000).to_bytes(4, 'little'),
                "logo_colour": (0xEEFF00FF).to_bytes(4, "little"),
                "path_colour": (0xEEFFFF00).to_bytes(4, "little")
            },
            {
                "wall_colour": (0xEE0000FF).to_bytes(4, 'little'),
                "tunnel_colour": (0xEE000000).to_bytes(4, 'little'),
                "logo_colour": (0xEEFF00FF).to_bytes(4, "little"),
                "path_colour": (0xEEFFFF00).to_bytes(4, "little")
            },
            {
                "wall_colour": (0xEEFF0000).to_bytes(4, 'little'),
                "tunnel_colour": (0xEE000000).to_bytes(4, 'little'),
                "logo_colour": (0xEEFF00FF).to_bytes(4, "little"),
                "path_colour": (0xEEFFFF00).to_bytes(4, "little")
            }
            ]


def mykey(keynum, displaydata):
    m = displaydata["Mlx"]
    win_ptr = displaydata["win_ptr"]
    mlx_ptr = displaydata["mlx_ptr"]
    ratio = displaydata["ratio"]
    print(f"Got key {keynum}, and got my stuff back:")
    if keynum == 32:
        m.mlx_mouse_hook(win_ptr, None, None)
    elif keynum == 65307:
        print("closing")
        m.mlx_destroy_window(mlx_ptr, win_ptr)
        m.mlx_loop_exit(mlx_ptr)
    elif keynum == 97:
        m.mlx_sync(mlx_ptr, m.mlx_clear_window(mlx_ptr, win_ptr), win_ptr)
        m.mlx_sync(mlx_ptr, m.mlx_clear_window(mlx_ptr, win_ptr), win_ptr)
        displaydata["maze_displayed"] = False
    elif keynum == 114:
        m.mlx_clear_window(mlx_ptr, win_ptr)
        m.mlx_sync(mlx_ptr, maze_display(displaydata), win_ptr)
    elif keynum == 112:
        if displaydata["display_path"]:
            displaydata["display_path"] = False
            displaydata["maze_displayed"] = False
            displaydata["path_displayed"] = False
        else:
            displaydata["display_path"] = True
    elif keynum == 99:
        shuffle(colours)
        colour = colours[0]
        m.mlx_sync(mlx_ptr, m.mlx_clear_window(mlx_ptr, win_ptr), win_ptr)
        pre_render_images(m, mlx_ptr, ratio, colour)
        m.mlx_sync(mlx_ptr, maze_display(displaydata), win_ptr)
    # elif keynum == 108:
    #     m.mlx_loop_hook(mlx_ptr, render_next_frame, displaydata)
    # elif keynum == 103:
    #     m.mlx_clear_window(mlx_ptr, win_ptr)
    #     m.mlx_sync(mlx_ptr, grow_maze(displaydata),
    #                win_ptr)


# def grow_maze(displaydata: dict) -> int:
#     m = displaydata["Mlx"]
#     win_ptr = displaydata["win_ptr"]
#     mlx_ptr = displaydata["mlx_ptr"]
#     tiles = displaydata["tiles"]
#     maze = displaydata["maze"]
#     ratio = displaydata["ratio"]
#     width = len(maze[0])
#     height = len(maze)
#     total = width * height
#     x, y = (0, 0)
#     m.mlx_do_sync(mlx_ptr)
#     # place logo first:
#     for row in maze:
#         for cell in row:
#             if int(cell, 16) == tiles[15].value:
#                 total -= 1
#                 m.mlx_put_image_to_window(
#                     mlx_ptr, win_ptr, tiles[15].image.img, x, y)
#             x += ratio
#         y += ratio
#         x = 0
#     x, y = (0, 0)
#     return (0)


def place_entry_exit(displaydata: dict) -> int:
    m = displaydata["Mlx"]
    win_ptr = displaydata["win_ptr"]
    mlx_ptr = displaydata["mlx_ptr"]
    tiles = displaydata["images"]
    x_start, y_start = displaydata["entry"]
    x_end, y_end = displaydata["exit"]
    start = tiles[20]
    end = tiles[21]
    m.mlx_put_image_to_window(mlx_ptr, win_ptr, start.image.img,
                              x_start, y_start)
    m.mlx_put_image_to_window(mlx_ptr, win_ptr, end.image.img,
                              x_end, y_end)
    return (0)


def maze_display(displaydata: dict) -> int:
    m = displaydata["Mlx"]
    win_ptr = displaydata["win_ptr"]
    mlx_ptr = displaydata["mlx_ptr"]
    tiles = displaydata["images"]
    maze = displaydata["maze"]
    ratio = displaydata["ratio"]
    x, y = (0, 0)
    m.mlx_do_sync(mlx_ptr)
    for row in maze:
        for cell in row:
            for tile in tiles:
                if int(cell, 16) == tile.value:
                    m.mlx_put_image_to_window(mlx_ptr, win_ptr, tile.image.img,
                                              x, y)
                    x += ratio
                    break
        y += ratio
        x = 0
    m.mlx_sync(mlx_ptr, place_entry_exit(displaydata), win_ptr)
    return (0)


def path_display(displaydata: dict) -> int:
    m = displaydata["Mlx"]
    win_ptr = displaydata["win_ptr"]
    mlx_ptr = displaydata["mlx_ptr"]
    x, y = displaydata["path_coords"]
    pos = displaydata["path_pos"]
    step_size = displaydata["ratio"]
    path = displaydata["path"]
    tiles = displaydata["images"]
    tile = tiles[16]
    half_step = int(step_size / 2)
    if pos == len(path):
        displaydata["path_coords"] = displaydata["entry"]
        displaydata["path_pos"] = 0
        displaydata["path_displayed"] = True
        return (1)
    match path[pos]:
        case "N":
            y -= half_step
            tile = tiles[16]
            m.mlx_put_image_to_window(mlx_ptr, win_ptr, tile.image.img,
                                      x, y)
            y -= half_step
        case "E":
            x += half_step
            tile = tiles[17]
            m.mlx_put_image_to_window(mlx_ptr, win_ptr, tile.image.img,
                                      x, y)
            x += half_step
        case "S":
            y += half_step
            tile = tiles[18]
            m.mlx_put_image_to_window(mlx_ptr, win_ptr, tile.image.img,
                                      x, y)
            y += half_step
        case "W":
            x -= half_step
            tile = tiles[19]
            m.mlx_put_image_to_window(mlx_ptr, win_ptr, tile.image.img,
                                      x, y)
            x -= half_step
    displaydata["path_coords"] = (x, y)
    displaydata["path_pos"] += 1
    return (0)


def parser(dimensions: dict) -> dict:
    m = dimensions["Mlx"]
    mlx_ptr = dimensions["mlx_ptr"]
    win_ptr = dimensions["win_ptr"]
    Grid: list[list[int]] = []
    with open("config.txt", "r") as config_file:
        configs = dict(line.strip().split("=") for line in config_file)
    file_name = configs["OUTPUT_FILE"]
    with open(file_name, "r") as maze:
        for line in maze:
            Row: list[int] = []
            if line != "\n" and "," not in line:
                for char in line:
                    if char != "\n":
                        cell = char
                        Row.append(cell)
            elif "," in line:
                Row = line.strip().split(',')
            if len(Row) != 0:
                Grid.append(Row)
    entry = Grid[-3]
    exit = Grid[-2]
    path = Grid[-1]
    Grid = Grid[:-3]
    window_width_effective = dimensions["window_width_effective"]
    window_height = dimensions["window_height"]
    ratio_horizontal = (window_width_effective / len(Grid[0]))
    ratio_vertical = (window_height / len(Grid))
    if ratio_horizontal < ratio_vertical:
        ratio = int(ratio_horizontal)
    else:
        ratio = int(ratio_vertical)
    images = pre_render_images(m, mlx_ptr, ratio)
    sidebar = None  # to be created
    display_data = {
        "maze_displayed": False,
        "path_displayed": False,
        "display_path": False,
        "images": images,
        "maze": Grid,
        "entry": (int((int(entry[0]) * ratio)),
                  int((int(entry[1]) * ratio))),
        "exit": (int((int(exit[0]) * ratio)),
                 int((int(exit[1]) * ratio))),
        "path": path,
        "ratio": ratio,
        "sidebar": sidebar,
        "Mlx": m,
        "mlx_ptr": mlx_ptr,
        "win_ptr": win_ptr,
        "path_coords": (int((int(entry[0]) * ratio)),
                        int((int(entry[1]) * ratio))),
        "path_pos": 0
    }
    return (display_data)


class ImgData():
    """Structure for image data"""
    def __init__(self):
        self.img = None
        self.width = 0
        self.height = 0
        self.data = None
        self.sl = 0  # size line
        self.bpp = 0  # bits per pixel
        self.iformat = 0


def render_next_frame(displaydata: dict) -> int:
    if not displaydata["maze_displayed"]:
        maze_display(displaydata)
        displaydata["maze_displayed"] = True
    if displaydata["display_path"] and not displaydata["path_displayed"]:
        path_display(displaydata)


def main():
    m = Mlx()
    mlx_ptr = m.mlx_init()
    window_width = 2000
    window_height = 1000
    sidebar_width = 200
    window_width_effective = window_width - sidebar_width
    win_ptr = m.mlx_new_window(mlx_ptr, window_width, window_height,
                               "test window")
    (ret, w, h) = m.mlx_get_screen_size(mlx_ptr)
    print(f"Got screen size: {w} x {h} .")
    dimensions = {
        "window_width": window_width,
        "window_height": window_height,
        "sidebar_width": sidebar_width,
        "window_width_effective": window_width_effective,
        "Mlx": m,
        "mlx_ptr": mlx_ptr,
        "win_ptr": win_ptr,
        "test": 0xEEFFFFFF
    }
    mouse_data = {
        "sidebar_width": sidebar_width,
        "Mlx": m,
        "mlx_ptr": mlx_ptr,
        "win_ptr": win_ptr
    }
    display_data = parser(dimensions)
    m.mlx_mouse_hook(win_ptr, mymouse, mouse_data)
    m.mlx_key_hook(win_ptr, mykey, display_data)
    m.mlx_loop_hook(mlx_ptr, render_next_frame, display_data)
    m.mlx_loop(mlx_ptr)


if __name__ == "__main__":
    main()
