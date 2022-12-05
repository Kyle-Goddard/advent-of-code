def split_sections(line):
    elf_pair = line.strip()
    assignments = []
    for elf in elf_pair.split(","):
        bnds = elf.split("-")
        elf_sections = set(range(int(bnds[0]), int(bnds[1]) + 1))
        assignments.append(elf_sections)

    return assignments


def find_common_sections(section_assignment_pair):
    return section_assignment_pair[0].intersection(section_assignment_pair[1])


def check_overlap(section_assignment_pair):
    common = find_common_sections(section_assignment_pair)

    if common == section_assignment_pair[0] or common == section_assignment_pair[1]:
        return 1

    return 0


def check_overlap_part2(section_assignment_pair):
    common = find_common_sections(section_assignment_pair)

    if len(common) > 0:
        return 1

    return 0


with open("input.txt", "r") as f:
    lines = f.readlines()
    section_assignments = []
    for line in lines:
        section_assignments.append(split_sections(line))

    overlap = [check_overlap(pair) for pair in section_assignments]
    overlap_part2 = [check_overlap_part2(pair) for pair in section_assignments]

print(sum(overlap))
print(sum(overlap_part2))
