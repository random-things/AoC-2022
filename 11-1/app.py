import dataclasses
import math
import operator
from typing import List, Callable


class Operation:
    op: Callable
    value: str
    is_numeric_value: bool

    def __init__(self, op: str, value: str):
        operator_map: dict[str, Callable] = {
            "+": operator.add,
            "*": operator.mul,
            "divisible": operator.mod,
        }

        self.op = operator_map[op]
        self.value = value
        self.is_numeric_value = value.isnumeric()


@dataclasses.dataclass
class Test:
    condition: Operation
    if_true: int = 0
    if_false: int = 0


@dataclasses.dataclass
class Monkey:
    id: int = 0
    items: List[int] = dataclasses.field(default_factory=list)
    operation: Operation = None
    test: Test = None
    inspection_count: int = 0

    def inspect_item(self) -> int:
        self.inspection_count += 1
        return self.items.pop(0)


def parse_block(block: str) -> Monkey:
    """
    Monkey 0:
     Starting items: 79, 98
     Operation: new = old * 19
     Test: divisible by 23
      If true: throw to monkey 2
      If false: throw to monkey 3
    :param block:
    :return:
    """
    lines = block.split("\n")
    monkey = Monkey()

    for i, line in enumerate(lines):
        if i == 0:
            monkey.id = int(line.split(":")[0].split(" ")[1])
        elif i == 1:
            monkey.items = [int(x) for x in line.split(":")[1].split(", ")]
        elif i == 2:
            operation_line = line.split(":")[1].strip()
            # ["new", "=", "old", "*", "19"]
            _, _, _, operation, value = operation_line.split(" ")
            monkey.operation = Operation(operation, value)
        elif i == 3:
            operation, condition = line.split(":")[1].strip().split(" by ")
            monkey.test = Test(Operation(operation, condition))
        elif i == 4:
            monkey.test.if_true = int(line.split("monkey")[1].strip())
        elif i == 5:
            monkey.test.if_false = int(line.split("monkey")[1].strip())

    return monkey


def run_rounds(monkeys: List[Monkey], number_of_rounds: int = 1, divisor: int = 3, debug=False):
    lcm: int = math.lcm(*[int(monkey.test.condition.value) for monkey in monkeys])
    for i in range(number_of_rounds):
        for monkey in monkeys:
            while len(monkey.items) > 0:
                item = monkey.inspect_item()
                if debug:
                    print(f"Monkey {monkey.id} is inspecting item {item}")
                new_worry_level: int = monkey.operation.op(item,
                                                           int(monkey.operation.value)) if monkey.operation.is_numeric_value else monkey.operation.op(
                    item, item)
                if debug:
                    print(f"Monkey {monkey.id} is inspecting item {item} with worry level {new_worry_level}")

                item_worry_level = new_worry_level % lcm // divisor

                if debug:
                    print(f"Monkey {monkey.id} is inspecting item {item} with worry level {item_worry_level}")
                    print(f"{monkey.test.condition.op(item_worry_level, int(monkey.test.condition.value))}")
                if monkey.test.condition.op(item_worry_level, int(monkey.test.condition.value)):
                    monkeys[monkey.test.if_false].items.append(item_worry_level)
                else:
                    monkeys[monkey.test.if_true].items.append(item_worry_level)
                if debug:
                    print(
                        f"Thrown to monkey {monkey.test.if_false if monkey.test.condition.op(item_worry_level, int(monkey.test.condition.value)) else monkey.test.if_true}")


with open("input.txt") as file:
    blocks = file.read().split("\n\n")

    # Part 1
    monkeys = [parse_block(block) for block in blocks]

    run_rounds(monkeys, 20, divisor=3)

    inspections = sorted([monkey.inspection_count for monkey in monkeys], reverse=True)
    monkey_business: int = inspections[0] * inspections[1]
    print(monkey_business)

    # Part 2
    # Reset the monkeys
    monkeys = [parse_block(block) for block in blocks]

    run_rounds(monkeys, 10000, divisor=1)

    inspections = sorted([monkey.inspection_count for monkey in monkeys], reverse=True)
    monkey_business: int = inspections[0] * inspections[1]
    print(monkey_business)
