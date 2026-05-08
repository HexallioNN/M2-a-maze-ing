# *This project has been created as part of the 42 curriculum by maavan-d, ikalach.*

# A-Maze-ing

## Description

A-Maze-ing is a maze generation and visualization project developed in Python using the MiniLibX graphics library.  
The project generates random mazes, converts them into a renderable hexadecimal representation, and visualizes them in real time through a graphical interface.

The goal of the project is to explore:
- maze generation algorithms,
- graphical rendering,
- event-driven programming,
- file parsing,
- and reusable software architecture.

The program supports:
- dynamic maze generation,
- animated maze rendering,
- path visualization,
- configurable colors,
- and interactive controls through keyboard and mouse input.

---

# Features

- Random maze generation
- Real-time graphical rendering
- Animated maze growth effect
- Pathfinding visualization
- Dynamic color switching
- Logo rendering
- Configurable maze dimensions
- Interactive controls
- Reusable maze generation system
- Configurable maze generation algorithm

---

# Instructions

---

## Running the project

Execute:

```bash
python3 a_maze_ing.py config.txt
```

---

# Config File Structure

The project uses a `config.txt` file.

Example:

```text
WIDTH=20
HEIGHT=15
ENTRY=0,0
EXIT=19,14
OUTPUT_FILE=maze.txt
PERFECT=True
```

---

# Maze File Structure

Example:

```text
ffffffffff
f00000000f
f0fffff00f
f0f000f00f
f0f0f0f00f
f0f0f0f00f
f0f000f00f
f0fffff00f
f00000000f
ffffffffff

1,1
8,8
EEEEEEEESSSSSSS
```

## Structure

1. Maze grid represented in hexadecimal characters
2. Empty line separator
3. Entry coordinates
4. Exit coordinates
5. Path directions

---

# Maze Generation Algorithm

## Chosen Algorithm

The project uses a randomized maze generation algorithm based on recursive carving/backtracking principles.

The algorithm:
1. Starts from an initial cell
2. Randomly selects neighboring cells
3. Removes walls between valid neighbors
4. Continues until all cells are visited

The generated maze guarantees:
- full connectivity,
- no isolated sections,
- and a valid path between entry and exit.

---

# Reusable Components

Several parts of the project are reusable:

## Maze Generator
The maze generation code can be downloaded using:

```bash
pip install mazegen-1.0.0-py3-none-any.whl
```

To use the downloaded maze generation algorithm ["WIDTH", "HEIGHT", "ENTRY", "EXIT", "OUTPUT_FILE", "PERFECT"] parameters should be given to the algorithm 

---

# AI Usage

AI tools were used for:
- debugging assistance,
- parsing fixes,
- documentation improvements.

AI was not used to fully generate the project, but rather as a support tool for:
- troubleshooting,
- understanding concepts.

---

# Resources

## Documentation

- Python Documentation  
  https://docs.python.org/3/

- MiniLibX Documentation  
  https://harm-smits.github.io/42docs/libs/minilibx

- 42 Documentation  
  https://github.com/harm-smits/42docs

---
