def parse_input(lines):
    stacks = []
    instructions = []

    sorting_stacks = True
    for line in lines:
        if sorting_stacks:
            if len(line.strip()) > 0:
                stacks.append(line.strip("\n"))
            else:
                sorting_stacks = False
                continue

        if not sorting_stacks:
            instructions.append(line.strip("\n").split(" "))

    return stacks, instructions


def stack_data_to_dict(stacks):
    stack_dict = {}

    stack_id = stacks[-1]
    stack_containers = stacks[:-1][::-1]

    for i in range(len(stack_id)):
        if stack_id[i].strip():
            stack_dict[stack_id[i]] = []

            for container in stack_containers:
                if container[i].strip():
                    stack_dict[stack_id[i]].append(container[i])

    return stack_dict


def execute_instructions(stacks, instructions):
    for instruction in instructions:
        loading_cycle = int(instruction[1])
        from_stack = instruction[3]
        to_stack = instruction[5]

        while loading_cycle > 0:
            stacks[to_stack].append(stacks[from_stack].pop(-1))
            loading_cycle -= 1

    return stacks


def execute_instructions_part_2(stacks, instructions):
    for instruction in instructions:
        pile = int(instruction[1])
        from_stack = instruction[3]
        to_stack = instruction[5]

        stacks[to_stack].extend(stacks[from_stack][-1 * pile :])
        del stacks[from_stack][-1 * pile :]

    return stacks


with open("puzzle_input.txt", "r") as f:
    lines = f.readlines()
    stacks, instructions = parse_input(lines)

    stacks = stack_data_to_dict(stacks)

    stacks = execute_instructions_part_2(stacks, instructions)

answer = [stacks[str(id + 1)][-1] for id in range(len(stacks))]
print("".join(answer))
