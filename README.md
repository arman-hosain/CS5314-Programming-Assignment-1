# CS5314-Programming-Assignment-1
 
# A* and Dijkstra's Algorithm Pathfinding Implementation

This repository contains Python implementations of the **A\*** and **Dijkstra's** algorithms for pathfinding in grid-based environments. The algorithms are designed to solve pathfinding problems using heuristic-driven (A*) and uniform-cost (Dijkstra) search strategies, with support for cycle detection and customizable heuristics (Manhattan and Euclidean distances).

## Table of Contents

- [Features](#features)
- [Prerequisites](#prerequisites)
- [Setup](#setup)
- [Usage](#usage)
  - [Running the A* Algorithm](#running-the-a-algorithm)
  - [Running the Dijkstra's Algorithm](#running-dijkstras-algorithm)
  - [Input Grid File Format](#input-grid-file-format)

---

## Features

- A* algorithm implementation with two heuristic functions:
  - **Manhattan Distance**: For grids where only horizontal and vertical movement is allowed.
  - **Euclidean Distance**: For grids where diagonal movement is allowed.
  
- Dijkstra's algorithm implementation for pathfinding.
  
- Cycle detection to avoid revisiting nodes unnecessarily.

- Outputs the following for both algorithms:
  - Path from start to goal.
  - Cost of the path.
  - Number of nodes expanded during the search.
  - Whether cycles were detected.

---

## Prerequisites

Before running the code, ensure that you have the following installed on your machine:

1. **Python 3.x**: The project is implemented in Python.
2. **pip**: Python package installer.

You will also need to install the `heapq` module (standard in Python).

---

## Setup

1. **Clone the repository**:
   
   ```bash
   git clone https://github.com/your-username/pathfinding-a-star-dijkstra.git
   cd pathfinding-a-star-dijkstra

## Usage

### Running the A* Algorithm

The A* algorithm can be run using the following command:

```bash
    python a_star.py <input_grid.txt> <heuristic>
   ```
`<input_grid.txt>`: Path to the input file containing the grid definition.

`<heuristic>`: The heuristic to use. It can be either:
- `manhattan`: For grids where only horizontal and vertical movement is allowed.
- `euclidean`: For grids where diagonal movement is allowed.
- 

### Running Dijkstra's Algorithm

The Dijkstra's algorithm can be run using the following command:

```bash
python dijkstra.py <input_grid.txt>
```
`<input_grid.txt>`: Path to the input file containing the grid definition.


### Input Grid File Format

The input grid file should follow this format:

- The grid is a 2D matrix with values between `0` and `5`:
  - `0`: Represents an obstacle (unpassable).
  - `1-5`: Represents the cost of traversing the cell (with `5` being the most expensive).

The file should also include the start and goal positions, like so:

```plaintext
1 1 1 1 1
0 0 0 5 5
5 5 5 5 0
5 1 1 1 5
5 5 5 0 5

Start: (0,0)
Goal: (4,4)
