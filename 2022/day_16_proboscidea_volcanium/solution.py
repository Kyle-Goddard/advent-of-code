from copy import deepcopy


class Valve:
    def __init__(self, name, rate, connects):
        self.name = name
        self.rate = int(rate)
        self.connects = connects
        self.is_open = False

    def __repr__(self) -> str:
        return f"{self.name}"

    def open_valve(self):
        self.is_open = True


class State:
    def __init__(self, valves, time=30, score=0):
        self.valves = deepcopy(valves)
        self.time = time
        self.score = score
        self.path = []

    def __repr__(self) -> str:
        return str(self.score)

    def get_valves(self):
        return self.valves

    def update_score(self, val):
        self.score += val

    def update_path(self, val):
        self.path.append(val)


def stay_and_open_valve(valve_name, state):
    new_state = State(
        valves=state.get_valves(),
        time=state.time - 1,
        score=state.score,
    )

    new_state.valves[valve_name].open_valve()
    pressure_release = new_state.valves[valve_name].rate
    new_state.update_score(new_state.time * pressure_release)
    new_state.update_path(f"open {valve_name}")

    return new_state


def move_to_next_valve(valve_name, state):
    new_state = State(
        valves=state.get_valves(),
        time=state.time - 1,
        score=state.score,
    )
    new_state.update_path(f"move to {valve_name}")

    return new_state


def parse_valves(line):
    valve_line = line.split(";")[0].strip()
    tunnel_line = line.split(";")[1].strip()

    valve_name = valve_line.split(" ")[1].strip()
    valve_rate = valve_line.split("rate=")[-1].strip()

    tunnels = [t.strip(",") for t in tunnel_line.split(" ")[4:]]

    return Valve(valve_name, valve_rate, tunnels)


with open(
    "/Users/kyle/Documents/Learning/advent-of-code/2022/day_16_proboscidea_volcanium/input.txt",
    "r",
) as file:
    lines = file.readlines()

valves = [parse_valves(line.strip()) for line in lines]
valves = {v.name: v for v in valves}

start = "AA"
