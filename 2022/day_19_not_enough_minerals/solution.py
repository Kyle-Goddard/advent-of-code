class Blueprint:
    def __init__(self, id, robot_recipes):
        self.id = id
        self.robot_recipes = robot_recipes

    def __repr__(self) -> str:
        show = f"BLUEPRINT {self.id}\n"
        for r in self.robot_recipes:
            show += f"{r} {str(self.robot_recipes[r])}\n"
        return show


with open(
    "/Users/kyle/Documents/Learning/advent-of-code/2022/day_19_not_enough_minerals/input.txt",
    "r",
) as file:
    lines = file.readlines()

lines = [l.strip() for l in lines]


def parse_blueprint(line):

    id = line.split(":")[0].split(" ")[1]
    robots = {}
    for robot_recipe in line.split(":")[1].split("Each ")[1:]:
        robot_name = robot_recipe.split(" ")[0] + "_robot"
        match robot_name:
            case "ore_robot":
                priority = 3
            case "clay_robot":
                priority = 2
            case "obsidian_robot":
                priority = 1
            case "geode_robot":
                priority = 0

        robots[priority] = {}
        requirements = robot_recipe.split("costs ")[1].split("and")
        resources = ["ore", "clay", "obsidian"]
        for res in resources:
            robots[priority][res] = 0
        for req in requirements:
            req = req.strip().split(" ")
            for res in resources:
                if res in req[1]:
                    robots[priority][res] = int(req[0])

    return Blueprint(id, robot_recipes=robots)


blueprints = [parse_blueprint(l) for l in lines]

# print(blueprints)

robots = [1, 0, 0, 0]  # ore, clay, obs, geode
resources = [0, 0, 0, 0]  # ore, clay, obs, geode

for t in range(24):

    # building phase
    new_robots = [0, 0, 0, 0]
    for priority in range(4):
        try_to_build = blueprints[0].robot_recipes[priority]
        if (
            try_to_build["ore"] <= resources[0]
            and try_to_build["clay"] <= resources[1]
            and try_to_build["obsidian"] <= resources[2]
        ):
            new_robots[3 - priority] = robots[3 - priority] + 1
            resources[0] -= blueprints[0].robot_recipes[priority]["ore"]
            resources[1] -= blueprints[0].robot_recipes[priority]["clay"]
            resources[2] -= blueprints[0].robot_recipes[priority]["obsidian"]
        else:
            new_robots[3 - priority] = robots[3 - priority]

    # collection phase
    for r in range(len(resources)):
        resources[r] += robots[r]

    robots = new_robots

print(robots)
print(resources)
