import numpy as np


class Sensor:
    def __init__(self, position=None, nearest_beacon_position=None):
        self.position = position
        self.beacon_position = nearest_beacon_position

    def __repr__(self) -> str:
        return f"SENSOR: {self.position[0]}, {self.position[1]}, with range {self.get_manhattan()}"

    def max_range(self):
        return abs(self.position[0] - self.beacon_position[0]) + abs(
            self.position[1] - self.beacon_position[1]
        )

    def get_manhattan(self, pos):
        return abs(self.position[0] - pos[0]) + abs(self.position[1] - pos[1])

    def x_coord(self):
        return self.position[0]

    def y_coord(self):
        return self.position[1]


def get_bnds(sensors):
    xs = []
    ys = []
    for sensor in sensors:
        xs.append(sensor.x_coord())
        ys.append(sensor.y_coord())

    x_ave = int(sum(xs) / len(xs))
    y_ave = int(sum(ys) / len(ys))

    x_range, y_range = [x_ave, x_ave], [y_ave, y_ave]

    for sensor in sensors:
        min_x = sensor.x_coord() - sensor.max_range()
        max_x = sensor.x_coord() + sensor.max_range()
        min_y = sensor.y_coord() - sensor.max_range()
        max_y = sensor.y_coord() + sensor.max_range()

        if min_x < x_range[0]:
            x_range[0] = min_x
        if max_x > x_range[1]:
            x_range[1] = max_x
        if min_y < y_range[0]:
            y_range[0] = min_y
        if max_y > y_range[1]:
            y_range[1] = max_y

    return list(range(x_range[0], x_range[1] + 1)), list(
        range(y_range[0], y_range[1] + 1)
    )


def parse_positions(line):
    line = line.strip()
    line = line.split(":")

    sensor_line = line[0].strip()
    sensor_x = sensor_line.split(",")[0].split("x=")[-1]
    sensor_y = sensor_line.split(",")[1].split("y=")[-1]

    beacon_line = line[1].strip()
    beacon_x = beacon_line.split(",")[0].split("x=")[-1]
    beacon_y = beacon_line.split(",")[1].split("y=")[-1]

    return Sensor([int(sensor_x), int(sensor_y)], [int(beacon_x), int(beacon_y)])


with open("puzzle_input.txt", "r") as file:
    lines = file.readlines()

sensors = [parse_positions(line.strip()) for line in lines]

x_bnds, y_bnds = get_bnds(sensors)


def get_sign(x, y, sensor):

    if sensor.get_manhattan(pos=[x, y]) == 0:
        return "S"
    if sensor.get_manhattan(pos=[x, y]) <= sensor.max_range():
        return "#"

    return " "


def get_coverage_for_line(y_pt):
    coverage = [0] * len(x_bnds)
    for i in range(len(x_bnds)):
        x_pt = x_bnds[i]
        for sensor in sensors:
            if sensor.get_manhattan(pos=[x_pt, y_pt]) <= sensor.max_range():
                coverage[i] = 1
                break

    for i in range(len(x_bnds)):
        x_pt = x_bnds[i]
        for sensor in sensors:
            if sensor.beacon_position[0] == x_pt and sensor.beacon_position[1] == y_pt:
                coverage[i] = 0
                break
    return coverage


coverage = get_coverage_for_line(10)
ans = sum(coverage)

print(ans)
