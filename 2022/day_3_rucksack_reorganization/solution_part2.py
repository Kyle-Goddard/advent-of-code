def split_compartments(line):
    rucksack = list(line.strip())
    return set(rucksack)


def find_common_items(rucksacks):
    common_items = []
    for i in range(int(len(rucksacks) / 3)):
        common1 = rucksacks[3 * i].intersection(rucksacks[3 * i + 1])
        common2 = rucksacks[3 * i].intersection(rucksacks[3 * i + 2])

        common_items.append(list(common1.intersection(common2))[0])

    return common_items


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

    common_items = find_common_items(rucksacks)
    priority = [prioritize(c) for c in common_items]
    total = sum(priority)

print(total)
