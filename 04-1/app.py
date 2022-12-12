from typing import List

with open("input.txt") as file:
    contents: List[str] = list(map(lambda s: s.strip(), file.readlines()))

    total_assignments: int = len(contents)
    fully_contained_assignments: int = 0
    uncontained_assignments: int = 0
    for line in contents:
        assignment1, assignment2 = list(map(lambda a: list(map(int, a.split('-'))), line.split(",")))

        if (assignment1[0] <= assignment2[0] and assignment1[1] >= assignment2[1]) or \
                (assignment2[0] <= assignment1[0] and assignment2[1] >= assignment1[1]):
            fully_contained_assignments += 1

        if (assignment1[1] < assignment2[0]) or (assignment2[1] < assignment1[0]):
            uncontained_assignments += 1

    print(f"Fully contained assignments: {fully_contained_assignments}")
    print(f"Partially contained assignments: {total_assignments - uncontained_assignments}")
