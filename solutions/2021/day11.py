from utils.abstract import FileReaderSolution
from abc import abstractmethod
from enum import Enum


class Octopus:
    flashed: bool

    def __init__(self, energy):
        self.energy = energy
        self.flashed = False

    def __str__(self):
        return f"{self.energy}"

    def __repr__(self):
        return f"{self.energy}"

    @staticmethod
    def increase_by_one(octopus, x, y):
        octopus.energy += 1


class Grid:
    data: []

    def __init__(self, input):
        self.data = []
        lines = input.splitlines()
        self.height = len(lines)
        self.width = len(lines[0])
        for line in lines:
            self.data.append(list(map(lambda x: Octopus(int(x)), [char for char in line])))

    def __str__ (self):
        str = ""
        for y in range(self.height):
            for x in range(self.width):
                str += f"{self.data[y][x]}"
            str += "\n"
        return str

    def for_all(self, func):
        for y in range(self.height):
            for x in range(self.width):
                func(self.data[y][x], x, y)

    def count_all_flashes(self):
        amount = 0
        for y in range(self.height):
            for x in range(self.width):
                if self.data[y][x].flashed:
                    amount += 1
        return amount

    @staticmethod
    def reset_flashes(octopus: Octopus, x, y):
        octopus.flashed = False

    def handle_flashing(self, octopus: Octopus, x, y):
        if octopus.energy <= 9:
            return

        octopus.energy = 0
        octopus.flashed = True

        for dy in range(-1, 2):
            for dx in range(-1, 2):
                if dx == dy and dx == 0:
                    continue

                if x + dx < 0 or x + dx >= self.width:
                    continue

                if y + dy < 0 or y + dy >= self.width:
                    continue

                neighbour = self.data[y+dy][x+dx]
                if not neighbour.flashed:
                    neighbour.energy += 1
                    self.handle_flashing(neighbour, x+dx, y+dy)


class Day11:
    grid: Grid

    @abstractmethod
    def solve_part(self, median):
        pass

    def solve(self, input_data: str) -> int:
        self.parse_input(input_data)

        return self.solve_part()

    def parse_input(self, input_data: str):
        self.grid = Grid(input_data)

    def common_solver(self):
        pass


class Day11PartA(Day11, FileReaderSolution):

    def solve_part(self) -> int:
        days = 100
        amount_of_flashes = 0

        for day in range(days):
            self.grid.for_all(self.grid.reset_flashes)
            self.grid.for_all(Octopus.increase_by_one)
            self.grid.for_all(self.grid.handle_flashing)
            amount_of_flashes += self.grid.count_all_flashes()

        return amount_of_flashes


class Day11PartB(Day11, FileReaderSolution):
    def solve_part(self) -> int:
        day = 0
        while True:
            day += 1
            self.grid.for_all(self.grid.reset_flashes)
            self.grid.for_all(Octopus.increase_by_one)
            self.grid.for_all(self.grid.handle_flashing)
            amount_of_flashes = self.grid.count_all_flashes()

            if amount_of_flashes == self.grid.width * self.grid.height:
                return day
