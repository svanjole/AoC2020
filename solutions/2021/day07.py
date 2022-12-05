from utils.abstract import FileReaderSolution
from abc import abstractmethod
import statistics


class Day07:
    def __init__(self):
        self.numbers = []

    @abstractmethod
    def solve_part(self, median):
        pass

    def solve(self, input_data: str) -> int:
        self.parse_input(input_data)

        return self.solve_part()

    def parse_input(self, input_data: str):
        lines = input_data.splitlines()
        self.numbers = list(map(lambda x: int(x), lines[0].split(",")))

    def common_solver(self):
        pass


class Day07PartA(Day07, FileReaderSolution):
    def solve_part(self) -> int:
        offset = statistics.median(self.numbers)
        return sum(list(map(lambda x:  int(abs(x - offset)), self.numbers)))


class Day07PartB(Day07, FileReaderSolution):
    def solve_part(self) -> int:
        min_offset = min(self.numbers)
        max_offset = max(self.numbers)

        best = 999999999

        for offset in range(min_offset, max_offset):
            current = sum(list(map(lambda x: sum(range(1, int(abs(x - offset))+1)), self.numbers)))
            if current < best:
                best = current

        return best