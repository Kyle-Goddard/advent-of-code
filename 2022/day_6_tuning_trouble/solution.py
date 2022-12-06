def get_start_marker(message):
    buffer_size = 14
    buffer = list(message[:buffer_size])
    idx = buffer_size

    for char in message[buffer_size:]:
        if len(set(buffer)) < len(buffer):
            buffer.pop(0)
            buffer.append(char)
            idx += 1

    return idx


with open("puzzle_input.txt", "r") as file:
    lines = file.readlines()

lines = [line.strip() for line in lines]

for line in lines:
    marker = get_start_marker(message=line)
    print(marker)
