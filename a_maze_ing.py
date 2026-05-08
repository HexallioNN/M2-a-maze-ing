import sys
from config import load_config
from mazegen.maze import Maze
from maze_visualization import start_visual
# from collections import deque


# def get_neighbors(maze: Maze, x: int, y: int) -> list:
#     directions = {
#         'N': (0, -1),
#         'S': (0, 1),
#         'E': (1, 0),
#         'W': (-1, 0)
#     }
#     neighbors = []
#     cell = maze.cell_at(x, y)
#     for dir_name, (dx, dy) in directions.items():
#         nx, ny = x + dx, y + dy
#         if 0 <= nx < maze.nx and 0 <= ny < maze.ny:
#             if not cell.walls[dir_name]:
#                 neighbors.append((nx, ny, dir_name))
#     return neighbors


# def bfs_solver(maze: Maze, start, end) -> str:
#     queue = deque([start])
#     visited = set([start])
#     parent = {start: None}
#     direction_from_parent = {start: None}

#     while queue:
#         current = queue.popleft()
#         if current == end:
#             break
#         for nx, ny, dir_name in get_neighbors(maze, current[0], current[1]):
#             if (nx, ny) not in visited:
#                 visited.add((nx, ny))
#                 queue.append((nx, ny))
#                 parent[(nx, ny)] = current
#                 direction_from_parent[(nx, ny)] = dir_name
#     if end not in parent:
#         return "Maze not solveable"
#     path: list = []
#     current = end
#     while current != start:
#         path.append(direction_from_parent[current])
#         current = parent[current]
#     path.reverse()
#     return ''.join(path)


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
    entry = config["entry"]
    exit = config["exit"]
    path = maze.bfs_solver(entry, exit)
    maze.write_output(config, path)
    start_visual()
