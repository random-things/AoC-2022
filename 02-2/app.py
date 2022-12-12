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
    "X": Result.LOSS,
    "Y": Result.DRAW,
    "Z": Result.WIN
}


def rock_paper_scissors_with_desired_result(their_action: ActionValues, desired_result: Result):
    if desired_result == Result.WIN:
        return ActionValues(int(their_action.value) % 3 + 1)
    elif desired_result == Result.DRAW:
        return their_action
    else:
        return ActionValues((int(their_action.value) - 2) % 3 + 1)


with open("input.txt", "r") as file:
    contents = file.read()

    total_score: int = 0
    for line in contents.split("\n"):
        their_action, desired_result = list(map(ACTIONS.get, line.split(' ')))
        total_score += rock_paper_scissors_with_desired_result(their_action, desired_result).value + desired_result.value

    print(f"Score after all games: {total_score}")

