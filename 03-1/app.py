def get_priority(letter: str) -> int:
    ret: int = ord(letter) - ord('a') + 1
    if ret < 0:
        ret = ord(letter) - ord('A') + 27
    return ret


with open("input.txt") as file:
    contents = file.read()

    total_priority = 0
    for line in contents.split("\n"):
        length: int = int(len(line) / 2)
        compartment1, compartment2 = set(line[0:length]), set(line[length:])

        shared_items = compartment1 & compartment2

        # Assumes one item in common between compartments.
        total_priority += get_priority(shared_items.pop())

    print(f"Total priority across bags: {total_priority}")
