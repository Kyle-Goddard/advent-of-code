import numpy as np

NORTH = "N"
SOUTH = "S"
EAST = "E"
WEST = "W"

order_of_movement = [NORTH, SOUTH, WEST, EAST]


class Elf:
    def __init__(self, x, y) -> None:
        self.x = x
        self.y = y
        self.x_new = None
        self.y_new = None

    def __repr__(self) -> str:
        return f"[{self.x},{self.y}]"

    def position(self):
        return [self.x, self.y]

    def new_position(self):
        return [self.x_new, self.y_new]

    def _move_is_needed(self, elf_map):
        surrounding_space = [
            [1, 0],
            [0, 1],
            [0, -1],
            [-1, 0],
            [1, 1],
            [-1, -1],
            [1, -1],
            [-1, 1],
        ]
        for s in surrounding_space:
            if [self.x + s[0], self.y + s[1]] in elf_map:
                return True
        return False

    def propose_move(self, elf_map, preferred_direction):
        if not self._move_is_needed(elf_map):
            self.x_new = None
            self.y_new = None
            return [self.x_new, self.y_new]

        preferred_dir = order_of_movement.index(preferred_direction)

        for i in range(4):
            dir_idx = (preferred_dir + i) % 4
            moves = {1: [], 2: [], 3: []}

            if order_of_movement[dir_idx] == NORTH:
                moves[1] = [self.x, self.y + 1]
                moves[2] = [self.x + 1, self.y + 1]
                moves[3] = [self.x - 1, self.y + 1]

            elif order_of_movement[dir_idx] == SOUTH:
                moves[1] = [self.x, self.y - 1]
                moves[2] = [self.x + 1, self.y - 1]
                moves[3] = [self.x - 1, self.y - 1]

            elif order_of_movement[dir_idx] == EAST:
                moves[1] = [self.x + 1, self.y]
                moves[2] = [self.x + 1, self.y - 1]
                moves[3] = [self.x + 1, self.y + 1]

            elif order_of_movement[dir_idx] == WEST:
                moves[1] = [self.x - 1, self.y]
                moves[2] = [self.x - 1, self.y - 1]
                moves[3] = [self.x - 1, self.y + 1]

            if (
                moves[1] not in elf_map
                and moves[2] not in elf_map
                and moves[3] not in elf_map
            ):
                self.x_new = moves[1][0]
                self.y_new = moves[1][1]
                break
            else:
                self.x_new = None
                self.y_new = None

        return [self.x_new, self.y_new]

    def make_move(self):
        if self.x_new != None:
            self.x = self.x_new
        if self.y_new != None:
            self.y = self.y_new


def get_rect(pos):
    x = [p[0] for p in pos]
    y = [p[1] for p in pos]

    xs = list(range(min(x), max(x) + 1))
    ys = list(range(min(y), max(y) + 1))

    arr = np.zeros((len(ys), len(xs)))

    for i in range(len(xs)):
        for j in range(len(ys)):
            if [xs[i], ys[j]] in pos:
                arr[j, i] = 1
    return arr


def display_positions(t, moved, pos):

    arr = get_rect(pos)

    score = (np.shape(arr)[0] * np.shape(arr)[1]) - np.sum(arr)

    print("t =", t, "movers =", moved)
    # print(moved, "moved")
    # print()

    # arr = np.flipud(arr)

    # for i in range(np.shape(arr)[0]):
    #     show = []
    #     for j in range(np.shape(arr)[1]):
    #         if arr[i, j] == 1:
    #             show.append("#")
    #         else:
    #             show.append(" ")
    #     print("".join(show))
    # print()
    print("score =", score)
    print()


def parse(lines):
    elves = []
    for i, line in enumerate(lines):
        line = line.strip()
        chars = [*line]
        for j, char in enumerate(chars):
            if char == "#":
                elves.append(Elf(j, len(lines) - i - 1))
    return elves


def count_movers(proposed):
    cnt = 0
    for i in range(len(proposed)):
        if proposed[i] != [None, None]:
            cnt += 1

    return cnt


with open(
    "/Users/kyle/Documents/Learning/advent-of-code/2022/day_23_unstable_diffusion/input.txt",
    "r",
) as file:
    lines = file.readlines()


elves = parse(lines)

movers = 1
t = 0

while movers > 0:

    current = [e.position() for e in elves]

    proposed = [e.propose_move(current, order_of_movement[t % 4]) for e in elves]

    movers = count_movers(proposed)

    display_positions(t, movers, current)

    for e in elves:
        cnt = 0
        for p in proposed:
            if e.new_position() == p:
                cnt += 1

        if cnt < 2:
            e.make_move()

    t += 1

print(t)
