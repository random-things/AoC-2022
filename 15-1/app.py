import dataclasses
import re

from typing import Dict, List, Set, Tuple


SEARCH_SPACE_X: int = 4000000
SEARCH_SPACE_Y: int = 4000000


@dataclasses.dataclass(frozen=True)
class Location:
    x: int
    y: int


def manhattan_distance(loc1: Location, loc2: Location) -> int:
    return abs(loc1.x - loc2.x) + abs(loc1.y - loc2.y)


def range_affected_by_sensor_in_row(sensor: Location, sensor_range: int, row: int, restrict_range: bool = False) -> Tuple[int, int]:
    dist_y: int = abs(row - sensor.y)
    if dist_y > sensor_range:
        return 0, 0

    positions_affected = sensor_range - dist_y
    if restrict_range:
        start_x = max(sensor.x - positions_affected, 0)
        end_x = min(sensor.x + positions_affected, SEARCH_SPACE_X)
    else:
        start_x = sensor.x - positions_affected
        end_x = sensor.x + positions_affected

    return start_x, end_x


def is_overlapping(range1: Tuple[int, int], range2: Tuple[int, int]) -> bool:
    return range1[0] <= range2[0] <= range1[1] or range1[0] <= range2[1] <= range1[1]


def merge_ranges(range1: Tuple[int, int], range2: Tuple[int, int]) -> Tuple[int, int]:
    return min(range1[0], range2[0]), max(range1[1], range2[1])


def tuning_frequency(x: int, y: int):
    return 4000000 * x + y


with open("input.txt") as file:
    lines: List[str] = file.readlines()

    sensors: Dict[Location, Location] = {}

    location_regex: str = r"x=(-?\d+), y=(-?\d+)"

    for line in lines:
        sensor_part, beacon_part = line.split(":")

        sensor_match = re.search(location_regex, sensor_part)
        beacon_match = re.search(location_regex, beacon_part)

        sensors[Location(int(sensor_match.group(1)), int(sensor_match.group(2)))] = Location(int(beacon_match.group(1)), int(beacon_match.group(2)))

    # Part 1
    sensor_distances: Dict[Location, int] = {}
    min_x: int = 0
    max_x: int = 0
    row_of_interest: int = 2000000
    locations_covered_in_row: Set[int] = set()
    for sensor, beacon in sensors.items():
        sensor_distances[sensor] = manhattan_distance(sensor, beacon)

        min_x = min(min_x, sensor.x - sensor_distances[sensor])
        max_x = max(max_x, sensor.x + sensor_distances[sensor])

        sensor_range = range_affected_by_sensor_in_row(sensor, sensor_distances[sensor], row_of_interest)
        locations_covered_in_row.update(list(range(sensor_range[0], sensor_range[1] + 1)))
        if beacon.y == row_of_interest:
            locations_covered_in_row.discard(beacon.x)

    print(len(locations_covered_in_row))

    # Part 2
    possible_locations = set(range(0, SEARCH_SPACE_X + 1))
    for y in range(0, SEARCH_SPACE_Y + 1):
        impossible_ranges: List[Tuple[int, int]] = []

        for sensor in sensors.keys():
            impossible_ranges.append(range_affected_by_sensor_in_row(sensor, sensor_distances[sensor], y, restrict_range=True))

        impossible_ranges.sort(key=lambda x: x[0])

        i: int = 0
        current_length: int = len(impossible_ranges)
        while i < current_length:
            if i + 1 >= current_length:
                break
            if is_overlapping(impossible_ranges[i], impossible_ranges[i + 1]):
                impossible_ranges[i] = merge_ranges(impossible_ranges[i], impossible_ranges[i + 1])
                impossible_ranges.pop(i + 1)
                i -= 1

            i += 1
            current_length = len(impossible_ranges)

        if len(impossible_ranges) == 2:
            if impossible_ranges[1][0] - impossible_ranges[0][1] == 2:
                print(f"Found beacon! x: {impossible_ranges[0][1] + 1}, y: {y} - Frequency: {tuning_frequency(impossible_ranges[0][1] + 1, y)}")
                break
