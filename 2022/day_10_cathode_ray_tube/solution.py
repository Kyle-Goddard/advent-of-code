with open(
    "/Users/kyle/Documents/Learning/advent-of-code/2022/day_10_cathode_ray_tube/puzzle_input.txt",
    "r",
) as file:
    lines = file.readlines()

lines = [l.strip().split(" ") for l in lines]

register = [1]

for l in lines:
    if l[0] == "noop":
        register.append(register[-1])

    if l[0] == "addx":
        register.append(register[-1])
        register.append(register[-1] + int(l[1]))


def during_cycle(id, register):
    return register[id - 1]


def after_cycle(id, register):
    return register[id]


cycles = [20, 60, 100, 140, 180, 220]
sum_of_cycles = 0

for c in cycles:
    sum_of_cycles += c * during_cycle(c, register)

print(sum_of_cycles)
