from utils.abstract import FileReaderSolution
import operator


class Day07:
    def __init__(self):
        self.system = {"total": 0, "dirs": {}, "files": {}}

    def create_dir(self, current_dir, dir_name):
        pointer = self.system
        for item in current_dir:
            pointer = pointer["dirs"][item]

        if dir_name not in pointer:
            pointer["dirs"][dir_name] = {"total": 0, "dirs": {}, "files": {}}

    def create_file(self, current_dir, file_name, file_size):
        pointer = self.system
        pointer["total"] += file_size

        for item in current_dir:
            pointer = pointer["dirs"][item]
            pointer["total"] += file_size

        pointer["files"][file_name] = file_size

    def parse(self, input_data):
        current_dir = []

        for line in input_data.split("\n"):
            command = line[2:].split(" ") if line[0] == "$" else line.split(" ")
            if command[0] == "ls":
                pass
            elif command[0] == "cd":
                if command[1] == "/":
                    current_dir = []
                    continue
                current_dir.pop() if command[1] == ".." else current_dir.append(command[1])
            elif command[0] == "dir":
                self.create_dir(current_dir, command[1])
            else:
                self.create_file(current_dir, command[1], int(command[0]))

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
