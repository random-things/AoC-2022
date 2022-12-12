import dataclasses
import math
from typing import List, ForwardRef, Dict, Tuple, Set


@dataclasses.dataclass(frozen=True)
class Location:
    x: int
    y: int
    z: int

    def __eq__(self, other):
        return self.x == other.x and self.y == other.y


@dataclasses.dataclass
class AStarNode:
    location: Location
    g: int
    h: int
    f: int
    parent: ForwardRef("AStarNode")


@dataclasses.dataclass
class Map:
    locations: List[Location] = dataclasses.field(default_factory=list)
    locations_dict: Dict[Tuple[int, int], Location] = dataclasses.field(default_factory=dict)
    my_location: Location = None
    end_location: Location = None

    @staticmethod
    def from_lines(map_lines: List[str]):
        new_map = Map()
        for y, line in enumerate(map_lines):
            for x, char in enumerate(line):

                if char == 'S':
                    new_map.my_location = Location(x, y, 0)
                elif char == 'E':
                    new_map.end_location = Location(x, y, ord('z') - ord('a'))
                else:
                    new_map.locations.append(Location(x, y, ord(char) - ord('a')))

                if char == 'E':
                    char = 'z'
                new_map.locations_dict[(x, y)] = Location(x, y, ord(char) - ord('a'))

        return new_map

    def find_possible_moves(self, current_location: Location) -> List[Location]:
        possible_moves = []
        allowed_moves = ((-1, 0), (1, 0), (0, -1), (0, 1))
        for move in allowed_moves:
            location = self.locations_dict.get((current_location.x + move[0], current_location.y + move[1]))
            if location is None:
                continue
            if location.x == current_location.x and location.y == current_location.y:
                continue
            if location.z <= current_location.z + 1:
                possible_moves.append(location)
        return possible_moves

    def find_shortest_path_astar(self, current_location: Location, end_location: Location):
        open_list: List[AStarNode] = []
        closed_list: Set[Location] = set()

        start_node = AStarNode(current_location, 0, 0, 0, None)
        end_node = AStarNode(end_location, 0, 0, 0, None)

        open_list.append(start_node)

        while len(open_list) > 0:
            current_node = open_list.pop(0)
            if current_node.location in closed_list:
                continue
            closed_list.add(current_node.location)

            if current_node.location == end_node.location:
                path = []
                current = current_node
                while current is not None:
                    path.append(current.location)
                    current = current.parent
                return path[::-1]

            possible_moves = self.find_possible_moves(current_node.location)
            possible_nodes = [AStarNode(move, 0, 0, 0, current_node) for move in possible_moves]

            for node in possible_nodes:
                if node.location in closed_list:
                    continue

                node.g = current_node.g + 1
                node.h = math.sqrt((node.location.x - end_node.location.x) ** 2 + (node.location.y - end_node.location.y) ** 2)
                node.f = node.g + node.h

                for open_node in open_list:
                    if node.location == open_node.location and node.g >= open_node.g:
                        continue

                open_list.append(node)

    def print_map(self):
        for location in self.locations:
            print(location)


with open("input.txt") as file:
    lines = [s.strip() for s in file.readlines()]

    m = Map.from_lines(lines)

    # Part 1
    path = m.find_shortest_path_astar(m.my_location, m.end_location)
    print(path)
    print(len(path) - 1)

    # Part 2
    path_length: List[int] = []
    for location in m.locations:
        if location.z == 0:
            path = m.find_shortest_path_astar(location, m.end_location)
            if path is not None:
                path_length.append(len(path) - 1)

    print(min(path_length))
