from utils.abstract import FileReaderSolution
from abc import abstractmethod


class Day15:
    def __init__(self):
        self.grid = []
        self.goal = ()

    @abstractmethod
    def solve_part(self):
        pass

    def solve(self, input_data: str) -> int:
        self.parse_input(input_data)

        return self.solve_part()

    def parse_input(self, input_data: str):
        lines = input_data.splitlines()
        self.grid = {}
        for y in range(len(lines)):
            for x in range(len(lines[0])):
                self.grid[(x,y)] = int(lines[y][x])

        self.goal = (x, y)

    @staticmethod
    def find_lowest_f_score(open_set, f_score):
        lowest = 99999999999999
        lowest_node = ()
        for node in open_set:
            if f_score[node] < lowest:
                lowest_node = node
                lowest = f_score[node]

        return lowest_node

    @staticmethod
    def reconstruct_path(came_from, current):
        total_path = [current]
        while current in came_from.keys():
            current = came_from[current]
            total_path.append(current)

        total_path.reverse()
        return total_path

    def a_star(self, start, goal, h):
        dirs = [(1, 0), (-1, 0), (0, 1), (0, -1)]
        open_set = [start]
        came_from = {}
        g_score = {start: 0}
        f_score = {start: h(start)}

        while len(open_set) > 0:
            current = self.find_lowest_f_score(open_set, f_score)

            if current == goal:
                return self.reconstruct_path(came_from, current)

            open_set.remove(current)

            for direction in dirs:
                dx = current[0] + direction[0]
                dy = current[1] + direction[1]

                if dx < 0 or dx > self.goal[0]:
                    continue
                if dy < 0 or dy > self.goal[1]:
                    continue

                neighbour = (dx, dy)
                tentative_g_score = g_score[current] + h(neighbour)

                if tentative_g_score < g_score.get(neighbour, 9999999999999):
                    came_from[neighbour] = current
                    g_score[neighbour] = tentative_g_score
                    f_score[neighbour] = tentative_g_score + self.manhattan_distance(current, neighbour)

                    if neighbour not in open_set:
                        open_set.append(neighbour)
        return False

    def heuristic(self, pos):
        return self.grid[pos]

    @staticmethod
    def manhattan_distance(start, end):
        return sum(abs(val1 - val2) for val1, val2 in zip(start, end))

    def common_solver(self):
        path = self.a_star((0, 0), self.goal, self.heuristic)
        if not path:
            raise Exception("Could not find path")

        total_cost = 0
        for c in path:
            total_cost += self.grid[c]

        return total_cost - self.grid[(0, 0)]


class Day15PartA(Day15, FileReaderSolution):
    def solve_part(self) -> int:
        return self.common_solver()


class Day15PartB(Day15, FileReaderSolution):
    def solve_part(self) -> int:
        grid = {}
        width = self.goal[0] + 1
        height = self.goal[1] + 1

        for dy in range(5):
            for dx in range(5):
                for y in range(height):
                    for x in range(width):
                        coord = (x + dx*width, y + dy*height)
                        grid[coord] = ((self.grid[(x, y)] + dy + dx - 1) % 9) + 1

        self.grid = grid
        f = open("E:/grid.txt", "a")
        for y in range(height*5):
            line = ""
            for x in range(width*5):
                line += f"{grid[(x,y)]}"
            f.write(line + "\n")
        f.close()

        self.goal = (width * 5 - 1, height * 5 - 1)
        return self.common_solver()

