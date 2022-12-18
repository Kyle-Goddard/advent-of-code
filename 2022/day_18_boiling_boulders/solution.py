import matplotlib.pyplot as plt

with open(
    "/Users/kyle/Documents/Learning/advent-of-code/2022/day_18_boiling_boulders/input.txt",
    "r",
) as file:
    lines = file.readlines()

voxel_coords = [l.strip().split(",") for l in lines]


class Face:
    def __init__(self, points):
        self.points = points

    def __eq__(self, other):
        return self.points == other.points

    def __repr__(self):
        str_to_hash = ""

        cnt = 1
        for p in self.points:
            str_to_hash += f"x{cnt}:{p[0]};"
            str_to_hash += f"y{cnt}:{p[1]};"
            str_to_hash += f"z{cnt}:{p[2]};"
            cnt += 1

        return str_to_hash

    def __hash__(self) -> int:
        return hash(self.__repr__())

    def point_coords(self):
        return self.points


def get_face_coords(x, y, z):
    x = int(x)
    y = int(y)
    z = int(z)

    points = {
        1: [x - 1, y - 1, z - 1],
        2: [x, y - 1, z - 1],
        3: [x, y, z - 1],
        4: [x - 1, y, z - 1],
        5: [x - 1, y - 1, z],
        6: [x, y - 1, z],
        7: [x, y, z],
        8: [x - 1, y, z],
    }

    faces = {
        1: Face([points[1], points[2], points[3], points[4]]),
        2: Face([points[5], points[6], points[7], points[8]]),
        3: Face([points[6], points[2], points[3], points[7]]),
        4: Face([points[5], points[1], points[4], points[8]]),
        5: Face([points[1], points[2], points[6], points[5]]),
        6: Face([points[4], points[3], points[7], points[8]]),
    }

    return faces


blocks = [get_face_coords(v[0], v[1], v[2]) for v in voxel_coords]

cnt = 0
shape = []
points = []
xs = []
while len(blocks) > 0:
    block = blocks[0]

    for bface in block:
        block_face = block[bface]
        shape.append(block_face)
        for p in block_face.point_coords():
            if p not in points:
                points.append(p)
            if p[0] not in xs:
                xs.append(p[0])

    blocks.pop(0)

surface = dict.fromkeys(shape)

for sface in surface:
    surface[sface] = 0

for face in shape:
    surface[face] += 1

common_faces = []
for sface in surface:
    if surface[sface] > 1:
        common_faces.append(sface)

for c in common_faces:
    del surface[c]

print(len(surface))

# points = []
# xs = []
# for face in surface:
#     for p in face.point_coords():
#         if p not in points:
#             points.append(p)
#         if p[0] not in xs:
#             xs.append(p[0])

print(points)
print(len(points))

xs.sort()
print(xs)

for level in xs:
    ys = [p[1] for p in points if p[0] == level]
    zs = [p[2] for p in points if p[0] == level]

    print(ys, zs)

    plt.figure()
    plt.scatter(ys, zs)
    plt.show()
