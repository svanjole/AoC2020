from utils.abstract import FileReaderSolution
from enum import Enum
from collections import Counter


class Direction(Enum):
    N = (0, -1)
    NE = (1, -1)
    E = (1, 0)
    S = (0, 1)
    W = (-1, 0)
    SE = (1, 1)
    SW = (-1, 1)
    NW = (-1, -1)


class Day23:
    def __init__(self):
        self.grid = {}

        self.all_directions = [
            (Direction.N, [Direction.N, Direction.NE, Direction.NW]),
            (Direction.S, [Direction.S, Direction.SE, Direction.SW]),
            (Direction.W, [Direction.W, Direction.NW, Direction.SW]),
            (Direction.E, [Direction.E, Direction.NE, Direction.SE])
        ]

    def parse(self, input_data):
        lines = input_data.split("\n")
        for y in range(len(lines)):
            line = lines[y]
            for x in range(len(line)):
                if line[x] == "#":
                    self.grid[(x, y)] = '#'

    def get_dimensions(self):
        return tuple(op([x[i] for x in self.grid.keys()]) for i in [0, 1] for op in [min, max])

    def pretty_print(self, padding=5):
        min_x, max_x, min_y, max_y = self.get_dimensions()
        for y in range(min_y-padding, max_y + 1 + padding):
            line = ""
            for x in range(min_x-padding, max_x + 1 + padding):
                line += self.grid[(x, y)] if (x, y) in self.grid.keys() else "."
            print(line)
        print()

    def base_solve(self):
        propositions = {}

        for pos in self.grid.keys():
            has_neighbours = False
            for dy in range(-1, 2):
                for dx in range(-1, 2):
                    if dy == 0 and dx == 0:
                        continue

                    if (pos[0] + dx, pos[1] + dy) in self.grid.keys():
                        has_neighbours = True
                        break

            if not has_neighbours:
                continue

            for i, (proposal, directions) in enumerate(self.all_directions):
                possible = True
                for dir in directions:
                    new_pos = tuple([sum(x) for x in zip(pos, dir.value)])
                    if new_pos in self.grid.keys():
                        possible = False
                        break

                if possible:
                    propositions[pos] = tuple([sum(x) for x in zip(pos, proposal.value)])
                    break

        # if multiple elves suggest same proposition, remove them
        valid_unique_moves = [k for k, v in Counter([v for k, v in propositions.items()]).items() if v == 1]
        valid_moves = [(pos, new_pos) for pos, new_pos in propositions.items() if new_pos in valid_unique_moves]

        # for move in moves, search elf and update pos (remove from grid, add to grid)
        if len(valid_moves) == 0:
            return False

        for move in valid_moves:
            del self.grid[move[0]]
            self.grid[move[1]] = "#"

        self.all_directions.append(self.all_directions.pop(0))

        return True


class Day23PartA(Day23, FileReaderSolution):
    def solve(self, input_data: str) -> int:
        self.parse(input_data)
        #self.pretty_print(2)

        for i in range(10):
            self.base_solve()
            #self.pretty_print(0)

        min_x, max_x, min_y, max_y = self.get_dimensions()

        return (max_x-min_x+1) * (max_y-min_y+1) - len(self.grid)


class Day23PartB(Day23, FileReaderSolution):
    def solve(self, input_data: str) -> int:
        self.parse(input_data)
        #self.pretty_print(2)

        count = 1

        while self.base_solve():
            count += 1
            #self.pretty_print(0)

        return count

