from utils.abstract import FileReaderSolution
from abc import abstractmethod


class Point:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    @staticmethod
    def create_from_string(input: str):
        coords = input.split(",")
        return Point(int(coords[0]), int(coords[1]))

    def __str__(self):
        return f"({self.x}:{self.y})"

    def __repr__(self):
        return self.__str__()

class Line:
    start: Point
    end: Point

    def __init__(self, start: Point, end: Point):
        self.start = start
        self.end = end

    def get_all_points(self):
        points = []

        minx = min(self.start.x, self.end.x)
        maxx = max(self.start.x, self.end.x)
        miny = min(self.start.y, self.end.y)
        maxy = max(self.start.y, self.end.y)

        if self.start.x == self.end.x:
            dx = 0
        elif self.start.x > self.end.x:
            dx = -1
        else:
            dx = 1

        if self.start.y == self.end.y:
            dy = 0
        elif self.start.y > self.end.y:
            dy = -1
        else:
            dy = 1

        length = max(maxx-minx, maxy-miny)

        for step in range(0,length+1):
            points.append(Point(self.start.x + step*dx, self.start.y + step*dy))

        return points

    @staticmethod
    def create_from_string(input: str):
        coords = input.split(" -> ")
        return Line(
            Point.create_from_string(coords[0]),
            Point.create_from_string(coords[1])
        )

    def is_straight(self):
        return self.start.x == self.end.x or self.start.y == self.end.y

    def __str__(self):
        return f"{self.start} - {self.end} {self.is_straight()}"

    def __repr__(self):
        return self.__str__()


class Day05:
    def __init__(self):
        self.lines = []

    @abstractmethod
    def solve_part(self):
        pass

    def solve(self, input_data: str) -> int:
        self.parse_input(input_data)
        return self.solve_part()

    def parse_input(self, input_data: str):
        lines = input_data.splitlines()
        for line in lines:
            self.lines.append(Line.create_from_string(line))


class Day05PartA(Day05, FileReaderSolution):
    def solve_part(self) -> int:
        count = {}
        for line in self.lines:
            if not line.is_straight():
                continue

            points = line.get_all_points()

            for point in points:
                key = f"{point}"
                if key in count.keys():
                    count[key] += 1
                else:
                    count[key] = 1

        return sum(1 for value in count.values() if value > 1)


class Day05PartB(Day05, FileReaderSolution):
    def solve_part(self) -> int:
        count = {}
        for line in self.lines:

            points = line.get_all_points()
            for point in points:
                key = f"{point}"
                if key in count.keys():
                    count[key] += 1
                else:
                    count[key] = 1

        return sum(1 for value in count.values() if value > 1)