from collections import namedtuple
from enum import Enum
from typing import Tuple, ForwardRef


class Direction(Enum):
    UP = "U"
    DOWN = "D"
    LEFT = "L"
    RIGHT = "R"


Position = namedtuple("Position", ["x", "y"])


class Knot:
    id: int
    position: Position
    leader: ForwardRef("Knot")
    follower: ForwardRef("Knot")
    history: set[Position]

    def __init__(self, id: int, position: Position):
        self.id = id
        self.position = position
        self.leader = None
        self.follower = None
        self.history = set()
        self.history.add(Position(0, 0))

    def move(self, direction: Direction):
        if direction == Direction.UP:
            self.position = Position(self.position.x, self.position.y + 1)
        elif direction == Direction.DOWN:
            self.position = Position(self.position.x, self.position.y - 1)
        elif direction == Direction.LEFT:
            self.position = Position(self.position.x - 1, self.position.y)
        elif direction == Direction.RIGHT:
            self.position = Position(self.position.x + 1, self.position.y)

        self.move_follower()

    def move_to(self, position: Position):
        self.position = position
        self.history.add(position)

        self.move_follower()

    def move_follower(self):
        if self.follower is not None:
            dx = self.position.x - self.follower.position.x
            dy = self.position.y - self.follower.position.y
            total_distance = abs(dx) + abs(dy)

            if total_distance > 1 and not (abs(dx) == 1 and abs(dy) == 1):
                if abs(dx) > 1:
                    new_x = self.position.x - round(dx / abs(dx))
                else:
                    new_x = self.position.x
                if abs(dy) > 1:
                    new_y = self.position.y - round(dy / abs(dy))
                else:
                    new_y = self.position.y

                self.follower.move_to(Position(new_x, new_y))


with open("input.txt") as file:
    lines = file.readlines()

    NUM_KNOTS: int = 10
    knots: dict[int, Knot] = {}
    for i in range(NUM_KNOTS):
        knot: Knot = Knot(i, Position(0, 0))
        knots[i] = knot
        if i > 0:
            previous_knot: Knot = knots[i - 1]
            knot.leader = previous_knot
            previous_knot.follower = knot

    for line in lines:
        direction, distance_str = line.strip().split(' ')
        distance: int = int(distance_str)

        for _ in range(distance):
            knots[0].move(Direction(direction))

    print(len(knots[9].history))
