from utils.abstract import FileReaderSolution
from typing import Dict, List
from enum import Enum
import math


class TileType(Enum):
    Corner = 1
    Edge = 2
    Regular = 3


class Edge(Enum):
    Top = 1
    Right = 2
    Bottom = 3
    Left = 4


class Tile:
    tile_id: int
    data: List[List[str]]
    tile_type: TileType
    is_used: bool

    def count_character(self, character):
        return sum([sum(cell == character for cell in row) for row in self.data])

    def count_occurrences(self, pattern):
        pattern_height = len(pattern.data)
        pattern_width = len(pattern.data[0])
        height = len(self.data)
        width = len(self.data[0])
        count = 0
        for y in range(0, height-pattern_height):
            for x in range(0, width - pattern_width):
                found = True
                for py in range(pattern_height):
                    for px in range(pattern_width):
                        if pattern.data[py][px] == '#' and pattern.data[py][px] != self.data[y+py][x+px]:
                            found = False

                if found:
                    count += 1

        return count

    def find_pattern(self, pattern):
        tries = 0

        while tries < 12:
            count = self.count_occurrences(pattern)

            if count > 0:
                return count

            self.rotate()

            if tries == 3:
                self.flip('h')

            if tries == 7:
                self.flip('h')
                self.flip('v')

            if tries == 11:
                self.flip('v')
                break

            tries += 1

        return 0

    def __str__(self):
        result = str(self.tile_id)
        result += "\n"

        for row in self.data:
            result += ''.join(row) + "\n"

        return result

    def strip_border(self):
        return [''.join(row[1:-1]) for row in self.data[1:-1]]

    def get_edge(self, edge: Edge):

        if edge == Edge.Top:
            result = self.data[0]
        elif edge == Edge.Right:
            result = [row[len(self.data)-1] for row in self.data]
        elif edge == Edge.Bottom:
            result = self.data[len(self.data)-1]
        elif edge == Edge.Left:
            result = [row[0] for row in self.data]
        else:
            raise ValueError("Unknown edge")

        return ''.join(result)

    def __init__(self, tile_id, data):
        self.tile_id = tile_id
        self.data = data
        self.is_used = False

    def get_edges(self) -> List[str]:
        edges = []

        edges.append(self.get_edge(Edge.Top))
        edges.append(self.get_edge(Edge.Right))
        edges.append(self.get_edge(Edge.Bottom))
        edges.append(self.get_edge(Edge.Left))

        self.flip('h')
        edges.append(self.get_edge(Edge.Top))
        edges.append(self.get_edge(Edge.Right))
        edges.append(self.get_edge(Edge.Bottom))
        edges.append(self.get_edge(Edge.Left))
        self.flip('h')

        self.flip('v')
        edges.append(self.get_edge(Edge.Top))
        edges.append(self.get_edge(Edge.Right))
        edges.append(self.get_edge(Edge.Bottom))
        edges.append(self.get_edge(Edge.Left))
        self.flip('v')

        return edges

    def rotate(self):
        rotated = zip(*self.data[::-1])
        self.data = [list(elem) for elem in rotated]

    def flip(self, mode):
        flipped = self.data.copy()
        if mode == 'v':
            for i in range(0, len(flipped), 1):
                flipped[i].reverse()
        elif mode == 'h':
            flipped.reverse()
        self.data = flipped

    @staticmethod
    def parse_data(data):
        lines = data.splitlines()
        tile_id = int(lines[0].split(" ")[1].strip(":"))
        grid = []

        for y in range(0, len(lines)-1):
            grid.append([])
            for x in range(0, len(lines[y+1])):
                grid[y].append(lines[y+1][x])

        return Tile(tile_id, grid)


class Day20:
    edge_data: Dict[str, List[int]]
    tiles = Dict[int, Tile]

    def __init__(self):
        self.edge_data = {}
        self.tiles = {}

    def parse_input(self, input_data: str):
        for tile_data in input_data.split("\n\n"):
            tile = Tile.parse_data(tile_data)
            self.tiles[tile.tile_id] = tile
            edges = tile.get_edges()

            for edge in edges:
                if edge not in self.edge_data.keys():
                    self.edge_data[edge] = []

                self.edge_data[edge].append(tile.tile_id)

    def create_tiles(self, input_data: str):
        self.parse_input(input_data)

        for tile in self.tiles.values():
            neighbours = 0
            for edge in self.edge_data:
                if tile.tile_id in self.edge_data[edge] and len(self.edge_data[edge]) > 1:
                    neighbours += 1

            if neighbours == 6:
                tile.tile_type = TileType.Corner
            elif neighbours == 7:
                tile.tile_type = TileType.Edge
            else:
                tile.tile_type = TileType.Regular


