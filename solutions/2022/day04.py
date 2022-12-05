from abc import abstractmethod
from utils.abstract import FileReaderSolution


class Day04:
    def is_contained_by(self, a, b):
        return self.check(a, b) or self.check(b, a)

    def base_solve(self, input_data):
        count = 0
        for line in input_data.split("\n"):
            sections = list(map(lambda x:  pytx.split("-"), line.split(",")))
            if self.is_contained_by(
                    list(map(int, sections[0])),
                    list(map(int, sections[1]))
            ):
                count += 1

        return count

    @abstractmethod
    def check(self, a, b):
        raise NotImplementedError


class Day04PartA(Day04, FileReaderSolution):
    @staticmethod
    def check(a, b):
        return a[0] <= b[0] and a[1] >= b[1]

    def solve(self, input_data: str) -> int:
        return self.base_solve(input_data)


class Day04PartB(Day04, FileReaderSolution):
    @staticmethod
    def check(a, b):
        return a[0] <= b[0] <= a[1] or a[0] <= b[1] <= a[1]

    def solve(self, input_data: str) -> int:
        return self.base_solve(input_data)
