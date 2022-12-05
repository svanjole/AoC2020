import math

from utils.abstract import FileReaderSolution
from abc import abstractmethod
import statistics


class Day09:
    def __init__(self):
        self.heightmap = []
        self.width = 0
        self.height = 0

    @abstractmethod
    def solve_part(self, median):
        pass

    def solve(self, input_data: str) -> int:
        self.parse_input(input_data)

        return self.solve_part()

    def parse_input(self, input_data: str):
        lines = input_data.splitlines()
        self.height = len(lines)
        self.heightmap = []
        for line in lines:
            numbers = list(map(lambda x: int(x), [char for char in line]))
            self.width = len(numbers)
            self.heightmap.append(numbers)

    def common_solver(self):
        pass


class Day09PartA(Day09, FileReaderSolution):
    def solve_part(self) -> int:
        directions = [
            [0, -1],  # up
            #[1, -1],  # up right
            [1, 0],  # right
            #[1, 1],  # down right
            [0, 1],  # down
            #[-1, 1],  # down left
            [-1, 0],  # left
            #[-1, -1],  # left up
        ]
        low_points = []
        for y in range(self.height):
            for x in range(self.width):
                location = self.heightmap[y][x]
                is_lowest_point = True
                for direction in directions:
                    dx = x + direction[0]
                    dy = y + direction[1]

                    if dx < 0 or dx >= self.width:
                        continue
                    if dy < 0 or dy >= self.height:
                        continue

                    if self.heightmap[dy][dx] <= location:
                        is_lowest_point = False
                        break

                if is_lowest_point:
                    low_points.append(location)

        return sum(low_points) + len(low_points)


class Day09PartB(Day09, FileReaderSolution):
    def solve_part(self) -> int:
        for y in range(self.height):
            for x in range(self.width):
                self.heightmap[y][x] = "#" if self.heightmap[y][x] == 9 else " "

        basin_sizes = []

        for y in range(self.height):
            for x in range(self.width):
                if self.heightmap[y][x] == " ":
                    size = self.floodfill(x, y)
                    basin_sizes.append(size);

        return math.prod(sorted(basin_sizes)[-3:])

    def floodfill(self, x, y):
        if self.heightmap[y][x] != " ":
            return 0

        self.heightmap[y][x] = "."

        directions = [
            [0, -1],  # up
            # [1, -1],  # up right
            [1, 0],  # right
            # [1, 1],  # down right
            [0, 1],  # down
            # [-1, 1],  # down left
            [-1, 0],  # left
            # [-1, -1],  # left up
        ]
        count = 1
        for direction in directions:
            dx = x + direction[0]
            dy = y + direction[1]

            if dx < 0 or dx >= self.width:
                continue
            if dy < 0 or dy >= self.height:
                continue

            count += self.floodfill(dx, dy)

        return count
