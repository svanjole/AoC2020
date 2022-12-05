from utils.abstract import FileReaderSolution
from abc import abstractmethod
from collections import defaultdict


class Day14:
    def __init__(self):
        self.rules = {}
        self.polymer = ""
        self.pairs = defaultdict(int)
        self.amounts = defaultdict(int)

    @abstractmethod
    def solve_part(self):
        pass

    def solve(self, input_data: str) -> int:
        self.parse_input(input_data)

        for pair in [self.polymer[i:i + 2] for i in range(len(self.polymer) - 1)]:
            self.pairs[pair] += 1

        for letter in self.polymer:
            self.amounts[letter] += 1

        return self.solve_part()

    def parse_input(self, input_data: str):
        lines = input_data.splitlines()
        first_line = True
        for line in lines:
            if first_line:
                self.polymer = line
                first_line = False
                continue

            if len(line) == 0:
                continue

            parts = line.split(" -> ")
            self.rules[parts[0]] = parts[1]

    def common_solver(self, steps: int):
        for step in range(steps):
            pairs = defaultdict(int)

            for pair, amount in self.pairs.items():
                inserted = self.rules.get(pair)
                pairs[pair[0] + inserted] += amount
                pairs[inserted + pair[1]] += amount
                self.amounts[inserted] += amount

            self.pairs = pairs

        return max(self.amounts.values()) - min(self.amounts.values())


class Day14PartA(Day14, FileReaderSolution):
    def solve_part(self) -> int:
        return self.common_solver(10)


class Day14PartB(Day14, FileReaderSolution):
    def solve_part(self) -> int:
        return self.common_solver(40)
