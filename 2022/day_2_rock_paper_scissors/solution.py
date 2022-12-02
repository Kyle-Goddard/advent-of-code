WIN = "win"
DRAW = "draw"
LOSE = "lose"

ROCK = "rock"
PAPER = "paper"
SCISSORS = "scissors"


def get_shape_from_symbol(symbol):
    if symbol == "A" or symbol == "X":
        return ROCK
    elif symbol == "B" or symbol == "Y":
        return PAPER
    elif symbol == "C" or symbol == "Z":
        return SCISSORS
    else:
        return "error"


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


def game_outcome(my_shape, their_shape):
    outcome = LOSE

    if my_shape == their_shape:
        outcome = DRAW

    if my_shape == ROCK and their_shape == SCISSORS:
        outcome = WIN

    if my_shape == PAPER and their_shape == ROCK:
        outcome = WIN

    if my_shape == SCISSORS and their_shape == PAPER:
        outcome = WIN

    return outcome


def total_score(games):
    total_score = 0

    for game in games:
        their_shape = get_shape_from_symbol(game[0])
        my_shape = get_shape_from_symbol(game[1])

        outcome = game_outcome(my_shape, their_shape)

        total_score += game_score(my_shape, outcome)
    return total_score


with open("input.txt", "r") as f:
    lines = f.readlines()
    games = []
    for line in lines:
        games.append(line.split())

print(total_score(games))
