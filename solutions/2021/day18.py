from utils.abstract import FileReaderSolution, TestSolution
from abc import abstractmethod
import operator
from math import floor, ceil


class Day18:
    def __init__(self):
        self.lines = []

    def solve(self, input_data: str) -> int:
        self.parse_input(input_data)

        return self.solve_part()

    def parse_input(self, input_data: str):
        self.lines = input_data.splitlines()

    def common_solver(self):
        pass

    @staticmethod
    def find_matching_values(values, depth, func):
        for pos in range(len(values)):
            if values[pos][1] != depth:
                continue

            for x in range(pos + 1, len(values)):
                if values[x][1] == depth:
                    func(pos, x)
                    return values, True

        return values, False

    def magnitude(self, values):
        def func(pos, other):
            values[pos] = [3*values[pos][0]+2*values[other][0], values[pos][1] - 1]
            del values[other]

        while len(values) > 1:
            max_depth = max(values, key=operator.itemgetter(1))[1]
            values, _ = self.find_matching_values(values, max_depth, func)

        return values[0][0]

    def explode(self, values):
        def func(pos, other):
            if other < len(values) - 1:
                values[other + 1][0] += values[other][0]

            if pos > 0:
                values[pos - 1][0] += values[pos][0]

            values[pos] = [0, values[pos][1] - 1]
            del values[other]

        return self.find_matching_values(values, 4, func)

    @staticmethod
    def split(values):
        has_split = False
        for x in range(len(values)):
            if values[x][0] >= 10:

                half = values[x][0] / 2
                depth = values[x][1] + 1

                split = [[floor(half), depth], [ceil(half), depth]]

                values = values[:x] + split + values[x+1:]
                has_split = True

                break

        return values, has_split

    @staticmethod
    def flatten(line):
        values = []
        depth = 0

        for s in line[1:-1]:
            if s == "[":
                depth += 1
            elif s == "]":
                depth -= 1
            elif s.isnumeric():
                values.append([int(s), depth])
        return values

    @staticmethod
    def add(a, b):
        def increment_depth(x):
            return [x[0], x[1]+1]

        if a is None:
            return b

        added = list(map(increment_depth, a)) + list(map(increment_depth, b))
        return added

    def actions(self, a, b):
        values = self.add(a, b)

        has_split = True
        while has_split:
            values, has_exploded = self.explode(values)
            if not has_exploded:
                values, has_split = self.split(values)

        return values


class Day18PartA(Day18, FileReaderSolution):
    def solve_part(self) -> int:
        current = None
        for line in self.lines:
            line = self.flatten(line)
            current = self.actions(current, line)

        return self.magnitude(current)


class Day18PartB(Day18, FileReaderSolution):
    def solve_part(self) -> int:
        magnitudes = []
        for line_a in self.lines:
            for line_b in self.lines:
                if line_a == line_b:
                    continue

                values = self.actions(self.flatten(line_a), self.flatten(line_b))
                magnitudes.append(self.magnitude(values))

        return max(magnitudes)


class Day18Tests(Day18, TestSolution):
    import unittest
    def run_tests(self):
        # Arrange

        input = "[[[[1,1],[2,2]],[3,3]],[4,4]]"
        values = self.flatten(input)
        expected = 143

        # Act
        actual = self.magnitude(values)

        # Assert
        print(actual, expected)
        pass
