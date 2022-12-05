from utils.abstract import FileReaderSolution
from typing import Dict, List
from enum import Enum
import math


class Day23:
    cups: List[int]

    def parse_input(self, input_data: str):
        self.cups = [int(x) for x in input_data]


class Day23PartA(Day23, FileReaderSolution):
    def solve(self, input_data: str) -> int:
        self.parse_input(input_data)
        moves = 2

        current_cup_index = 0
        current_cup = self.cups[0]

        for i in range(moves):
            print(self.cups)
            cups = self.cups[current_cup_index+1:current_cup_index+4]
            #for x in cups:
            #    self.cups.remove(x)

            print(cups)

            destination_index = self.cups.index(current_cup-1)+1
            print(destination_index)

            self.cups = self.cups[0:current_cup_index+2] + cups + self.cups[destination_index:]
            current_cup_index += 1 % len(self.cups)
        return 0

class Day23PartB(Day23, FileReaderSolution):
    def solve(self, input_data: str) -> int:
        self.parse_input(input_data)

        return 0