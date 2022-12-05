from utils.abstract import FileReaderSolution
from abc import abstractmethod


class Probe:
    pos: []
    velocity: []

    def __init__(self, pos, velocity):
        self.pos = pos
        self.velocity = velocity

    def perform_step(self):
        self.pos = list(map(sum, zip(self.pos, self.velocity)))

        if self.velocity[0] > 0:
            self.velocity[0] -= 1

        self.velocity[1] -= 1

    def within(self, range_x, range_y):
        return range_x[0] <= self.pos[0] <= range_x[1] and range_y[0] <= self.pos[1] <= range_y[1]


class Day17:
    range_x = ()
    range_y = ()

    def __init__(self):
        pass

    @abstractmethod
    def solve_part(self, median):
        pass

    @abstractmethod
    def parse_boundaries(self, line):
        return list(map(lambda x: int(x), line[2:].split("..")))

    def solve(self, input_data: str) -> int:
        self.parse_input(input_data)

        return self.solve_part()

    def parse_input(self, input_data: str):
        line = input_data.splitlines()[0]
        line = line.replace("target area: ", "")
        line = line.split(", ")
        self.range_x = self.parse_boundaries(line[0])
        self.range_y = self.parse_boundaries(line[1])

    def common_solver(self):
        max_values = {}
        for x in range(1, self.range_x[1] + 1):
            for y in range(self.range_y[0], 176):
                # print(f"New Probe: ({x},{y})")
                p = Probe([0, 0], [x, y])
                max_y = 0

                while True:
                    p.perform_step()
                    if p.pos[0] > self.range_x[1]:
                        break

                    if p.pos[1] < self.range_y[0]:
                        break

                    if p.pos[1] > max_y:
                        max_y = p.pos[1]

                    if p.within(self.range_x, self.range_y):
                        max_values[(x, y)] = max_y

        return max_values


class Day17PartA(Day17, FileReaderSolution):
    def solve_part(self) -> int:
        values = self.common_solver()
        return max(values.values())


class Day17PartB(Day17, FileReaderSolution):
    def solve_part(self) -> int:
        values = self.common_solver()
        return len(values)

