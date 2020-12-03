from utils.abstract import FileReaderSolution
import math


class Day03:
    @staticmethod
    def traverse(input_data: str, slope) -> int:
        rows = input_data.split("\n")
        height = len(rows)
        width = len(rows[0])

        x = 0
        amount_of_trees = 0

        for y in range(0, height, slope[1]):
            x %= width

            if rows[y][x] == "#":
                amount_of_trees += 1

            x += slope[0]

        return amount_of_trees


class Day03PartA(Day03, FileReaderSolution):
    def solve(self, input_data: str) -> int:
        return self.traverse(input_data, [3, 1])


class Day03PartB(Day03, FileReaderSolution):
    def solve(self, input_data: str) -> int:
        slopes = [
            [1, 1],
            [3, 1],
            [5, 1],
            [7, 1],
            [1, 2]
        ]
        result = list(map(lambda x: self.traverse(input_data, x), slopes))
        return math.prod(result)
