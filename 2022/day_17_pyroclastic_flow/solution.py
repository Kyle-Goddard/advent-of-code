class Tower:
    def __init__(self):
        self.tower = []
        self.shape_id = None
        self.shape_location = None

    def __repr__(self):
        show = ""
        for row in self.tower[::-1]:
            show += " ".join([str(r) for r in row]) + "\n"
        return show

    def new_shape(self, shape_id):
        self.tower.extend([[0] * 7] * 3)
        self.tower.extend(shapes[shape_id][::-1])
        self.shape_location = [2, len(self.tower) - len(shapes[shape_id])]
        self.shape_id = shape_id

    def shape_can_fall(self):
        if self.shape_location[1] <= 0:
            return False

        shape_space = self.tower[
            self.shape_location[1]
            - 1 : self.shape_location[1]
            + len(shapes[self.shape_id])
        ]

        for i in range(7):
            column = [s[i] for s in shape_space]
            for j in range(len(column) - 1):
                if column[j] == 2 and column[j + 1] == 1:
                    return False

        return True

    def shape_must_fall(self):

        for i in range(
            self.shape_location[1] - 1,
            self.shape_location[1] + len(shapes[self.shape_id]),
        ):
            for j in range(7):
                if tower.tower[i - 1][j] == 0 and tower.tower[i][j] == 1:
                    tower.tower[i - 1][j] = 1
                    tower.tower[i][j] = 0


# with open(
#     "/Users/kyle/Documents/Learning/advent-of-code/2022/day_16_proboscidea_volcanium/input.txt",
#     "r",
# ) as file:
#     lines = file.readlines()

# jets = [l.strip() for l in lines]

shapes = {
    0: [[0, 0, 1, 1, 1, 1, 0]],
    1: [[0, 0, 0, 1, 0, 0, 0], [0, 0, 1, 1, 1, 0, 0], [0, 0, 0, 1, 0, 0, 0]],
    2: [[0, 0, 0, 0, 1, 0, 0], [0, 0, 0, 0, 1, 0, 0], [0, 0, 1, 1, 1, 0, 0]],
    3: [
        [0, 0, 1, 0, 0, 0, 0],
        [0, 0, 1, 0, 0, 0, 0],
        [0, 0, 1, 0, 0, 0, 0],
        [0, 0, 1, 0, 0, 0, 0],
    ],
    4: [[0, 1, 1, 0, 0, 0, 0], [0, 1, 1, 0, 0, 0, 0]],
}

cycles = 0

tower = Tower()

while cycles < 1:
    tower.new_shape(shape_id=cycles % len(shapes))

    print(tower)

    print()

    if tower.shape_can_fall():
        tower.shape_must_fall()

    # while shape can fall:
    # --- move rock using jet
    # --- move rock down
    # set shape in place

    cycles += 1

print(tower)
