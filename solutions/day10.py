from utils.abstract import FileReaderSolution
from collections import Counter
from itertools import groupby
import math


class Day10:
    @staticmethod
    def tribonacci(n):
        if n == 0:
            return 0
        elif n == 1:
            return 0
        elif n == 2:
            return 1
        else:
            return Day10.tribonacci(n - 1) + Day10.tribonacci(n - 2) + Day10.tribonacci(n - 3)

    @staticmethod
    def get_differences(input_data: str) -> []:
        list_of_numbers = list(map(lambda x: int(x), input_data.split("\n")))
        list_of_numbers.append(0)

        list_of_numbers.sort()
        list_of_numbers.append(max(list_of_numbers) + 3)

        differences = [list_of_numbers[n] - list_of_numbers[n - 1] for n in range(1, len(list_of_numbers))]

        return differences


class Day10PartA(Day10, FileReaderSolution):
    def solve(self, input_data: str) -> int:
        differences = self.get_differences(input_data)
        counter = Counter(differences)

        return counter[1] * counter[3]


class Day10PartB(Day10, FileReaderSolution):
    def solve(self, input_data: str) -> int:
        differences = self.get_differences(input_data)

        groups = [(k, sum(1 for i in g)) for k, g in groupby(differences)]
        valid_groups = list(filter(lambda x: x[0] == 1, groups))

        return math.prod(self.tribonacci(group[1]+2) for group in valid_groups)
