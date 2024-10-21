import heapq

class Node:
    def __init__(self, position, g):
        self.position = position  # (x, y) position on the grid
        self.g = g  # Actual cost from start to this node

    def __lt__(self, other):
        return self.g < other.g

def dijkstra_search(grid, start, goal):
    open_list = []
    heapq.heappush(open_list, Node(start, 0))  # Push the start node with cost 0
    came_from = {}
    g_score = {start: 0}  # Distance to start is 0
    visited = set()  # To track visited nodes

    while open_list:
        current_node = heapq.heappop(open_list)
        current_position = current_node.position

        # If the current node is the goal, reconstruct the path
        if current_position == goal:
            path = []
            while current_position in came_from:
                path.append(current_position)
                current_position = came_from[current_position]
            path.append(start)
            path.reverse()  # Reverse the path to get it from start to goal
            return path, g_score[goal], len(visited)

        # Mark the node as visited
        visited.add(current_position)

        # Explore neighbors (up, down, left, right)
        neighbors = [(0, 1), (1, 0), (0, -1), (-1, 0)]
        for dx, dy in neighbors:
            neighbor = (current_position[0] + dx, current_position[1] + dy)

            # Ensure neighbor is within bounds and is not an obstacle
            if not (0 <= neighbor[0] < len(grid) and 0 <= neighbor[1] < len(grid[0])):
                continue  # Out of bounds
            if grid[neighbor[0]][neighbor[1]] == 0:  # Obstacle
                continue

            tentative_g_score = g_score[current_position] + grid[neighbor[0]][neighbor[1]]

            # Only consider this neighbor if the new path cost is better
            if tentative_g_score < g_score.get(neighbor, float('inf')):
                came_from[neighbor] = current_position
                g_score[neighbor] = tentative_g_score
                heapq.heappush(open_list, Node(neighbor, tentative_g_score))

    return None, float('inf'), len(visited)  # Return None if no path is found

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


if __name__ == "__main__":
    import sys

    if len(sys.argv) != 2:
        print("Usage: python dijkstra.py <input_grid.txt>")
        sys.exit(1)

    input_file = sys.argv[1]
    grid, start, goal = read_grid(input_file)

    # Run Dijkstra's algorithm
    path, cost, nodes_expanded = dijkstra_search(grid, start, goal)

    if path:
        print(f"Path: {path}")
        print(f"Cost: {cost}")
    else:
        print("No path found.")
    print(f"Nodes Expanded: {nodes_expanded}")
