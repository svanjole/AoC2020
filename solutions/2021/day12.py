from utils.abstract import FileReaderSolution
from abc import abstractmethod
from enum import Enum
from anytree import Node, RenderTree


class Node:
    def __init__(self, letter):
        self.letter = letter
        self.is_large = letter.isupper()
        self.is_start = letter == "start"
        self.is_end = letter == "end"
        self.neighbours = {}

    def add_neighbour(self, neighbour: Node):
        if neighbour.letter not in self.neighbours.keys():
            self.neighbours[neighbour.letter] = neighbour

    def __str__(self):
        output = f"Node: {self.letter}"
        for nb in self.neighbours.keys():
            output += f"\n\t{nb}"

        output += "\n\n"
        return output

    def __repr__(self):
        return str(self)


class Day12:
    def __init__(self):
        self.lines = []
        self.nodes = {}

    @abstractmethod
    def solve_part(self, median):
        pass

    def createOrUpdateNode(self, node_a, node_b):
        if node_a not in self.nodes.keys():
            self.nodes[node_a] = Node(node_a)

        if node_b not in self.nodes.keys():
            self.nodes[node_b] = Node(node_b)

        self.nodes[node_a].add_neighbour(self.nodes[node_b])
        self.nodes[node_b].add_neighbour(self.nodes[node_a])

    def solve(self, input_data: str) -> int:
        self.parse_input(input_data)

        return self.solve_part()

    def parse_input(self, input_data: str):
        lines = input_data.splitlines()
        for connection in lines:
            parts = connection.split("-")
            self.createOrUpdateNode(parts[0], parts[1])

    def common_solver(self):
        pass


class Day12PartA(Day12, FileReaderSolution):

    def find_paths(self, current: Node, target: Node, path: [], visited: [], found_paths: []):

        path.append(current.letter)

        if not current.is_large:
            visited[current.letter] = True

        if current.letter == target.letter:
            found_paths.append(path.copy())
        else:
            for nb in current.neighbours.keys():
                if not visited[nb]:
                    self.find_paths(current.neighbours[nb], target, path, visited, found_paths)

        path.pop()
        visited[current.letter] = False

    def solve_part(self) -> int:
        paths = []
        visited = dict(zip(self.nodes.keys(), [False] * len(self.nodes)))
        self.find_paths(self.nodes["start"], self.nodes["end"], [], visited, paths)
        return len(paths)


class Day12PartB(Day12, FileReaderSolution):
    def find_paths(self, current: Node, target: Node, path: [], visited: [], found_paths: []):

        path.append(current.letter)
        visited[current.letter] += 1

        if current.letter == target.letter:
            found_paths.append(path.copy())
        else:
            for nb in current.neighbours.keys():
                neighbour = current.neighbours[nb]
                if neighbour.is_start:
                    continue

                if not neighbour.is_large:
                    another_small_cave_exhausted = False
                    # check if a small cave exists that has been visited twice
                    for key in visited.keys():
                        if not self.nodes[key].is_large and nb != key:
                            if visited[key] == 2:
                                another_small_cave_exhausted = True
                                break

                    if visited[nb] == 2 or (another_small_cave_exhausted and visited[nb] == 1):
                        continue

                self.find_paths(neighbour, target, path, visited, found_paths)

        path.pop()
        visited[current.letter] -= 1

    def solve_part(self) -> int:
        paths = []
        visited = dict(zip(self.nodes.keys(), [0] * len(self.nodes)))

        self.find_paths(self.nodes["start"], self.nodes["end"], [], visited, paths)
        return len(paths)

