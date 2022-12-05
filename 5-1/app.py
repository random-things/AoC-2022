from typing import Dict
from typing import List

from enum import Enum, auto


class CrateMover(Enum):
    V9000 = auto()
    V9001 = auto()


current_crate_mover = CrateMover.V9001

with open("input.txt") as file:
    stacks, lines = file.read().split("\n\n")

    stacks = stacks.split("\n")
    stacks.reverse()

    row_list: Dict[int, List[str]] = {key: [] for key in list(map(int, stacks.pop(0).split()))}

    for line in stacks:
        length = len(line)
        for i in range(0, length, 4):
            contents = line[i:i+4].translate(str.maketrans("[]", "  ")).strip()
            if contents:
                row_list[int(i / 4) + 1].append(contents)

    for line in lines.split("\n"):
        quantity, source, target = list(map(int, line.replace("move", "").replace("from", "").replace("to", "").replace("  ", " ").strip().split(" ")))

        if current_crate_mover == CrateMover.V9000:
            for i in range(quantity):
                row_list[target].append(row_list[source].pop())
        elif current_crate_mover == CrateMover.V9001:
            row_list[target].extend(row_list[source][-quantity:])
            row_list[source] = row_list[source][:-quantity]

    print("".join([value[-1:][0] for value in row_list.values()]))
