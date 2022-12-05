from utils.abstract import FileReaderSolution
from abc import abstractmethod


class Day06:
    def __init__(self):
        self.numbers = []

    @abstractmethod
    def solve_part(self):
        pass

    def solve(self, input_data: str) -> int:
        self.parse_input(input_data)
        return self.solve_part()

    def parse_input(self, input_data: str):
        lines = input_data.splitlines()
        numbers = list(map(lambda x: int(x), lines[0].split(",")))
        self.numbers = [numbers.count(i) for i in range(0, 9)]

    def common_solver(self, days: int):
        for day in range(days):
            self.numbers[(day + 7) % 9] += self.numbers[day % 9]

        return sum(self.numbers)


class Day06PartA(Day06, FileReaderSolution):
    def solve_part(self) -> int:
        return self.common_solver(80)


class Day06PartB(Day06, FileReaderSolution):
    def solve_part(self) -> int:
        return self.common_solver(256)