class Day20PartA(Day20, FileReaderSolution):
    def solve(self, input_data: str) -> int:
        self.create_tiles(input_data)

        return math.prod([x.tile_id if x.tile_type == TileType.Corner else 1 for x in self.tiles.values()])


class Day20PartB(Day20, FileReaderSolution):

    def get_unused_pieces(self):
        return list(filter(lambda x: not x.is_used, self.tiles.values()))

    def orient_top_left_tile(self, corner_piece) -> Tile:
        top_edge = corner_piece.get_edge(Edge.Top)
        left_edge = corner_piece.get_edge(Edge.Left)
        # check if both edges do not occur in edge lists

        keys = self.edge_data.keys()
        tries = 0

        while top_edge in keys or left_edge in keys:

            corner_piece.rotate()

            if tries == 3:
                corner_piece.flip('h')

            if tries == 7:
                corner_piece.flip('h')
                corner_piece.flip('v')

            if tries == 11:
                corner_piece.flip('v')
                break

            tries += 1

            top_edge = corner_piece.get_edge(Edge.Top)
            left_edge = corner_piece.get_edge(Edge.Left)

        return corner_piece

    def mark_as_used(self, tile: Tile):
        tile.is_used = True
        for key in list(self.edge_data.keys()):
            if tile.tile_id in self.edge_data[key]:
                self.edge_data[key] = list(filter(lambda x: x != tile.tile_id, self.edge_data[key]))
                if len(self.edge_data[key]) == 0:
                    del self.edge_data[key]

    def solve_puzzle(self):
        corner_piece = list(filter(lambda x: x.tile_type == TileType.Corner, self.tiles.values()))[0]

        self.mark_as_used(corner_piece)
        corner_piece.flip('h')
        corner_piece = self.orient_top_left_tile(corner_piece)

        size = int(math.sqrt(len(self.tiles)))

        puzzle_grid = [[0 for y in range(size)] for x in range(size)]
        puzzle_grid[0][0] = corner_piece.tile_id

        while any(0 in row for row in puzzle_grid):
            for y in range(size):
                for x in range(size):
                    if puzzle_grid[y][x] == 0:
                        edges = {}
                        left_piece = puzzle_grid[y][x - 1] if x > 0 else None
                        right_piece = puzzle_grid[y][x + 1] if x < size - 1 else None
                        top_piece = puzzle_grid[y - 1][x] if y > 0 else None
                        bottom_piece = puzzle_grid[y + 1][x] if y < size - 1 else None

                        if left_piece:
                            edges[Edge.Left] = self.tiles[left_piece].get_edge(Edge.Right)

                        if right_piece:
                            edges[Edge.Right] = self.tiles[right_piece].get_edge(Edge.Left)

                        if top_piece:
                            edges[Edge.Top] = self.tiles[top_piece].get_edge(Edge.Bottom)

                        if bottom_piece:
                            edges[Edge.Bottom] = self.tiles[bottom_piece].get_edge(Edge.Top)

                        piece = self.find_possible_fit(edges)

                        if piece:
                            self.mark_as_used(piece)
                            puzzle_grid[y][x] = piece.tile_id

        return puzzle_grid

    def assemble_image(self, puzzle_grid):
        image = []
        size = len(puzzle_grid)
        for y in range(size):
            image.append([])
            for x in range(size):
                tile = self.tiles[puzzle_grid[y][x]]
                stripped_tile = Tile(tile.tile_id, tile.strip_border())
                image[y].append(stripped_tile)

        result = ""

        for cell_y in range(size):
            for y in range(len(image[0][0].data)):
                for cell_x in range(size):
                    for x in range(len(image[0][0].data)):
                        result += image[cell_y][cell_x].data[y][x]
                result += "\n"

        return result

    def solve(self, input_data: str) -> int:
        self.create_tiles(input_data)

        puzzle_grid = self.solve_puzzle()
        new_grid = Tile.parse_data("Tile 1:\n" + self.assemble_image(puzzle_grid))

        pattern_tile = Tile.parse_data("Tile 2:\n" + "                  # \n#    ##    ##    ###\n #  #  #  #  #  #   ")

        total_cells = new_grid.count_character('#')
        occurrences = new_grid.find_pattern(pattern_tile)

        return total_cells - (occurrences * pattern_tile.count_character('#'))

    def find_possible_fit(self, edge_constraints: Dict[Edge, str]):
        for tile in self.tiles.values():
            if tile.is_used:
                continue

            tries = 0

            while True:
                all_constraints_valid = True
                for (edge, value) in edge_constraints.items():
                    if tile.get_edge(edge) != value:
                        all_constraints_valid = False

                if all_constraints_valid:
                    return tile

                tile.rotate()

                if tries == 3:
                    tile.flip('h')

                if tries == 7:
                    tile.flip('h')
                    tile.flip('v')

                if tries == 11:
                    tile.flip('v')
                    break

                tries += 1

        return None
