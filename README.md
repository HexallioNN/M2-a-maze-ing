*This project has been created as part of the 42 curriculum by maavan-d, ikalach.*

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

We recommended excuting the following script to install the requirements in a virtual enviroment and run the project smoothly:

```bash
python -m venv venv
source venv/bin/activate
make install
make run
```

in order to check the linting of this project run it in the virtual enviroment using

```bash
make lint
make lint-strict
```

Execute:

```bash
python3 a_maze_ing.py config.txt
```

<img width="1280" height="720" alt="Maze GIF from CloudConvert" src="https://github.com/user-attachments/assets/b0b942e1-aa5e-457a-a5b0-fed4fbb60a0f" />

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
D53D5511553D51395153
D3C553E83D4396EABAD2
96917C3AC53C693AAC3A
83AC556A93C556A847AA
AAA955546A9557AA93AA
AC6C393FBAAFFFAAAC6A
A953EAAFC4057FC6AD16
C6BC56AFFFAFFF93C3C7
954553A93FAFD52A9293
AB9552AAAFEFFFAC6EAA
C2C396C6C5393D41556A
BC3AC57913AAC53E9392
87AA9556AAC697A96C6A
A96AC393AE93856A953A
C47C546EC56C4556C7C6

0, 0
19, 14
EESEEESESWWWNWSSSWNNWSSSSENEESEENNESSSSSENNESSEESSENNESEESSWWSEEENNENESENESSS
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

This project uses two distinct algorithm for randomized maze generation. The first algorithm is a modified version of depth first search relying on recursive carving/backtracking principles. The second algorithm is an loop erased random walk algorithm

The depth first search algorithm:
1. Starts from an initial cell
2. Randomly selects neighboring cells
3. Removes walls between valid neighbors
4. Continues until all cells are visited


The loop erased random walk algorithm:
1. Pick a random cell and marks this a part of the maze
2. Pick a secondary random cell from the remaining valid cells and add it to path
3. Randomly pick a neighbour from this second cell and add to path
4. Repeat this process until the path reaches a cell thats in the maze
5. If the path contains any loop cut the loop from the path
6. remove the walls along the path and add all cell with in it too the maze
7. repeat this with a new random cell until all cells are part if the maze

The generated maze guarantees:
- full connectivity,
- no isolated sections,
- and a valid path between entry and exit.

A second algorithm was used 

---

# Reusable Components

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
