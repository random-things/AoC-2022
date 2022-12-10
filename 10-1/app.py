

class Emulator:
    register_x: int = 1
    cycles: int = 0
    cycle_watches: set[int] = set()
    strength_total: int = 0
    crt_position: int = 0

    def __init__(self):
        self.register_x = 1
        self.cycles = 0
        self.cycle_watches = {20, 60, 100, 140, 180, 220}
        self.strength_total = 0

    def run_command(self, command: str, *args):
        if command == "addx":
            self.tick()
            self.tick()
            self.register_x += int(args[0])
        elif command == "noop":
            self.tick()

    def tick(self):
        if any(pos == self.crt_position for pos in range(self.register_x - 1, self.register_x + 2)):
            print("#", end="")
        else:
            print(".", end="")
        if self.crt_position == 39:
            print("")

        self.cycles += 1
        self.crt_position = self.cycles % 40

        if self.cycles in self.cycle_watches:
            signal_strength: int = self.register_x * self.cycles
            self.strength_total += signal_strength


with open("input.txt") as file:
    lines = file.readlines()

    emulator = Emulator()

    for line in lines:
        command = line.strip().split(" ")
        emulator.run_command(command[0], *command[1:])

    print(emulator.strength_total)
