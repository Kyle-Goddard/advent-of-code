WIN = "win"
DRAW = "draw"
LOSE = "lose"

ROCK = "rock"
PAPER = "paper"
SCISSORS = "scissors"


def get_shape_from_symbol(symbol):
    if symbol == "A":
        return ROCK
    elif symbol == "B":
        return PAPER
    elif symbol == "C":
        return SCISSORS
    else:
        return "error"


def get_outcome_from_symbol(symbol):
    if symbol == "X":
        return LOSE
    elif symbol == "Y":
        return DRAW
    elif symbol == "Z":
        return WIN
    else:
        return "error"


def get_shape_from_outcome(their_shape, outcome):

    if outcome == DRAW:
        return their_shape

    shapes = [ROCK, SCISSORS, PAPER]

    if outcome == WIN:
        idx = shapes.index(their_shape)
        return shapes[idx - 1]

    if outcome == LOSE:
        idx = shapes.index(their_shape)
        return shapes[(idx + 1) % 3]


def game_score(my_shape, outcome):
    score = 0

    if my_shape == ROCK:
        score += 1
    if my_shape == PAPER:
        score += 2
    if my_shape == SCISSORS:
        score += 3

    if outcome == DRAW:
        score += 3
    if outcome == WIN:
        score += 6

    return score


def total_score(games):
    total_score = 0

    for game in games:
        their_shape = get_shape_from_symbol(game[0])
        outcome = get_outcome_from_symbol(game[1])
        my_shape = get_shape_from_outcome(their_shape, outcome)

        total_score += game_score(my_shape, outcome)
    return total_score


with open("input.txt", "r") as f:
    lines = f.readlines()
    games = []
    for line in lines:
        games.append(line.split())

print(total_score(games))
