from mlx import Mlx
from random import shuffle, randint
from config import load_config
from mazegen.maze import Maze
from timeit import default_timer as timer
from Display import Display
from typing import Any
"""
This module governs the visualization of the maze using mlx

In this module al logic in regard to the interface and deploying
of the mazegen module is housed, using the Display class from the
Display.py module and the images from the images_prerender module
this module determines what the render to the display when and responds
key and mouse events
"""


def mymouse(button: int, x: int, y: int, displaydata: Display) -> None:
    """
    This function responds to mouse events

    Args:
        button: this is the button pressed on the mouse
        with 1 representing the left mouse button 2 the right,
        3 represent clicking the scroll wheel and 4 and five are
        scrolling up and down respectively
        x, y: these represent the x and y coordinates of where the
        mouse event occured, this is in pixels
        displaydata: this is the Display on which the event occured

    this function then checks where on the screen the event occured
    and wether it was a left mouse click, it then updates the flags
    in displaydata accordingly
    """
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
    """
    This is an outdated function that intercept keyboard events

    Args:
        keynum: this is an interger representation of the key
        pressed
        displaydata: Is the display we want the event to be
        associated with

        much like the mymouse function this function deals with
        updating whats on the display based on the events but it
        is no longer the primarily used function for this and has been
        left primarly for later references
    """
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
    """This function Closes the window"""
    print("closing")
    display.m.mlx_destroy_window(display.mlx_ptr, display.win_ptr)
    display.m.mlx_loop_exit(display.mlx_ptr)
    return (0)


def render_next_frame(display: Display) -> None:
    """
    This function governs the rendering of the frame displayed

    This function is the back bone of the animations used in
    this project, using the flag in the Display class it allows
    for frame by frame updating of processes
    """
    if not display.ui_displayed:
        if display.loading and not display.running:
            display.img_to_window_mine(display.loading_img,
                                       int(display.width / 2) - 100,
                                       int(display.height / 2) - 50)
            display.loading = False
            display.running = True
        elif display.start_up:
            display.parsing()
            display.clear_maze()
            display.start_up = False
            display.m.SYNC_WIN_FLUSH
        else:
            display.m.mlx_sync(display.mlx_ptr,
                               display.display_ui(),
                               display.win_ptr)
            display.ui_displayed = True
    elif display.clear and not display.cleared:
        display.m.mlx_sync(display.mlx_ptr,
                           display.clear_maze(),
                           display.win_ptr)
        display.m.mlx_sync(display.mlx_ptr,
                           display.display_ui(),
                           display.win_ptr)
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
        display.loading = False
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
    """This function governs the regeration of the maze"""
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
        # displaydata.loading = False


def update_configs(key_value: tuple[Any, Any]) -> None:
    """This function updates the configs.txt of the maze"""
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
                value = f"{x}, {y}"
            if key == "seed":
                value = randint(0, 999999)
            i += 1
            file.write(f"{key.upper()}={value}\n")


def start_visual() -> None:
    """This function starts the visualization of the maze"""
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
