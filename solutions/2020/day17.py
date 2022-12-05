from utils.abstract import FileReaderSolution
import numpy as np


class Day17:
    grid: np.array
    depth: int
    width: int
    height: int
    hyper: int

    def next_iteration(self):
        raise NotImplementedError

    def initialize_grid(self, state):
        lines = state.splitlines()

        self.width = len(lines[0])
        self.height = len(lines)
        self.depth = 1
        self.hyper = 1

        self.grid = np.zeros((self.hyper, self.depth, self.height, self.width))

        for y, row in enumerate(state.splitlines()):
            for x in range(0, len(row)):
                self.grid[0][0][y][x] = 1 if row[x] == '#' else 0

    @staticmethod
    def apply_rules(grid, x, y, z, w, nb):
        if grid[w][z][y][x] == 1:
            if not (nb == 2 or nb == 3):
                return 0
        else:
            if nb == 3:
                return 1

        return grid[w][z][y][x]

    def count_neighbours(self, grid, x, y, z, w):
        count = 0
        for dw in range(-1, 2):
            for dz in range(-1, 2):
                for dy in range(-1, 2):
                    for dx in range(-1, 2):

                        if x + dx < 0 or x + dx >= self.width:
                            continue

                        if y + dy < 0 or y + dy >= self.height:
                            continue

                        if z + dz < 0 or z + dz >= self.depth:
                            continue

                        if w + dw < 0 or w + dw >= self.hyper:
                            continue

                        if dw == dz == dy == dx == 0:
                            continue

                        count += grid[w + dw][z + dz][y + dy][x + dx]

        return count

    def prepare_next_generation(self):
        self.grid = np.pad(self.grid, 1)
        self.hyper += 2
        self.width += 2
        self.height += 2
        self.depth += 2

        return self.grid.copy()

    def apply_next_iteration(self, w, new_state):
        for z in range(0, self.depth):
            for y in range(0, self.height):
                for x in range(0, self.width):
                    nb = self.count_neighbours(self.grid, x, y, z, w)
                    new_cell_state = self.apply_rules(new_state, x, y, z, w, nb)
                    new_state[w][z][y][x] = new_cell_state

        return new_state

    def solve(self, input_data: str) -> int:
        self.initialize_grid(input_data)
        max_iterations = 6

        for i in range(0, max_iterations):
            self.grid = self.next_iteration()

        return int(np.sum(self.grid))


class Day17PartA(Day17, FileReaderSolution):
    def next_iteration(self):
        new_state = self.prepare_next_generation()

        w = self.hyper // 2

        return self.apply_next_iteration(w, new_state)


class Day17PartB(Day17, FileReaderSolution):
    def next_iteration(self):
        new_state = self.prepare_next_generation()

        for w in range(0, self.hyper):
            new_state = self.apply_next_iteration(w, new_state)

        return new_state
