from utils.abstract import FileReaderSolution
from collections import OrderedDict


class Day06:
    @staticmethod
    def base_solve(line, length):
        return line.find(list(filter(lambda x: len(x) == length, ["".join(OrderedDict.fromkeys(line[i:i + length])) for i in range(0, len(line))]))[0]) + length


class Day06PartA(Day06, FileReaderSolution):
    def solve(self, input_data: str) -> int:
        return self.base_solve(input_data, 4)


class Day06PartB(Day06, FileReaderSolution):
    def solve(self, input_data: str) -> int:
        return self.base_solve(input_data, 14)
