from typing import List

current_elf: int = 0
elf_calories: List[int] = []

with open("input.txt", "r") as file:
    contents: str = file.read()

    calories_by_elf = contents.split("\n\n")
    total_calories_by_elf = list(map(lambda s: sum(map(int, s.split("\n"))), calories_by_elf))
    print(f"Calories carried by elf with most calories: {max(total_calories_by_elf)}")

    total_calories_by_elf.sort(reverse=True)
    print(f"Calories carried by the three elves with the most calories: {sum(total_calories_by_elf[:3])}")
