import dataclasses
from enum import Enum
from typing import List, Dict


SOURCE_X: int = 500
SOURCE_Y: int = 0


class CaveLocationType(Enum):
    AIR = "."
    ROCK = "#"
    SAND = "o"
    FALLING_SAND = "~"
    SAND_SOURCE = "+"


@dataclasses.dataclass(frozen=True)
class CaveLocation:
    x: int
    y: int


class Cave:
    def __init__(self):
        self.cave_locations: Dict[CaveLocation, CaveLocationType] = {CaveLocation(SOURCE_X, SOURCE_Y): CaveLocationType.SAND_SOURCE}
        self.min_x: int = SOURCE_X
        self.max_x: int = SOURCE_X
        self.min_y: int = SOURCE_Y
        self.max_y: int = SOURCE_Y

    def add_rock_face(self, rock_string: str):
        coordinates: List[str] = rock_string.split(" -> ")
        for i in range(0, len(coordinates) - 1):
            x, y = list(map(int, coordinates[i].split(",")))
            a, b = list(map(int, coordinates[i + 1].split(",")))

            self.min_x = min(self.min_x, x, a)
            self.max_x = max(self.max_x, x, a)
            self.max_y = max(self.max_y, y, b)

            if x == a:
                for j in range(min(y, b), max(y, b) + 1):
                    self.cave_locations[CaveLocation(x, j)] = CaveLocationType.ROCK
            elif y == b:
                for j in range(min(x, a), max(x, a) + 1):
                    self.cave_locations[CaveLocation(j, y)] = CaveLocationType.ROCK

    def count_sand(self):
        return sum(1 for location in self.cave_locations.values() if location == CaveLocationType.SAND)

    def drop_sand(self, use_floor: bool = False):
        x: int = SOURCE_X
        y: int = SOURCE_Y

        if use_floor:
            if self.cave_locations.get(CaveLocation(x, y), CaveLocationType.AIR) == CaveLocationType.SAND:
                return False
        self.cave_locations[CaveLocation(x, y)] = CaveLocationType.FALLING_SAND

        while True:
            new_x: int = x
            new_y: int = y + 1

            if not use_floor:
                if new_y > self.max_y:
                    return False

            if use_floor and new_y == self.max_y + 2:
                self.cave_locations[CaveLocation(x, y)] = CaveLocationType.SAND
                break
            if self.cave_locations.get(CaveLocation(x, new_y), CaveLocationType.AIR) == CaveLocationType.AIR:
                pass
            elif self.cave_locations.get(CaveLocation(x - 1, new_y), CaveLocationType.AIR) == CaveLocationType.AIR:
                new_x = x - 1
            elif self.cave_locations.get(CaveLocation(x + 1, new_y), CaveLocationType.AIR) == CaveLocationType.AIR:
                new_x = x + 1
            else:
                self.cave_locations[CaveLocation(x, y)] = CaveLocationType.SAND
                break

            if x == SOURCE_X and y == SOURCE_Y:
                self.cave_locations[CaveLocation(x, y)] = CaveLocationType.SAND_SOURCE
            else:
                self.cave_locations[CaveLocation(x, y)] = CaveLocationType.AIR

            self.cave_locations[CaveLocation(new_x, new_y)] = CaveLocationType.FALLING_SAND
            x = new_x
            y = new_y

            self.max_x = max(self.max_x, x)
            self.min_x = min(self.min_x, x)

        return True

    def print(self, use_floor: bool = False):
        if use_floor:
            upper_y: int = self.max_y + 2
        else:
            upper_y: int = self.max_y

        for y in range(self.min_y, upper_y):
            for x in range(self.min_x, self.max_x + 1):
                print(self.cave_locations.get(CaveLocation(x, y), CaveLocationType.AIR).value, end="")
            print()
        if use_floor:
            print(CaveLocationType.ROCK.value * (self.max_x - self.min_x + 1))
        print()


with open("input.txt") as file:
    lines: List[str] = list(map(str.strip, file.readlines()))

    # Part 1
    cave = Cave()

    for line in lines:
        cave.add_rock_face(line)

    while cave.drop_sand():
        # cave.print()
        pass

    print(cave.count_sand())

    # Part 2
    cave = Cave()

    for line in lines:
        cave.add_rock_face(line)

    while cave.drop_sand(use_floor=True):
        # cave.print(use_floor=True)
        pass

    print(cave.count_sand())
