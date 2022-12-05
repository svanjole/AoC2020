from utils.abstract import FileReaderSolution
from abc import abstractmethod
from enum import Enum
from itertools import product

class Day21:
    def __init__(self):
        self.startpos = []

    @abstractmethod
    def solve_part(self):
        pass

    def solve(self, input_data: str) -> int:
        self.parse_input(input_data)

        return self.solve_part()

    def parse_input(self, input_data: str):
        for line in input_data.splitlines():
            self.startpos.append(int(line.split(": ")[1]))


    def common_solver(self):
        pass


class Day21PartA(Day21, FileReaderSolution):
    def solve_part(self) -> int:
        current_player = 0
        die_value = 1
        scores = [0, 0]
        rolls = 0

        while scores[0] < 1000 and scores[1] < 1000:
            total = 0
            for _ in range(3):
                total += die_value
                die_value += 1
                if die_value > 100:
                    die_value = 1
            rolls += 3

            self.startpos[current_player] += total
            while self.startpos[current_player] > 10:
                self.startpos[current_player] -= 10

            scores[current_player] += self.startpos[current_player]


            current_player = 1 - current_player

        print(scores, rolls)

        return min(scores) * rolls


class Day21PartB(Day21, FileReaderSolution):
    def solve_part(self) -> int:
        scores = [0, 0]
        pos = self.startpos
        current_player = 0
        wins = self.play_driac(pos[0], pos[1], scores[0], scores[1], current_player)
        return max(wins)

    def play_driac(self, p1, p2, s1=0, s2=0, player=0, cache={}):

        if (p1, p2, s1, s2, player) in cache:
            return cache[(p1, p2, s1, s2, player)]

        wins = [0, 0]
        rolls = [r1 + r2 + r3 for r1, r2, r3 in product([1, 2, 3], repeat=3)]

        for r in rolls:
            pos = [p1, p2]
            score = [s1, s2]

            pos[player] = (pos[player] + r - 1) % 10 + 1
            score[player] += pos[player]

            if score[player] >= 21:
                wins[player] += 1
            else:
                w1, w2 = self.play_driac(
                    pos[0], pos[1], score[0], score[1], 1 if player == 0 else 0
                )

                wins[0] += w1
                wins[1] += w2

        cache[(p1, p2, s1, s2, player)] = wins
        return wins