import heapq


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


# Heuristic functions
def manhattan_heuristic(a, b):
    return abs(a[0] - b[0]) + abs(a[1] - b[1])


def euclidean_heuristic(a, b):
    return ((a[0] - b[0]) ** 2 + (a[1] - b[1]) ** 2) ** 0.5


# A* Algorithm with Cycle Detection
def a_star(grid, start, goal, heuristic_func):
    rows, cols = len(grid), len(grid[0])
    open_list = []
    heapq.heappush(open_list, (0, start))
    came_from = {}
    g_score = {start: 0}
    f_score = {start: heuristic_func(start, goal)}
    visited = set()
    nodes_expanded = 0
    cycles_detected = False

    while open_list:
        current = heapq.heappop(open_list)[1]
        if current in visited:
            cycles_detected = True
            continue

        # If goal is reached, reconstruct the path
        if current == goal:
            path = []
            while current in came_from:
                path.append(current)
                current = came_from[current]
            path.append(start)
            return path[::-1], g_score[goal], nodes_expanded, "YES" if cycles_detected else "NO"

        visited.add(current)
        nodes_expanded += 1

        # Neighbors of the current node
        neighbors = [(current[0] + i, current[1] + j) for i, j in [(0, 1), (1, 0), (0, -1), (-1, 0)]]
        for neighbor in neighbors:
            if 0 <= neighbor[0] < rows and 0 <= neighbor[1] < cols and grid[neighbor[0]][neighbor[1]] != 0:
                tentative_g_score = g_score[current] + grid[neighbor[0]][neighbor[1]]

                if neighbor not in g_score or tentative_g_score < g_score[neighbor]:
                    came_from[neighbor] = current
                    g_score[neighbor] = tentative_g_score
                    f_score[neighbor] = tentative_g_score + heuristic_func(neighbor, goal)
                    heapq.heappush(open_list, (f_score[neighbor], neighbor))

    return None, None, nodes_expanded, "YES" if cycles_detected else "NO"  # No path found


# Main function
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

    path, cost, nodes_expanded, cycles_detected = a_star(grid, start, goal, heuristic)

    if path:
        print("Path:", path)
        print("Cost:", cost)
    else:
        print("No path found")

    print("Nodes Expanded:", nodes_expanded)
    print("Cycles Detected:", cycles_detected)
