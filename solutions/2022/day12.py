from utils.abstract import FileReaderSolution


class Day12:
    def __init__(self):
        self.grid = {}
        self.start = ()
        self.goal = ()
        self.height = 0
        self.width = 0

    def solve(self, input_data: str) -> int:
        self.parse_input(input_data)
        return self.solve_part()

    def parse_input(self, input_data: str):
        lines = input_data.splitlines()
        self.grid = {}
        self.width = len(lines[0])
        self.height = len(lines)
        for y in range(len(lines)):
            for x in range(len(lines[0])):
                if lines[y][x] == "E":
                    self.goal = (x, y)
                    self.grid[(x, y)] = ord('z') - 97
                elif lines[y][x] == "S":
                    self.start = (x, y)
                    self.grid[(x, y)] = ord('a') - 97
                else:
                    self.grid[(x, y)] = ord(lines[y][x]) - 97

    @staticmethod
    def reconstruct_path(came_from, current):
        total_path = [current]
        while current in came_from.keys():
            current = came_from[current]
            total_path.append(current)

        total_path.reverse()
        return total_path

    def a_star(self, start, goal):
        open_set = [start]
        came_from = {}
        g_score = {start: 0}
        f_score = {start: 0}

        while len(open_set) > 0:
            current = sorted([(node, f_score[node]) for node in open_set], key=lambda t: t[1])[0][0]

            if current == goal:
                return self.reconstruct_path(came_from, current)

            open_set.remove(current)

            for direction in [(1, 0), (-1, 0), (0, 1), (0, -1)]:
                neighbour = (current[0] + direction[0], current[1] + direction[1])
                if not 0 <= neighbour[0] < self.width or not 0 <= neighbour[1] < self.height:
                    continue

                if not (self.grid[neighbour] - self.grid[current]) <= 1:
                    continue

                tentative_g_score = g_score[current] + 1

                if tentative_g_score < g_score.get(neighbour, 9999999999999):
                    came_from[neighbour] = current
                    g_score[neighbour] = tentative_g_score
                    f_score[neighbour] = tentative_g_score + self.manhattan_distance(current, self.goal)

                    if neighbour not in open_set:
                        open_set.append(neighbour)

        raise Exception("Could not find path")

    @staticmethod
    def manhattan_distance(start, end):
        return sum(abs(val1 - val2) for val1, val2 in zip(start, end))


class Day12PartA(Day12, FileReaderSolution):
    def solve_part(self) -> int:
        path = self.a_star(self.start, self.goal)
        return len(path) - 1


class Day12PartB(Day12, FileReaderSolution):
    def solve_part(self) -> int:
        positions = [start_pos for (start_pos, value) in self.grid.items() if value == 0]

        lengths = []
        for position in positions:
            try:
                path = self.a_star(position, self.goal)
                lengths.append(len(path) - 1)
            except:
                pass

        return min(lengths)
