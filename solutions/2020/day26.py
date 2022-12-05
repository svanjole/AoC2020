from utils.abstract import FileReaderSolution
from typing import List


class Day26:

    def __init__(self):
        pass


class Day26PartA(Day26, FileReaderSolution):
    def solve(self, input_data: str) -> int:
        alpha = "ABCDEFGHIJKLMNOPQRSTUVWXYZ "
        a = "DIT IS EEN VOORBEELD VAN NOABERSCHOP"
        b = "EHVZHSAHCN VOOS FDLCYWZQXMNZFBQPBILR"

        for i in range(len(a)):
            diff = (alpha.find(b[i])-alpha.find(a[i]))
            print(diff)

class Day26PartB(Day26, FileReaderSolution):
    def solve(self, input_data: str) -> int:
        return 0