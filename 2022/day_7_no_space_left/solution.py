class File:
    def __init__(self, name, size):
        self.name = name
        self.size = size

    def __repr__(self):
        return f" -- {self.name} (file size = {self.size})\n"


class Tree:
    def __init__(self, name=None, parent=None):
        self.name = name
        self.parent = parent
        self.dirs = []
        self.files = []
        self.size = 0

    def __repr__(self):
        show = f" - {self.name} (dir) size = {self.size}\n"
        for file in self.files:
            show += str(file)
        for dir in self.dirs:
            show += str(dir)

        return show

    def navigate_to(self, path):
        if path == self.name:
            return self

        if path == "..":
            return self.parent

        for dir in self.dirs:
            if path == dir.name:
                return dir

        if path == "/":
            current_directory = self
            while current_directory.name != path:
                current_directory = current_directory.parent
            return current_directory

    def make_dir(self, name):
        existing_dirs = [d.name for d in self.dirs]
        if name not in existing_dirs:
            self.dirs.append(Tree(name, parent=self))

    def make_file(self, name, size):
        existing_files = [f.name for f in self.files]
        if name not in existing_files:
            self.files.append(File(name, size))

            current_directory = self
            while current_directory != None:
                current_directory.size += size
                current_directory = current_directory.navigate_to("..")


with open(
    "/Users/kyle/Documents/Learning/advent-of-code/2022/day_7_no_space_left/puzzle_input.txt",
    "r",
) as file:
    lines = file.readlines()

lines = [l.strip().split(" ") for l in lines]

current_directory = Tree(name="/")

cnt = 0
while cnt < len(lines):
    terminal = lines[cnt]

    if terminal[0] == "$":
        cmd = terminal[1]
        if cmd == "cd":
            path = terminal[2]
            current_directory = current_directory.navigate_to(path)
            cnt += 1
        if cmd == "ls":
            cnt += 1
    else:
        if terminal[0] == "dir":
            current_directory.make_dir(terminal[1])
        else:
            current_directory.make_file(terminal[1], int(terminal[0]))
        cnt += 1

root_directory = current_directory.navigate_to("/")


def dfs(root, visited=None):
    if visited == None:
        visited = set()

    visited.add(root)

    for next in set(root.dirs) - visited:
        dfs(next, visited)

    return visited


visited = list(dfs(root_directory))

total_disk_available = 70000000
required_disk_for_update = 30000000

total_disk_used = root_directory.size
total_disk_unused = total_disk_available - total_disk_used

min_to_be_deleted = required_disk_for_update - total_disk_unused

sizes = [v.size for v in visited if v.size >= min_to_be_deleted]

print(min(sizes))
