def split_compartments(line):
    rucksack = list(line.strip())
    return [
        set(rucksack[: int(len(rucksack) / 2)]),
        set(rucksack[int(len(rucksack) / 2) :]),
    ]


def find_mistakes(rucksack):
    return list(rucksack[0].intersection(rucksack[1]))[0]


def prioritize(mistake):
    if mistake.isupper():
        return ord(mistake.lower()) - 70
    else:
        return ord(mistake) - 96


with open("input.txt", "r") as f:
    lines = f.readlines()
    rucksacks = []
    for line in lines:
        rucksacks.append(split_compartments(line))

    mistakes = [find_mistakes(r) for r in rucksacks]
    priority = [prioritize(m) for m in mistakes]
    total = sum(priority)

print(total)
