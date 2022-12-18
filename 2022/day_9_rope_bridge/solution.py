with open(
    "/Users/kyle/Documents/Learning/advent-of-code/2022/day_9_rope_bridge/puzzle_input.txt",
    "r",
) as file:
    lines = file.readlines()

lines = [l.strip() for l in lines]


def parse_instructions(lines):
    instructions = []
    for l in lines:
        instruction = l.split(" ")
        instructions.append([instruction[0], int(instruction[1])])
    return instructions


def move_head(head_position, direction):
    match direction:
        case "R":
            return [head_position[0] + 1, head_position[1]]
        case "L":
            return [head_position[0] - 1, head_position[1]]
        case "U":
            return [head_position[0], head_position[1] + 1]
        case "D":
            return [head_position[0], head_position[1] - 1]

    return head_position


def tail_is_far(head_position, tail_position):
    return (
        abs(head_position[0] - tail_position[0]) > 1
        or abs(head_position[1] - tail_position[1]) > 1
    )


def move_tail(head_position, tail_position):
    possible_moves = [
        [1, 0],
        [-1, 0],
        [0, 1],
        [0, -1],
        [1, 1],
        [-1, 1],
        [-1, -1],
        [1, -1],
    ]
    distance_after_move = []
    for p in possible_moves:
        new_position = [tail_position[0] + p[0], tail_position[1] + p[1]]
        distance_after_move.append(
            abs(new_position[0] - head_position[0])
            + abs(new_position[1] - head_position[1])
        )

    idx = distance_after_move.index(min(distance_after_move))

    return [
        tail_position[0] + possible_moves[idx][0],
        tail_position[1] + possible_moves[idx][1],
    ]


instructions = parse_instructions(lines)

knots = {
    0: [0, 0],
    1: [0, 0],
    2: [0, 0],
    3: [0, 0],
    4: [0, 0],
    5: [0, 0],
    6: [0, 0],
    7: [0, 0],
    8: [0, 0],
    9: [0, 0],
}

end_knot = 9

unique_tail_coords = []

for i in range(len(instructions)):
    direction = instructions[i][0]
    steps = instructions[i][1]

    while steps > 0:
        knots[0] = move_head(knots[0], direction)
        for k in range(len(knots) - 1):
            if tail_is_far(knots[k], knots[k + 1]):
                knots[k + 1] = move_tail(knots[k], knots[k + 1])

        if knots[end_knot] not in unique_tail_coords:
            unique_tail_coords.append(knots[end_knot])
        steps -= 1

print(len(unique_tail_coords))
