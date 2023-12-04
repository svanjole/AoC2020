from utils.abstract import FileReaderSolution
import operator
import re


class Day15:
    def __init__(self):
        self.grid = {}
        self.boundaries = [9999999, -9999999, 9999999, -9999999]
        self.sensors = {}
        self.covered = {}

    def parse(self, input_data):
        self.grid = {}
        self.boundaries = [9999999, -9999999, 9999999, -9999999]
        self.sensors = {}
        self.covered = {}

        for line in input_data.split("\n"):
            if line[0] == "#":
                continue
            regex = r"x=([-]?\d*).*?y=([-]?\d*)"
            matches = re.finditer(regex, line, re.MULTILINE)

            for key, match in enumerate(matches):
                x = int(match.groups()[0])
                y = int(match.groups()[1])

                match key:
                    case 0:
                        sensor = (x, y)
                    case 1:
                        beacon = (x, y)

            self.sensors[sensor] = beacon

            if min(sensor[0], beacon[0]) < self.boundaries[0]:
                self.boundaries[0] = min(sensor[0], beacon[0])

            if max(sensor[0], beacon[0]) > self.boundaries[1]:
                self.boundaries[1] = max(sensor[0], beacon[0])

            if min(sensor[1], beacon[1]) < self.boundaries[2]:
                self.boundaries[2] = min(sensor[1], beacon[1])

            if max(sensor[1], beacon[1]) > self.boundaries[3]:
                self.boundaries[3] = max(sensor[1], beacon[1])

            self.grid[sensor] = "S"
            self.grid[beacon] = "B"

    def pretty_print(self):
        for y in range(self.boundaries[2], self.boundaries[3]+1):
            output = ""
            for x in range(self.boundaries[0], self.boundaries[1]+1):
                output += self.grid[(x, y)] if (x, y) in self.grid else "#" if (x,y) in self.covered else "."
            print(output)

    @staticmethod
    def calculate_distance(a, b):
        return sum(abs(val1 - val2) for val1, val2 in zip(a, b))

    def calculate_coverage(self, horizon):
        self.covered = {}
        items = []
        for sensor, beacon in self.sensors.items():
            distance = self.calculate_distance(beacon, sensor)

            max_squares = abs(distance) * 2 + 1
            height_difference = abs(horizon - sensor[1])
            squares_on_horizon = max_squares - ((height_difference) * 2)

            if squares_on_horizon <= 0:
                continue

            offset = sensor[0] - ((squares_on_horizon - 1) // 2)
            items.append((offset, offset+squares_on_horizon-1))

        return items

    @staticmethod
    def find_sections(items, floor=None, ceil=None):
        items = sorted(items, key=lambda x: x[0])
        (min_x, max_x) = items.pop(0)

        if floor is not None and min_x < floor:
            min_x = max(0, min_x)

        for item in items:
            if min_x <= max(0, item[0]) <= max_x:
                if item[1] > max_x:
                    max_x = item[1] if ceil is None else min(ceil, item[1])
            elif item[0] == max_x + 2:
                return True, max_x+1

        return False, max_x-min_x


class Day15PartA(Day15, FileReaderSolution):
    def solve(self, input_data: str) -> int:
        self.parse(input_data)
        items = self.calculate_coverage(2000000)
        has_gap, size = self.find_sections(items)
        print(has_gap, size)
        return size


class Day15PartB(Day15, FileReaderSolution):
    def solve(self, input_data: str) -> int:
        self.parse(input_data)
        for i in range(3429553, 4000000):
            items = self.calculate_coverage(i)
            has_gap, sections = self.find_sections(items, 0, 4000000)
            if has_gap:
                return (4000000 * sections) + i

