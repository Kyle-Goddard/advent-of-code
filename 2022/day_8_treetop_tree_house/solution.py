import numpy as np

with open(
    "/Users/kyle/Documents/Learning/advent-of-code/2022/day_8_treetop_tree_house/puzzle_input.txt",
    "r",
) as file:
    lines = file.readlines()

lines = [l.strip() for l in lines]

trees = np.zeros((len(lines), len(lines[0])))

for i in range(len(lines)):
    for j in range(len(lines[0])):
        trees[i, j] = int(lines[i][j])

vis_map = np.zeros_like(trees)

for i in range(vis_map.shape[0]):
    for j in range(vis_map.shape[1]):
        vert = trees[:, j]
        horz = trees[i, :]

        top = vert[:i]
        bottom = vert[i + 1 :]
        left = horz[:j]
        right = horz[j + 1 :]

        this_tree = trees[i, j]

        if len(top) == 0 or len(bottom) == 0 or len(left) == 0 or len(right) == 0:
            vis_map[i, j] = 1

        elif (
            this_tree > max(top)
            or this_tree > max(bottom)
            or this_tree > max(left)
            or this_tree > max(right)
        ):
            vis_map[i, j] = 1

print(sum(sum(vis_map)))


vis_map = np.zeros_like(trees)


def view_distance(current_height, tree_row):
    view_dist = []
    for t in tree_row:
        if t < current_height:
            view_dist.append(1)
        else:
            view_dist.append(1)
            break

    return sum(view_dist)


for i in range(vis_map.shape[0]):
    for j in range(vis_map.shape[1]):
        vert = trees[:, j]
        horz = trees[i, :]

        top = vert[:i]
        bottom = vert[i + 1 :]
        left = horz[:j]
        right = horz[j + 1 :]

        this_tree = trees[i, j]

        top_view = view_distance(this_tree, top[::-1])
        bottom_view = view_distance(this_tree, bottom)
        left_view = view_distance(this_tree, left[::-1])
        right_view = view_distance(this_tree, right)

        vis_map[i, j] = top_view * bottom_view * left_view * right_view

print(np.amax(vis_map))
