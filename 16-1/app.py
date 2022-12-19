import dataclasses
import re
from enum import Enum
from typing import List, Dict, Set, Iterable


class ValveState(Enum):
    OPEN = "open"
    CLOSED = "closed"


@dataclasses.dataclass
class Valve:
    name: str = ""
    flow_rate: int = 0
    state: ValveState = ValveState.CLOSED
    to_valves: List[str] = dataclasses.field(default_factory=list)

    def open(self):
        self.state = ValveState.OPEN


def find_node_from(valve1: str, valve2: str, recur_count: int = 0, parents: List[str] = None):
    if parents is None:
        parents = [valve1]
    else:
        parents.append(valve1)

    parent_copy: List[str] = parents.copy()

    v1 = valves[valve1]

    steps = [v for v in v1.to_valves if v not in parent_copy]
    paths: List[List[str]] = []
    for step in steps:
        parent_copy = parent_copy[0:recur_count+1]
        if step == valve2:
            paths.append(parents + [valve2])
        else:
            additional_path = find_node_from(step, valve2, recur_count + 1, parent_copy)
            if len(additional_path) > 0:
                paths.append(additional_path)

    if len(paths) == 0:
        return []

    # Return the path with the minimum length
    return min(paths, key=len)


def evaluate_node_path(node_path: Iterable[str]):
    global distances
    total_flow: int = 0
    current_minute: int = 30
    current_node: str = "AA"

    for node in node_path:
        try:
            distance = distances[current_node][node]
        except KeyError:
            return -1
        if distance == 0:
            continue

        current_minute -= distance
        current_minute -= 1  # Subtract one minute for the valve to open
        total_flow += valves[node].flow_rate * current_minute
        current_node = valves[node].name

        if current_minute <= 0:
            return -1

    return total_flow


def build_path(current_path: List[str], available_sorted_nodes: List[str]):
    best_flow: int = -1
    for node in available_sorted_nodes:
        if node in current_path:
            continue

        new_path = current_path + [node]
        flow = evaluate_node_path(new_path)
        best_flow = max(best_flow, flow)
        if flow <= 0:
            continue
        if len(new_path) != len(available_sorted_nodes):
            best_flow = max(build_path(new_path, available_sorted_nodes), best_flow)

    return best_flow


with open("input-demo.txt") as file:
    lines: List[str] = list(map(str.strip, file.readlines()))

    valves: Dict[str, Valve] = {}
    for line in lines:
        match = re.match(r"Valve (\w\w) has flow rate=(\d+); tunnels? leads? to valves? ([A-Z,\s]+)", line)

        valve_id: str = match.group(1)
        flow_rate: int = int(match.group(2))
        to_valves: List[str] = match.group(3).split(", ")

        valve = Valve(name=valve_id, flow_rate=flow_rate, to_valves=to_valves, state=ValveState.CLOSED)
        valves[valve_id] = valve

    # Part 1
    nodes_to_visit: Set[str] = set(key for key, value in valves.items() if value.flow_rate > 0)
    nodes_to_visit.add("AA")

    # Build a table of distances between nodes
    distances: Dict[str, Dict[str, int]] = {}
    for node in nodes_to_visit:
        distances[node] = {}
        for node2 in nodes_to_visit:
            if node == node2:
                continue
            distances[node][node2] = len(find_node_from(node, node2)) - 1

    nodes_to_visit.remove("AA")

    # Find the path with the most flow that visits all of the nodes
    sorted_nodes = sorted(nodes_to_visit, key=lambda x: valves[x].flow_rate, reverse=True)
    best: int = 0
    for node in sorted_nodes:
        flow = build_path([node], sorted_nodes)
        if flow > best:
            best = flow

    print(f"Best flow: {best}")

    # Part 2
    # Find two paths that visit all of the nodes with the most flow