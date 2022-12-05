from utils.abstract import FileReaderSolution
from typing import List


class Day24:
    instructions: List[str]

    def __init__(self):
        self.tiles = {}

    def initialize_grid(self, input_data):
        moves = ["E", "SE", "SW", "W", "NW", "NE"]
        self.tiles = {(0, 0, 0): True}

        for instruction in input_data.splitlines():
            coord = (0, 0, 0)
            pos = 0
            while pos < len(instruction):
                for move in moves:
                    if instruction[pos:pos + len(move)].upper() == move:
                        break

                if move == "E":
                    coord = (coord[0] + 1, coord[1] - 1, coord[2])
                elif move == "SE":
                    coord = (coord[0], coord[1] - 1, coord[2] + 1)
                elif move == "SW":
                    coord = (coord[0] - 1, coord[1], coord[2] + 1)
                elif move == "W":
                    coord = (coord[0] - 1, coord[1] + 1, coord[2])
                elif move == "NW":
                    coord = (coord[0], coord[1] + 1, coord[2] - 1)
                elif move == "NE":
                    coord = (coord[0] + 1, coord[1], coord[2] - 1)

                pos += len(move)

                if coord not in self.tiles:
                    self.tiles[coord] = True

            self.tiles[coord] = not self.tiles[coord]


class Day24PartA(Day24, FileReaderSolution):
    def solve(self, input_data: str) -> int:
        self.initialize_grid(input_data)

        return sum([not x for x in self.tiles.values()])


class Day24PartB(Day24, FileReaderSolution):
    def solve(self, input_data: str) -> int:
        self.initialize_grid(input_data)

        for day in range(100):
            self.tiles = self.new_grid(self.tiles)

        return sum([not x for x in self.tiles.values()])

    def new_grid(self, tiles):
        new_grid = tiles.copy()
        dirs = [
            (1, -1, 0),
            (0, -1, 1),
            (-1, 0, 1),
            (-1, 1, 0),
            (0, 1, -1),
            (1, 0, -1)
        ]

        for coord in tiles:
            black_nb = 0
            for dir in dirs:
                nb_coord = (coord[0]+dir[0], coord[1]+dir[1], coord[2]+dir[2])
                if nb_coord in tiles:
                    if not tiles[nb_coord]:
                        black_nb += 1
                else:
                    black_nb_nb = 0
                    for nb_dir in dirs:
                        nb_nb_coord = (nb_coord[0] + nb_dir[0], nb_coord[1] + nb_dir[1], nb_coord[2] + nb_dir[2])
                        if nb_nb_coord in tiles and not tiles[nb_nb_coord]:
                            black_nb_nb += 1
                    new_grid[nb_coord] = black_nb_nb != 2

            if not tiles[coord]:
                if black_nb == 0 or black_nb > 2:
                    new_grid[coord] = True
            elif tiles[coord] == 1 and black_nb == 2:
                new_grid[coord] = False

        return new_grid
