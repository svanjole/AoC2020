from utils.abstract import FileReaderSolution
import operator


class Day07:
    system: {} = {"total": 0, "dirs": {}, "files": {}}

    @staticmethod
    def traverse_dir_and_update_totals(ptr, path, file_size=0):
        ptr["total"] += file_size
        for item in path:
            ptr = ptr["dirs"][item]
            ptr["total"] += file_size

        return ptr

    def create(self, path, type, name, file_size=0):
        ptr = self.traverse_dir_and_update_totals(self.system, path, file_size)
        ptr[type][name] = {"total": 0, "dirs": {}, "files": {}} if type == "dirs" else file_size

    def parse(self, input_data):
        path = []

        for line in input_data.split("\n"):
            command = line[2:].split(" ") if line[0] == "$" else line.split(" ")
            match command[0]:
                case "ls":
                    pass
                case "cd":
                    path.pop() if command[1] == ".." else path.append(command[1])
                case "dir":
                    self.create(path, "dirs", command[1])
                case _:
                    self.create(path, "files", command[1], int(command[0]))

    def find_candidates(self, candidates, ptr, size, relate=operator.le):
        if relate(ptr["total"], size):
            candidates.append(ptr["total"])

        for dir_name in ptr["dirs"]:
            self.find_candidates(candidates, ptr["dirs"][dir_name], size, relate)

        return candidates


class Day07PartA(Day07, FileReaderSolution):
    def solve(self, input_data: str) -> int:
        self.parse(input_data)
        return sum(self.find_candidates([], self.system, 100000))


class Day07PartB(Day07, FileReaderSolution):
    def solve(self, input_data: str) -> int:
        self.parse(input_data)
        return min(self.find_candidates([], self.system, 30000000 - (70000000 - self.system["total"]), operator.ge))
