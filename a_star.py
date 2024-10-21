import heapq


class Node:
    """
    A node class for A* Pathfinding with cycle detection.
    """

    def __init__(self, parent=None, position=None):
        self.parent = parent
        self.position = position
        self.g = 0  # Cost from start to the node
        self.h = 0  # Heuristic cost to the goal
        self.f = 0  # Total cost g + h

    def __eq__(self, other):
        return self.position == other.position

    def __lt__(self, other):
        return self.f < other.f


# Function to read the grid from a file
def read_grid(file_path):
    with open(file_path, 'r') as f:
        # Split the text into lines
        lines = f.read().strip().splitlines()
        grid = []
        start = None
        goal = None

        for line in lines:
            if line.startswith("Start:"):
                start = tuple(map(int, line.split("Start:")[1].strip()[1:-1].split(',')))
            elif line.startswith("Goal:"):
                goal = tuple(map(int, line.split("Goal:")[1].strip()[1:-1].split(',')))
            else:
                # Add the grid row to the grid list
                grid.append([int(x) for x in line.split()])

        grid = [row for row in grid if row]

        return grid, start, goal


def return_path(current_node):
    path = []
    while current_node:
        path.append(current_node.position)
        current_node = current_node.parent
    return path[::-1]  # Return reversed path


def a_star_with_cycle_detection(grid, start, goal, heuristic_func, allow_diagonal=False):
    """
    Implements A* algorithm with cycle detection.
    :param grid: 2D grid containing values from 0 to 5
    :param start: Tuple of start coordinates (row, col)
    :param goal: Tuple of goal coordinates (row, col)
    :param heuristic_func: Heuristic function (manhattan/euclidean)
    :return: Path, cost, nodes expanded, and cycle detection result
    """
    # Create start and end node
    start_node = Node(None, start)
    goal_node = Node(None, goal)

    open_list = []
    visited = set()
    nodes_expanded = 0
    cycles_detected = False

    heapq.heappush(open_list, start_node)

    g_score = {start: 0}  # Actual cost from start to each node
    f_score = {start: heuristic_func(start, goal)}  # Total estimated cost (g + h)

    while open_list:
        current_node = heapq.heappop(open_list)
        current_position = current_node.position

        # If the goal is reached, return the results
        if current_position == goal:
            path = return_path(current_node)
            return path, g_score[goal], nodes_expanded, "YES" if cycles_detected else "NO"


        # Mark the node as visited
        visited.add(current_position)
        nodes_expanded += 1

        # Get neighbors (up, down, left, right)

        # Determine neighbors based on whether diagonal movement is allowed
        if allow_diagonal:
            # Include diagonal neighbors
            neighbors_pos = [(0, 1), (1, 0), (0, -1), (-1, 0), (1, 1), (1, -1), (-1, 1), (-1, -1)]
            neighbors = [(current_position[0] + dx, current_position[1] + dy)
                         for dx, dy in neighbors_pos]
        else:
            # Only horizontal and vertical neighbors
            neighbors_pos = [(0, 1), (1, 0), (0, -1), (-1, 0)]
            neighbors = [(current_position[0] + dx, current_position[1] + dy)
                         for dx, dy in neighbors_pos]

        neighbors = [(current_position[0] + dx, current_position[1] + dy)
                     for dx, dy in [(0, 1), (1, 0), (0, -1), (-1, 0)]]

        for neighbor in neighbors:
            # Make sure the neighbor is within the bounds of the grid
            if (0 <= neighbor[0] < len(grid)) and (0 <= neighbor[1] < len(grid[0])):
                # Skip if it's an obstacle
                if grid[neighbor[0]][neighbor[1]] == 0:
                    continue

                # Check if we revisited a node (cycle detection)
                if neighbor in visited:
                    cycles_detected = True
                    continue

                tentative_g_score = g_score[current_position] + grid[neighbor[0]][neighbor[1]]

                # If this path to the neighbor is better, or it's not visited yet
                if neighbor not in g_score or tentative_g_score < g_score[neighbor]:
                    g_score[neighbor] = tentative_g_score
                    f_score[neighbor] = tentative_g_score + heuristic_func(neighbor, goal)

                    new_node = Node(current_node, neighbor)
                    new_node.g = g_score[neighbor]
                    new_node.f = f_score[neighbor]

                    heapq.heappush(open_list, new_node)

    # If the goal is not reachable, return None
    return None, None, nodes_expanded, "YES" if cycles_detected else "NO"


# Heuristic functions
def manhattan_heuristic(a, b):
    return abs(a[0] - b[0]) + abs(a[1] - b[1])


def euclidean_heuristic(a, b):
    return ((a[0] - b[0]) ** 2 + (a[1] - b[1]) ** 2) ** 0.5


# Main function for testing
if __name__ == "__main__":
    import sys

    if len(sys.argv) != 3:
        print("Usage: python a_star.py <input_grid.txt> <heuristic>")
        sys.exit(1)

    input_file = sys.argv[1]
    heuristic_name = sys.argv[2]

    grid, start, goal = read_grid(input_file)

    if heuristic_name == "manhattan":
        heuristic = manhattan_heuristic
    elif heuristic_name == "euclidean":
        heuristic = euclidean_heuristic
    else:
        print("Invalid heuristic name. Use 'manhattan' or 'euclidean'.")
        sys.exit(1)

    # Call the A* algorithm with Manhattan heuristic
    path, cost, nodes_expanded, cycles_detected = a_star_with_cycle_detection(grid, start, goal, heuristic)

    if path:
        print("Path:", path)
        print("Cost:", cost)
    else:
        print("No path found")

    print("Nodes Expanded:", nodes_expanded)
    print("Cycles Detected:", cycles_detected)
