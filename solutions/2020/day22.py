from utils.abstract import FileReaderSolution
from typing import List


class Day22:

    def __init__(self):
        self.tiles = {}



class Day22PartA(Day22, FileReaderSolution):
    def solve(self, input_data: str) -> int:
        players = input_data.split("\n\n")

        player_one = [int(x) for x in players[0].splitlines()[1:]]
        player_two = [int(x) for x in players[1].splitlines()[1:]]
        #print(player_one)
        #print(player_two)
        rounds = 0

        while len(player_one) > 0 and len(player_two) > 0:
            card_one = player_one[0:1][0]
            card_two = player_two[0:1][0]
            #print(card_one, card_two)
            player_one.remove(card_one)
            player_two.remove(card_two)
            if card_one > card_two:
                player_one.append(card_one)
                player_one.append(card_two)
            else:
                player_two.append(card_two)
                player_two.append(card_one)

            rounds += 1

        if len(player_one) > 0:
            return self.calculate_score(player_one)
        else:
            return self.calculate_score(player_two)

    def calculate_score(self, cards):
        total = 0
        multiplier = len(cards)
        for i in cards:
            total += multiplier * i
            multiplier -= 1
        return total



class Day22PartB(Day22, FileReaderSolution):
    def solve(self, input_data: str) -> int:
        return 0
