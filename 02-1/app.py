from enum import Enum


class Result(Enum):
    WIN = 6
    DRAW = 3
    LOSS = 0


class ActionValues(Enum):
    ROCK = 1
    PAPER = 2
    SCISSORS = 3


ACTIONS = {
    "A": ActionValues.ROCK,
    "B": ActionValues.PAPER,
    "C": ActionValues.SCISSORS,
    "X": ActionValues.ROCK,
    "Y": ActionValues.PAPER,
    "Z": ActionValues.SCISSORS
}


def rock_paper_scissors(their_action: ActionValues, my_action: ActionValues):
    if my_action == their_action:
        return Result.DRAW
    elif their_action.value == (int(my_action.value) % 3) + 1:
        return Result.LOSS
    else:
        return Result.WIN


with open("input.txt", "r") as file:
    contents = file.read()

    total_score: int = 0
    for line in contents.split("\n"):
        their_action, my_action = list(map(ACTIONS.get, line.split(' ')))
        total_score += rock_paper_scissors(their_action, my_action).value + my_action.value

    print(f"Score after all games: {total_score}")

