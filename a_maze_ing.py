import sys
from config import load_config
from maze import Maze


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Error wrong arguments!")
        quit()
    try:
        config = load_config(sys.argv[1])
    except FileNotFoundError:
        print("Config file not found")
        quit()
    maze = Maze(config["width"], config["height"])
    maze.generate_maze(config)
    grid = maze.to_hex()
    maze.write_output(config, "not yet done")
