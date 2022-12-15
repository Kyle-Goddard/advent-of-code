import numpy as np
from matplotlib import pyplot as plt
import heapq


class Node:
    """A node class for A* Pathfinding"""

    def __init__(self, parent=None, position=None):
        self.parent = parent
        self.position = position

        self.g = 0
        self.h = 0
        self.f = 0

    def __eq__(self, other):
        return (
            self.position[0] == other.position[0]
            and self.position[1] == other.position[1]
        )

    def __neq__(self, other):
        return (
            self.position[0] != other.position[0]
            or self.position[1] != other.position[1]
        )

    def __hash__(self):
        return hash( "x" + str(self.position[0]) + "y" + str(self.position[1]))

    # defining less than for purposes of heap queue
    def __lt__(self, other):
        return self.f < other.f

    # defining greater than for purposes of heap queue
    def __gt__(self, other):
        return self.f > other.f

    def height(self, z):
        return z[self.position[1]][self.position[0]]


def plot_map(x, y, z, current_coords, target_coords, visited=[], open_coords=[]):
    fig = plt.figure()
    ax = fig.add_subplot(111, projection="3d")
    ax.plot_surface(x, y, z)
    plt.title("z as 3d height map")
    ax.scatter(
        [current_coords[0]],
        [current_coords[1]],
        [2],
        c="r",
        marker="o",
    )
    ax.scatter(
        [target_coords[0]],
        [target_coords[1]],
        [28],
        c="k",
        marker="o",
    )

    visited_coords = [v.position for v in visited]
    vx = [vc[0] for vc in visited_coords]
    vy = [vc[1] for vc in visited_coords]

    open_nodes = [o.position for o in open_coords]
    ox = [oc[0] for oc in open_nodes]
    oy = [oc[1] for oc in open_nodes]

    vz = []
    for i in range(len(vx)):
        vz.append(z[vx[i]][vy[i]] + 5)
    oz = []
    for i in range(len(ox)):
        oz.append(z[ox[i]][oy[i]] + 5)

    ax.scatter(vx, vy, vz, c="r", marker=".")

    ax.scatter(ox, oy, oz, c="y", marker=".")

    ax.view_init(50, 180)

    plt.show()


def to_numpy_array(height_map):
    for i in range(len(height_map)):
        for j in range(len(height_map[i])):
            height_map[i][j] = ord(height_map[i][j]) - 96
    return np.array(height_map)


def get_coords(char, height_map):
    x = None
    y = None
    for i in range(len(height_map)):
        if char in height_map[i]:
            x = height_map[i].index(char)
            y = i

    if char == "S":
        height_map[y][x] = "a"

    if char == "E":
        height_map[y][x] = "z"

    return [x, y], height_map


def A_star(start, target, z):

    # Create start and end node
    start_node = Node(None, start)
    start_node.g = start_node.h = start_node.f = 0
    target_node = Node(None, target)
    target_node.g = target_node.h = target_node.f = 0

    # Initialize both open and closed list
    open_list = set()
    closed_list = set()

    open_list.add(start_node)

    # what squares do we search
    allow_diagonal_movement = False
    adjacent_squares = [[0, -1], [0, 1], [-1, 0], [1, 0]]
    if allow_diagonal_movement:
        adjacent_squares = [
            [0, -1],
            [0, 1],
            [-1, 0],
            [1, 0],
            [-1, -1],
            [-1, 1],
            [1, -1],
            [1, 1],
        ]

    while len(open_list) > 0:
        print(len(closed_list) / (z.shape[0] * z.shape[1]) * 100)

        # plot_map(
        #     x, y, z, current_coords, target_coords, closed_list, open_coords=open_list
        # )

        # Get the current node

        current_node = open_list[0]
        for item in enumerate(open_list):
            if item.f < current_node.f:
                current_node = item

        open_list.remove(current_node)
        closed_list.add(current_node)

        # Found the goal
        if current_node == target_node:
            path = []
            current = current_node
            while current is not None:
                path.append(current.position)
                current = current.parent
            return path[::-1]  # Return reversed path

        # Generate children
        children = {}
        for new_position in adjacent_squares:

            # Get node position
            node_position = [
                current_node.position[0] + new_position[0],
                current_node.position[1] + new_position[1],
            ]

            # Make sure within range
            if (
                node_position[0] < 0
                or node_position[1] < 0
                or node_position[0] > z.shape[1] - 1
                or node_position[1] > z.shape[0] - 1
            ):
                continue

            new_node = Node(current_node, node_position)

            # Make sure walkable terrain
            if abs(current_node.height(z) - new_node.height(z)) > 1:
                continue

            # Append
            children.add(new_node)

        # Loop through children
        for child in children:

            # Child is on the closed list
            if child in closed_list:
                continue

            # Create the f, g, and h values
            child.g = current_node.g + 1
            child.h = ((child.position[0] - target_node.position[0]) ** 2) + (
                (child.position[1] - target_node.position[1]) ** 2
            )
            child.f = child.g + child.h

            # Child is already in the open list
            if child in open_list:
                continue

            # Add the child to the open list
            open_list.add(child)


def h_score():
    return 0


with open(
    "/Users/kyle/Documents/Learning/advent-of-code/2022/day_12_hill_climbing_algorithm/input.txt",
    "r",
) as f:
    lines = f.readlines()
    height_map = []
    for line in lines:
        height_map.append([*line.strip()])

height_map.reverse()
current_coords, height_map = get_coords("S", height_map)
target_coords, height_map = get_coords("E", height_map)
z = to_numpy_array(height_map)
x, y = np.meshgrid(range(z.shape[1]), range(z.shape[0]))

# plot_map(x, y, z, current_coords, target_coords)

path = A_star(current_coords, target_coords, z)

print(path)
print(len(path) - 1)
