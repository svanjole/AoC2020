from utils.abstract import FileReaderSolution

class Day18:
    def __init__(self):
        self.cubes = {}
        self.sides = {}

    def parse(self, input_data):
        self.cubes = {tuple(map(int, line.split(','))) for line in input_data.split('\n')}
        self.sides = lambda x, y, z: {(x + 1, y, z), (x - 1, y, z), (x, y + 1, z), (x, y - 1, z), (x, y, z + 1),
                                 (x, y, z - 1)}

    def calculate_surface_area(self):
        exposed = 0
        for c in self.cubes:
            for s in self.sides(*c):
                if s not in self.cubes:
                    exposed += 1

        return exposed


class Day18PartA(Day18, FileReaderSolution):
    def solve(self, input_data: str) -> int:
        self.parse(input_data)
        exposed = self.calculate_surface_area()
        return exposed


class Day18PartB(Day18, FileReaderSolution):
    def adj(self, p):
        for axis in range(3):
            for d in (-1, 1):
                q = list(p)
                q[axis] += d
                yield tuple(q)
    def solve(self, input_data: str) -> int:
        self.parse(input_data)
        ranges = [op([item[i] for item in self.cubes]) for i in range(3) for op in [min, max]]
        seen = set()
        todo = [(0, 0, 0)]

        while todo:
            here = todo.pop()
            seen |= {here}
            todo += [s for s in (self.sides(*here) - self.cubes - seen) if all(-1 <= c <= 25 for c in s)]

        print(sum((s in seen) for c in self.cubes for s in self.sides(*c)))
        quit()
