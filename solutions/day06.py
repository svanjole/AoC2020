from utils.abstract import FileReaderSolution
from collections import OrderedDict, Counter


class Day06:
    @staticmethod
    def solve_internal(input_data: str):
        return input_data.split("\n\n")


class Day06PartA(Day06, FileReaderSolution):

    def solve(self, input_data: str) -> int:
        groups = list(map(lambda x: ("".join(x.split("\n"))), self.solve_internal(input_data)))

        return sum(map(lambda x: len("".join(OrderedDict.fromkeys(x))), groups))


class Day06PartB(Day06, FileReaderSolution):

    def solve(self, input_data: str) -> int:
        groups = self.solve_internal(input_data)
        total = 0

        for group in groups:
            participants = group.split("\n")
            frequency = Counter(''.join(participants))

            filtered = list(filter(lambda x: frequency[x] == len(participants), frequency.keys()))
            total += len(filtered)

        return total
