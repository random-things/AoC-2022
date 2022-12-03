from typing import List


def get_priority(letter: str) -> int:
    ret: int = ord(letter) - ord('a') + 1
    if ret < 0:
        ret = ord(letter) - ord('A') + 27
    return ret


with open("input.txt") as file:
    contents: List[str] = list(map(lambda l: l.strip(), file.readlines()))

    total_priority = 0
    for i in range(0, len(contents), 3):
        shared_items = set(contents[i]) & set(contents[i+1]) & set(contents[i+2])

        # Assumes one item in common between compartments.
        total_priority += get_priority(shared_items.pop())

    print(f"Total priority across bags: {total_priority}")
