from collections import namedtuple
from enum import Enum
from typing import Tuple


class Direction(Enum):
    UP = "U"
    DOWN = "D"
    LEFT = "L"
    RIGHT = "R"


Position = namedtuple("Position", ["x", "y"])

def distance_from_head_to_tail(head_position: Position, tail_position: Position) -> Tuple[int, int, int]:
    dx = head_position.x - tail_position.x
    dy = head_position.y - tail_position.y
    return dx, dy, abs(dx) + abs(dy)


with open("input.txt") as file:
    lines = file.readlines()

    head: Position = Position(0, 0)
    tail: Position = Position(0, 0)
    tail_positions: set[Position] = set(Position(0, 0))

    for line in lines:
        direction, distance_str = line.strip().split(' ')
        distance: int = int(distance_str)

        # Move the head.
        for _ in range(int(distance)):
            if direction == Direction.UP.value:
                head = Position(head.x, head.y + 1)
            elif direction == Direction.DOWN.value:
                head = Position(head.x, head.y - 1)
            elif direction == Direction.LEFT.value:
                head = Position(head.x - 1, head.y)
            elif direction == Direction.RIGHT.value:
                head = Position(head.x + 1, head.y)

            # Move the tail.
            dx, dy, total_d = distance_from_head_to_tail(head, tail)
            if total_d == 0 or total_d == 1 or (abs(dx) == 1 and abs(dy) == 1):
                continue
            elif total_d == 3:
                if direction == Direction.UP.value:
                    tail = Position(head.x, head.y - 1)
                elif direction == Direction.DOWN.value:
                    tail = Position(head.x, head.y + 1)
                elif direction == Direction.LEFT.value:
                    tail = Position(head.x + 1, head.y)
                elif direction == Direction.RIGHT.value:
                    tail = Position(head.x - 1, head.y)
            else:
                if direction == Direction.UP.value:
                    tail = Position(tail.x, tail.y + 1)
                elif direction == Direction.DOWN.value:
                    tail = Position(tail.x, tail.y - 1)
                elif direction == Direction.LEFT.value:
                    tail = Position(tail.x - 1, tail.y)
                elif direction == Direction.RIGHT.value:
                    tail = Position(tail.x + 1, tail.y)

            print(f"head: {head}, tail: {tail}")

            tail_positions.add(tail)

    for pos in tail_positions:
        print(f"tail: {pos}")
    print(len(tail_positions))
