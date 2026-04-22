from mlx import Mlx
from images_prerender import pre_render_tiles as pre_render_images
from images_prerender import pre_render_button, pre_render_ui_env, \
    pre_render_empty
from random import shuffle


def mymouse(button, x, y, displaydata):
    buttons = displaydata["buttons"]
    m = displaydata["Mlx"]
    win_ptr = displaydata["win_ptr"]
    mlx_ptr = displaydata["mlx_ptr"]
    print(f"Got mouse event! button {button} at {x},{y}.")
    if x > 1800:
        if y < 100:
            buttons[0]
            m.mlx_put_image_to_window(mlx_ptr,
                                      win_ptr, buttons[0].pressed.img[0],
                                      1800, 0)
            displaydata["window_clear"] = True
            displaydata["maze_displayed"] = False
            displaydata["path_displayed"] = False
    # scroll up is button 4
    # scroll down is button 5


colours = [
            {
                "wall_colour": (0xEE9850AF).to_bytes(4, 'little'),
                "tunnel_colour": (0xEE000000).to_bytes(4, 'little'),
                "logo_colour": (0xEEFF00FF).to_bytes(4, "little"),
                "path_colour": (0xEE67AF50).to_bytes(4, "little")
            },
            {
                "wall_colour": (0xEEF6092A).to_bytes(4, 'little'),
                "tunnel_colour": (0xEE000000).to_bytes(4, 'little'),
                "logo_colour": (0xEEFF00FF).to_bytes(4, "little"),
                "path_colour": (0xEE09F6D5).to_bytes(4, "little")
            },
            {
                "wall_colour": (0xEE22DD4D).to_bytes(4, 'little'),
                "tunnel_colour": (0xEE000000).to_bytes(4, 'little'),
                "logo_colour": (0xEEFF00FF).to_bytes(4, "little"),
                "path_colour": (0xEEDD22B2).to_bytes(4, "little")
            },
            {
                "wall_colour": (0xEE1634E9).to_bytes(4, 'little'),
                "tunnel_colour": (0xEE000000).to_bytes(4, 'little'),
                "logo_colour": (0xEEFF00FF).to_bytes(4, "little"),
                "path_colour": (0xEEE9CB16).to_bytes(4, "little")
            },
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
        displaydata["window_clear"] = True
        displaydata["maze_displayed"] = False
    elif keynum == 114:
        displaydata["window_clear"] = True
        displaydata["maze_displayed"] = False
        displaydata["path_displayed"] = False
    elif keynum == 112:
        if displaydata["display_path"]:
            displaydata["display_path"] = False
            displaydata["maze_displayed"] = False
            displaydata["path_displayed"] = False
        else:
            displaydata["display_path"] = True
    elif keynum == 99:
        pre_colour = displaydata["colour"]
        while pre_colour == colours[0]:
            shuffle(colours)
        colour = colours[0]
        displaydata["colour"] = colour
        pre_render_images(m, mlx_ptr, ratio, colour)
        # m.mlx_sync(mlx_ptr, clear_maze(displaydata), win_ptr)
        m.mlx_sync(mlx_ptr, maze_display(displaydata), win_ptr)
        if displaydata["display_path"]:
            displaydata["path_displayed"] = False
            while not displaydata["path_displayed"]:
                path_display(displaydata)
    # elif keynum == 108:
    #     m.mlx_loop_hook(mlx_ptr, render_next_frame, displaydata)
    # elif keynum == 103:
    #     m.mlx_clear_window(mlx_ptr, win_ptr)
    #     m.mlx_sync(mlx_ptr, grow_maze(displaydata),a
    #                win_ptr)
    return displaydata


def clear_maze(displaydata: dict) -> int:
    m = displaydata["Mlx"]
    win_ptr = displaydata["win_ptr"]
    mlx_ptr = displaydata["mlx_ptr"]
    h_offset = displaydata["offset_horizontal"]
    v_offset = displaydata["offset_vertical"]
    clear = displaydata["clear"]
    m.mlx_put_image_to_window(mlx_ptr, win_ptr, clear.img,
                              h_offset, v_offset)
    return (0)


def place_logo(displaydata: dict) -> int:
    m = displaydata["Mlx"]
    win_ptr = displaydata["win_ptr"]
    mlx_ptr = displaydata["mlx_ptr"]
    tiles = displaydata["images"]
    ratio = displaydata["ratio"]
    h_offset = displaydata["offset_horizontal"]
    v_offset = displaydata["offset_vertical"]
    growth_dict = displaydata["growth_dict"]
    for cell in growth_dict["logo_cells"]:
        x, y = cell
        x = (x * ratio) + int(h_offset - (h_offset / 4))
        y = (y * ratio) + int(v_offset - (v_offset / 4))
        m.mlx_put_image_to_window(
            mlx_ptr, win_ptr, tiles[15].image.img, x, y)
    return (0)


def grow_maze(displaydata: dict) -> int:
    m = displaydata["Mlx"]
    win_ptr = displaydata["win_ptr"]
    mlx_ptr = displaydata["mlx_ptr"]
    tiles = displaydata["images"]
    maze = displaydata["maze"]
    ratio = displaydata["ratio"]
    growth_dict = displaydata["growth_dict"]
    valid_cells = growth_dict["valid_cells"]
    x, y = growth_dict["cell_coords"]
    h_offset = displaydata["offset_horizontal"]
    v_offset = displaydata["offset_vertical"]
    neighbours = growth_dict["neighbours"]
    filled_in_cells = growth_dict["filled_in_cells"]
    new_neighbours = set()
    if valid_cells - filled_in_cells == set():
        displaydata["maze_displayed"] = True
        growth_dict["filled_in_cells"] = set()
        growth_dict["neighbours"] = set()
        place_entry_exit(displaydata)
        displaydata["ui_displayed"] = False
    else:
        if neighbours == set():
            neighbours.add((x, y))
        for neighbour in neighbours:
            x, y = neighbour
            if x >= len(maze[0]) or y >= len(maze):
                growth_dict["valid_cells"] = valid_cells.remove((x, y))
                continue
            value = int(maze[y][x], 16)
            if (value >> 0 & 1 != 1):
                new_neighbours.add((x, y - 1))
            if (value >> 1 & 1 != 1):
                new_neighbours.add((x + 1, y))
            if (value >> 2 & 1 != 1):
                new_neighbours.add((x, y + 1))
            if (value >> 3 & 1 != 1):
                new_neighbours.add((x - 1, y))
            filled_in_cells.add((x, y))
            x *= ratio
            y *= ratio
            x += h_offset
            y += v_offset
            for tile in tiles:
                if value == tile.value:
                    m.mlx_put_image_to_window(
                        mlx_ptr, win_ptr, tile.image.img, x, y)
        growth_dict["neighbours"] = new_neighbours
        displaydata["growth_dict"] = growth_dict
    return (0)


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
    # clear_maze(displaydata)
    m = displaydata["Mlx"]
    win_ptr = displaydata["win_ptr"]
    mlx_ptr = displaydata["mlx_ptr"]
    tiles = displaydata["images"]
    maze = displaydata["maze"]
    ratio = displaydata["ratio"]
    x = displaydata["offset_horizontal"]
    y = displaydata["offset_vertical"]
    m.mlx_do_sync(mlx_ptr)
    place_logo(displaydata)
    for row in maze:
        for cell in row:
            for tile in tiles:
                if int(cell, 16) == tile.value:
                    if (int(cell, 16) != 0b1111):
                        m.mlx_put_image_to_window(mlx_ptr, win_ptr,
                                                  tile.image.img, x, y)
                    x += ratio
                    break
        y += ratio
        x = displaydata["offset_horizontal"]
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
    second_half = step_size - half_step
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
            y -= second_half
        case "E":
            x += half_step
            tile = tiles[17]
            m.mlx_put_image_to_window(mlx_ptr, win_ptr, tile.image.img,
                                      x, y)
            x += second_half
        case "S":
            y += half_step
            tile = tiles[18]
            m.mlx_put_image_to_window(mlx_ptr, win_ptr, tile.image.img,
                                      x, y)
            y += second_half
        case "W":
            x -= half_step
            tile = tiles[19]
            m.mlx_put_image_to_window(mlx_ptr, win_ptr, tile.image.img,
                                      x, y)
            x -= second_half
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
    cells_logo = set()
    valid_cells = set()
    x, y = (0, 0)
    maze_end = False
    with open(file_name, "r") as maze:
        for line in maze:
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
                Grid.append(Row)
    entry = Grid[-3]
    exit = Grid[-2]
    path = Grid[-1]
    Grid = Grid[:-3]
    window_width = dimensions["window_width"]
    window_width_effective = (dimensions["window_width_effective"]
                              - dimensions["offset_horizontal"])
    window_height = dimensions["window_height"]
    window_height_effective = (window_height -
                               (dimensions["offset_vertical"] * 2))
    ratio_horizontal = (window_width_effective / len(Grid[0]))
    ratio_vertical = (window_height_effective / len(Grid))
    if ratio_horizontal < ratio_vertical:
        ratio = int(ratio_horizontal)
    else:
        ratio = int(ratio_vertical)
    images = pre_render_images(m, mlx_ptr, ratio, colours[0])
    buttons = pre_render_button(m, mlx_ptr)
    ui = pre_render_ui_env(m, mlx_ptr, (window_width, window_height))
    maze_clear = pre_render_empty(m, mlx_ptr, (ratio * len(Grid[0]),
                                               (ratio * len(Grid[0]))))
    neighbours = set()
    filled_in_cells = set()
    h_offsett = dimensions["offset_horizontal"]
    v_offset = dimensions["offset_vertical"]
    growth_dict = {
        "logo_cells": cells_logo,
        "cell_coords": (0, 0),
        "neighbours": neighbours,
        "valid_cells": valid_cells,
        "filled_in_cells": filled_in_cells
    }
    display_data = {
        "ui": ui,
        "clear": maze_clear,
        "maze_displayed": False,
        "path_displayed": False,
        "display_path": False,
        "images": images,
        "maze": Grid,
        "entry": (int((int(entry[0]) * ratio)) + h_offsett,
                  int((int(entry[1]) * ratio)) + v_offset),
        "exit": (int((int(exit[0]) * ratio)) + h_offsett,
                 int((int(exit[1]) * ratio)) + v_offset),
        "path": path,
        "ratio": ratio,
        "Mlx": m,
        "mlx_ptr": mlx_ptr,
        "win_ptr": win_ptr,
        "path_coords": (int((int(entry[0]) * ratio)) + h_offsett,
                        int((int(entry[1]) * ratio)) + v_offset),
        "path_pos": 0,
        "growth_dict": growth_dict,
        "window_clear": False,
        "buttons": buttons,
        "ui_displayed": False,
        "colour": colours[0],
        "offset_horizontal": h_offsett,
        "offset_vertical": v_offset
    }
    return (display_data)


def display_ui(displaydata: dict):
    m = displaydata["Mlx"]
    win_ptr = displaydata["win_ptr"]
    mlx_ptr = displaydata["mlx_ptr"]
    buttons = displaydata["buttons"]
    ui = displaydata["ui"]
    x, y = (1800, 0)
    m.mlx_put_image_to_window(mlx_ptr, win_ptr, ui.img, 0, 0)
    for button in buttons:
        m.mlx_put_image_to_window(mlx_ptr, win_ptr, button.image.img[0],
                                  x, y)
        y += 100


def render_next_frame(displaydata: dict) -> int:
    m = displaydata["Mlx"]
    win_ptr = displaydata["win_ptr"]
    # mlx_ptr = displaydata["mlx_ptr"]
    m.mlx_mouse_hook(win_ptr, mymouse, displaydata)
    m.mlx_key_hook(win_ptr, mykey, displaydata)
    display_ui(displaydata)
    if displaydata["window_clear"]:
        clear_maze(displaydata)
        displaydata["window_clear"] = False
    elif not displaydata["maze_displayed"]:
        place_logo(displaydata)
        grow_maze(displaydata)
    elif displaydata["display_path"] and not displaydata["path_displayed"]:
        path_display(displaydata)
    else:
        m.SYNC_WIN_COMPLETED
        m.SYNC_WIN_FLUSH


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
        "offset_horizontal": 10,
        "offset_vertical": 10
    }
    # mouse_data = {
    #     "sidebar_width": sidebar_width,
    #     "Mlx": m,
    #     "mlx_ptr": mlx_ptr,
    #     "win_ptr": win_ptr
    # }
    display_data = parser(dimensions)
    m.mlx_loop_hook(mlx_ptr, render_next_frame, display_data)
    m.mlx_loop(mlx_ptr)


if __name__ == "__main__":
    main()
