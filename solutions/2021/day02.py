from utils.abstract import FileReaderSolution
import abc


class Submarine(metaclass=abc.ABCMeta):
    horizontal: int = 0
    depth: int = 0

    def handle_instruction(self, action, value):
        switcher = {
            "forward": self.forward,
            "up": self.up,
            "down": self.down
        }
        func = switcher.get(action)
        func(value)

    @abc.abstractmethod
    def forward(self, i):
        pass

    @abc.abstractmethod
    def down(self, i):
        pass

    @abc.abstractmethod
    def up(self, i):
        pass

    @abc.abstractmethod
    def get_current_location(self):
        pass


class SubmarineDay1(Submarine):
    aim: int = 0

    def get_current_location(self):
        return self.horizontal * self.depth

    def forward(self, i):
        self.horizontal += i

    def down(self, i):
        self.depth += i

    def up(self, i):
        self.depth -= i


class SubmarineDay2(Submarine):
    aim: int = 0

    def get_current_location(self):
        return self.horizontal * self.depth

    def forward(self, i):
        self.horizontal += i
        self.depth += self.aim * i

    def down(self, i):
        self.aim += i

    def up(self, i):
        self.aim -= i


class Day02:
    submarine: Submarine
    pass


class Day02PartA(Day02, FileReaderSolution):
    def solve(self, input_data: str) -> int:
        instructions = input_data.splitlines()
        submarine = SubmarineDay1()

        for line in instructions:
            instruction = line.split(" ")
            action = instruction[0]
            value = int(instruction[1])
            submarine.handle_instruction(action, value)

        return submarine.get_current_location()


class Day02PartB(Day02, FileReaderSolution):
    def solve(self, input_data: str) -> int:
        instructions = input_data.splitlines()
        submarine = SubmarineDay2()

        for line in instructions:
            instruction = line.split(" ")
            action = instruction[0]
            value = int(instruction[1])
            submarine.handle_instruction(action, value)

        return submarine.get_current_location()