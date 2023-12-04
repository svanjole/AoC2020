from utils.abstract import FileReaderSolution


class Day14:
    def __init__(self):
        self.grid = {}
        self.boundaries = []
        self.start = (500, 0)

    def parse(self, lines):
        all_paths = []
        for chunk in lines.split("\n"):
            paths = []
            for parts in chunk.split(" -> "):
                path = tuple([int(part) for part in parts.split(",")])
                paths.append(path)
            all_paths.append(paths)

        self.boundaries = [999, 0, 0]
        for path in all_paths:
            start = path.pop(0)
            for pos in path:
                for x in range(min(start[0], pos[0]), max(start[0], pos[0]) + 1):
                    if x < self.boundaries[0]:
                        self.boundaries[0] = x
                    if x > self.boundaries[1]:
                        self.boundaries[1] = x

                    for y in range(min(start[1], pos[1]), max(start[1], pos[1]) + 1):
                        self.grid[(x, y)] = "#"

                        if y > self.boundaries[2]:
                            self.boundaries[2] = y
                start = pos

    def pretty_print(self):
        for y in range(self.boundaries[2]+1):
            output = ""
            for x in range(self.boundaries[0], self.boundaries[1]+1):
                output += self.grid[(x,y)] if (x, y) in self.grid else "."
            print(output)

    def pour_sand(self):
        x = 500
        for y in range(self.boundaries[2]):
            if (x, y + 1) not in self.grid:
                pass
            elif (x-1, y + 1) not in self.grid:
                x -= 1
            elif (x+1, y + 1) not in self.grid:
                x += 1
            else:
                self.grid[(x, y)] = "o"
                return (x, y) != self.start
        return False

    def base_solve(self, input_data, add_floor=False):
        self.parse(input_data)
        if add_floor:
            self.add_floor()

        while self.pour_sand():
            pass

        return sum(1 for value in self.grid.values() if value == 'o')


class Day14PartA(Day14, FileReaderSolution):
    def solve(self, input_data: str) -> int:
        return self.base_solve(input_data)


class Day14PartB(Day14, FileReaderSolution):
    def add_floor(self):
        self.boundaries[2] += 2
        self.boundaries[0] -= 150
        self.boundaries[1] += 100
        for x in range(self.boundaries[0], self.boundaries[1]):
            self.grid[(x, self.boundaries[2])] = "#"

    def solve(self, input_data: str) -> int:
        return self.base_solve(input_data, True)

