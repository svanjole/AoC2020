from utils.abstract import FileReaderSolution


class Day10:
    cycle: int
    signal: int
    register: {}
    crt: str

    def __init__(self):
        self.cycle = 1
        self.signal = 0
        self.register = {
            "x": 1
        }
        self.crt = ""
        self.crt_size = 40

    def inc_and_process_cycle(self):
        self.cycle += 1
        if (self.cycle - 20) % self.crt_size == 0:
            self.signal += self.cycle * (self.register["x"])

    def base_solve(self, input_data: str) -> int:
        for instruction in [line.split(" ") for line in input_data.split("\n")]:
            self.handle_sprite()
            self.inc_and_process_cycle()

            match instruction[0]:
                case "addx":
                    self.handle_sprite()
                    self.register["x"] += int(instruction[1])
                    self.inc_and_process_cycle()

        return self.signal

    def handle_sprite(self):
        self.crt += "#" if -1 <= (self.register["x"]+1-(self.cycle % 40)) <= 1 else " "


class Day10PartA(Day10, FileReaderSolution):
    def solve(self, input_data: str):
        return self.base_solve(input_data)


class Day10PartB(Day10, FileReaderSolution):
    def solve(self, input_data: str) -> int:
        self.base_solve(input_data)
        parts = [self.crt[i:i + self.crt_size] for i in range(0, len(self.crt), self.crt_size)]
        result = "\n".join(parts)
        return f"\n{result}"







