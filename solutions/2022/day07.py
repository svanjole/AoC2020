from utils.abstract import FileReaderSolution
import operator


class Day07:
    def __init__(self):
        self.system = {"total": 0, "dirs": {}, "files": {}}

    @staticmethod
    def traverse_and_update_dir(pointer, path, file_size=0):
        pointer["total"] += file_size
        for item in path:
            pointer = pointer["dirs"][item]
            pointer["total"] += file_size

        return pointer

    def create(self, path, object_type, object_name, file_size=0):
        empty_dir = {"total": 0, "dirs": {}, "files": {}}
        pointer = self.traverse_and_update_dir(self.system, path, file_size)
        pointer[object_type][object_name] = empty_dir if object_type == "dirs" else file_size

    def parse(self, input_data):
        path = []

        for line in input_data.split("\n"):
            command = line[2:].split(" ") if line[0] == "$" else line.split(" ")
            match command[0]:
                case "cd":
                    if command[1] == "/":
                        path = []
                        continue
                    path.pop() if command[1] == ".." else path.append(command[1])
                case "dir":
                    self.create(path, "dirs", command[1])
                case "ls":
                    pass
                case _:
                    self.create(path, "files", command[1], int(command[0]))

    def find_candidates(self, candidates, pointer, size, relate=operator.le):
        if relate(pointer["total"], size):
            candidates.append(pointer["total"])

        for dir_name in pointer["dirs"]:
            self.find_candidates(candidates, pointer["dirs"][dir_name], size, relate)

        return candidates


class Day07PartA(Day07, FileReaderSolution):
    def solve(self, input_data: str) -> int:
        self.parse(input_data)
        return sum(self.find_candidates([], self.system, 100000))


class Day07PartB(Day07, FileReaderSolution):
    def solve(self, input_data: str) -> int:
        self.parse(input_data)
        return min(self.find_candidates([], self.system, 30000000 - (70000000 - self.system["total"]), operator.ge))
