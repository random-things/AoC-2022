from pathlib import Path
from typing import List, Callable, Dict

current_path: Path = Path("/")
current_command: str = ""
current_command_result: List[str] = []
directory_sizes: Dict[Path, int] = {}

TOTAL_FILESYSTEM_SIZE = 70000000
NEEDED_SPACE = 30000000


def parse_command(command: str, command_result: List[str]) -> List[str]:
    parts: List[str] = command.split(" ")

    func_key: str = "run_" + parts[0]
    args: List[str] = parts[1:]
    func: Callable = globals().get(func_key, None)
    if func is None:
        raise Exception(f"Unknown command: {parts[0]}")

    return func(*args, result=command_result)


def run_cd(directory: str, result: List[str]) -> None:
    global current_path
    if directory == "..":
        current_path = current_path.parent
        return
    if len(directory) > 0:
        current_path = current_path.joinpath(directory)

    if current_path not in directory_sizes:
        directory_sizes[current_path] = 0


def run_ls(result: List[str]) -> None:
    global current_path
    global directory_sizes

    for cmd_line in result:
        if cmd_line.startswith("dir"):
            continue

        size, filename = cmd_line.split(" ", 1)
        directory_sizes[current_path] += int(size)

        for parent in current_path.parents:
            if parent in directory_sizes:
                directory_sizes[parent] += int(size)
            elif parent not in directory_sizes:
                directory_sizes[parent] = int(size)


with open("input.txt") as file:
    lines: List[str] = list(map(lambda l: l.strip(), file.readlines()))

    for line in lines:
        if line.startswith("$ ") and current_command == "":
            current_command = line[2:].strip()
        elif line.startswith("$ ") and current_command != "":
            # Previous command has finished, parse the new one.
            parse_command(current_command, current_command_result)
            current_command = line[2:].strip()
            current_command_result = []
        else:
            current_command_result.append(line)

    # Parse the last command.
    parse_command(current_command, current_command_result)

    # Part 1
    print(sum(filter(lambda size: size <= 100000, directory_sizes.values())))

    # Part 2
    total_size: int = max(directory_sizes.values())
    unused_space: int = TOTAL_FILESYSTEM_SIZE - total_size
    print(min(filter(lambda size: unused_space + size >= NEEDED_SPACE, directory_sizes.values())))
