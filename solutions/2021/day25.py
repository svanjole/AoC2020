from utils.abstract import FileReaderSolution
from abc import abstractmethod
from enum import Enum
import copy

class Day25:
    def __init__(self):
        self.grid = []

    @abstractmethod
    def solve_part(self):
        pass

    def solve(self, input_data: str) -> int:
        self.parse_input(input_data)

        return self.solve_part()

    def parse_input(self, input_data: str):
        lines = input_data.splitlines()
        self.grid = []
        for line in lines:
            self.grid.append([char for char in line])


    def move(self, grid):
        new_grid = copy.deepcopy(grid)
        changed = False
        width = len(grid[0])
        height = len(grid)
        for y in range(height):
            for x in range(width):
                if grid[y][x] == '>':
                    if x < width-1 and grid[y][x+1] == ".":
                        new_grid[y][x] = '.'
                        new_grid[y][x+1] = '>'
                        changed = True
                    elif x == width - 1 and grid[y][0] == ".":
                        new_grid[y][x] = '.'
                        new_grid[y][0] = '>'
                        changed = True

        grid = new_grid
        new_grid = copy.deepcopy(grid)
        for y in range(height):
            for x in range(width):
                if grid[y][x] == 'v':
                    if y < height-1 and grid[y+1][x] == ".":
                        new_grid[y][x] = '.'
                        new_grid[y+1][x] = 'v'
                        changed = True
                    elif y == height-1 and grid[0][x] == ".":
                        new_grid[y][x] = '.'
                        new_grid[0][x] = 'v'
                        changed = True

        return changed, new_grid

    def common_solver(self):
        pass


class Day25PartA(Day25, FileReaderSolution):
    def solve_part(self) -> int:
        def prettyprint(grid):
            for line in grid:
                print(''.join(line))

        changes = True
        steps = 0
        grid = self.grid
        prettyprint(grid)
        while changes:
            changes, grid = self.move(grid)
            steps += 1

            prettyprint(grid)

        return steps


class Day25PartB(Day25, FileReaderSolution):
    def solve_part(self) -> int:
        pass

