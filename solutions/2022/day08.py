from utils.abstract import FileReaderSolution
import numpy as np


class Day08:
    A: None
    V: None

    def parse(self, input_data):
        lines = input_data.split("\n")
        height = len(lines)
        width = len(lines[0])
        self.A = np.empty((width, height))
        self.V = np.empty((width, height))

        for y, line in enumerate(lines):
            for x, digit in enumerate(line):
                self.A[y, x] = digit
                self.V[y, x] = 1 if y == 0 or x == 0 or y == height-1 or x == width-1 else 0


class Day08PartA(Day08, FileReaderSolution):
    def solve(self, input_data: str) -> int:
        self.parse(input_data)
        for i in range(0, 4):
            for j in range(self.A.shape[1]):
                row = self.A[j]
                max = row[0]
                for k in range(1, self.A.shape[0]):
                    if row[k] > max:
                        self.V[j, k] = 1
                        max = row[k]
            self.A = np.rot90(self.A)
            self.V = np.rot90(self.V)

        return np.count_nonzero(self.V)


class Day08PartB(Day08, FileReaderSolution):
    def check_direction(self, dir, x, y):
        (dx, dy, count) = (x, y, 0)

        while True:
            (dx, dy) = (dx + dir[0], dy + dir[1])
            if dx < 0 or dx >= self.A.shape[1] or dy < 0 or dy >= self.A.shape[0]:
                return count

            count += 1

            if self.A[dy, dx] >= self.A[y, x]:
                return count

    def calculate_scenic_score(self, x, y):
        return np.prod([self.check_direction(dir, x, y) for dir in [(0, -1), (-1, 0), (0, 1), (1, 0)]])

    def solve(self, input_data: str) -> int:
        self.parse(input_data)
        max = 0
        for y in range(1, self.A.shape[0]-1):
            score = np.max([self.calculate_scenic_score(x,y) for x in range(1, self.A.shape[1]-1)])
            if score > max:
                max = score

        return max
