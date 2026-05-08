from mlx import Mlx
from random import shuffle, randint
from config import load_config
from mazegen.maze import Maze
from timeit import default_timer as timer
from Display import Display


def mymouse(button: int, x: int, y: int, displaydata: Display) -> None:
    m = displaydata.m
    win_ptr = displaydata.win_ptr
    mlx_ptr = displaydata.mlx_ptr
    boundary = displaydata.width - displaydata.sidebar
    if button != 1:
        return
    if x > boundary:
        if y < 100:
            update_configs((None, None))
            displaydata.loading = True
            displaydata.clear = True
            displaydata.path_displayed = False
            displaydata.display_path = False
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
            logo_pre_colour = displaydata.logo_colours[0]
            while logo_pre_colour == displaydata.logo_colours[0]:
                shuffle(displaydata.logo_colours)
            displaydata.update_logo_colour(displaydata.logo_colours[0])
            m.mlx_sync(mlx_ptr, displaydata.pre_render_images(), win_ptr)
            m.mlx_sync(mlx_ptr, displaydata.maze_update(), win_ptr)
            if displaydata.display_path:
                displaydata.path_displayed = False
                while not displaydata.path_displayed:
                    displaydata.path_display()
        elif y < 500:
            if displaydata.algo_change:
                displaydata.algo_change = False
            else:
                displaydata.algo_change = True
            update_configs((None, None))
            displaydata.loading = True
            displaydata.clear = True
            displaydata.path_displayed = False
            displaydata.display_path = False
        elif y < 600:
            update_configs(("perfect", "False"))
            displaydata.loading = True
            displaydata.clear = True
            displaydata.path_displayed = False
            displaydata.display_path = False
    # scroll up is button 4
    # scroll down is button 5


def mykey(keynum: int, displaydata: Display) -> Display:
    m = displaydata.m
    win_ptr = displaydata.win_ptr
    mlx_ptr = displaydata.mlx_ptr
    if keynum == 32:
        m.mlx_mouse_hook(win_ptr, None, None)
    elif keynum == 65307:
        print("closing")
        m.mlx_destroy_window(mlx_ptr, win_ptr)
        m.mlx_loop_exit(mlx_ptr)
    elif keynum == 97:
        displaydata.clear = False
    elif keynum == 114:
        update_configs(("asd", "False"))
        displaydata.loading = True
        displaydata.clear = True
        displaydata.path_displayed = False
        displaydata.display_path = False
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
    return displaydata


def close_window(display: Display) -> int:
    print("closing")
    display.m.mlx_destroy_window(display.mlx_ptr, display.win_ptr)
    display.m.mlx_loop_exit(display.mlx_ptr)
    return (0)


def render_next_frame(display: Display) -> None:
    if not display.ui_displayed:
        if display.loading:
            display.img_to_window_mine(display.loading_img,
                                       int(display.width / 2) - 100,
                                       int(display.height / 2) - 50)
            display.loading = False
        elif display.start_up:
            display.parsing()
            display.clear_maze()
            display.start_up = False
            display.m.SYNC_WIN_FLUSH
        else:
            display.display_ui()
            display.ui_displayed = True
    elif display.clear and not display.cleared:
        display.clear_maze()
        if display.loading:
            display.img_to_window_mine(display.loading_img,
                                       display.center_x - 100,
                                       display.center_y - 50)
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
        else:
            display.end = timer()
            if (display.end - display.start) < 30:
                display.grow_maze()
            else:
                display.neighbours = set()
                display.maze_update()
    elif display.display_path and not display.path_displayed:
        display.path_display()
    else:
        display.m.mlx_mouse_hook(display.win_ptr, mymouse, display)
        display.m.mlx_key_hook(display.win_ptr, mykey, display)
        display.m.mlx_hook(display.win_ptr, 33, 0, close_window, display)
        display.m.SYNC_WIN_COMPLETED
        display.m.SYNC_WIN_FLUSH


def new_maze_stuff(displaydata: Display) -> None:
    try:
        config = load_config("config.txt")
    except FileNotFoundError:
        print("Config file not found")
        quit()
    maze = Maze(config["width"], config["height"])
    if displaydata.algo_change:
        maze.Loop_erased_random_walk(config)
    else:
        maze.generate_maze(config)
    maze.to_hex()
    path = maze.bfs_solver(config["entry"], config["exit"])
    maze.write_output(config, path)
    if not displaydata.start_up:
        displaydata.parsing()
        displaydata.loading = False


def update_configs(key_value: tuple) -> None:
    key_new, value_new = key_value
    try:
        config = load_config("config.txt")
    except FileNotFoundError:
        print("Config file not found")
        quit()
    with open("config.txt", "w") as file:
        i = 0
        for key, value in config.items():
            if key == key_new:
                if key == "perfect" and value:
                    value = False
                elif key == "perfect" and not value:
                    value = True
                else:
                    value = value_new
            elif "(" in str(value):
                x, y = value
                value = f"{x},{y}"
            if key == "seed":
                value = randint(0, 999999)
            i += 1
            file.write(f"{key.upper()}={value}\n")


def start_visual() -> None:
    m = Mlx()
    mlx_ptr = m.mlx_init()
    window_width = 1700
    window_height = 1500
    (ret, w, h) = m.mlx_get_screen_size(mlx_ptr)
    win_ptr = m.mlx_new_window(mlx_ptr, window_width, window_height,
                               "test window")
    display = Display(m, mlx_ptr, win_ptr, (window_width, window_height))
    new_maze_stuff(display)
    m.mlx_loop_hook(display.mlx_ptr, render_next_frame, display)
    m.mlx_loop(mlx_ptr)


if __name__ == "__main__":
    start_visual()
