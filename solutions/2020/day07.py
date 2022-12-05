from utils.abstract import FileReaderSolution
import re


class Bag:
    parents: list
    children: dict
    color: str

    def __init__(self, color):
        self.color = color
        self.parents = []
        self.children = {}

    def contains_bag(self, color):
        for child in self.children.keys():
            if child.color == color:
                return True
            if child.contains_bag(color):
                return True

        return False

    def count_bags(self):
        bags_inside = 0

        for(child, amount) in self.children.items():
            bags_inside += amount + amount * child.count_bags()

        return bags_inside

    def add_parent(self, parent):
        self.parents.append(parent)

    def add_child(self, child, amount):
        self.children[child] = amount

    def __str__(self):
        return self.color


class Day07:
    nodes = {}

    def create_graph(self, rules):
        for rule in rules:
            (color, children) = rule.split(" bags contain ")

            if color not in self.nodes.keys():
                self.nodes[color] = Bag(color)

            parent = self.nodes[color]

            if children == 'no other bags.':
                continue

            for child in children.split(","):
                result = re.match(r"^(\d*) ([a-z ]*) bag(?:[s.]*)?$", child.strip())

                assert result

                amount = int(result[1])
                color = result[2]

                if color not in self.nodes.keys():
                    self.nodes[color] = Bag(color)

                child_node = self.nodes[color]
                child_node.add_parent(parent)
                parent.add_child(child_node, amount)


class Day07PartA(Day07, FileReaderSolution):
    def solve(self, input_data: str) -> int:
        self.create_graph(input_data.split("\n"))

        return sum(map(lambda x: x.contains_bag("shiny gold"), self.nodes.values()))


class Day07PartB(Day07, FileReaderSolution):

    def solve(self, input_data: str) -> int:
        self.create_graph(input_data.split("\n"))

        return self.nodes["shiny gold"].count_bags()
