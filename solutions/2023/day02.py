from utils.abstract import FileReaderSolution
from functools import reduce
import operator


class Day02:
    @staticmethod
    def parse(input_data: str) -> str:
        sets = []

        info = input_data.split(": ")
        gamesets = info[1].split("; ")

        for set in gamesets:
            cubes = set.split(", ")
            myset = {
                "red": 0,
                "green": 0,
                "blue": 0
            }
            for cube in cubes:
                cubeinfo = cube.split(" ")
                amount = int(cubeinfo[0])
                color = cubeinfo[1]
                myset[color] = amount
            sets.append(myset)

        return {
            "id": int(info[0].split(" ")[1]),
            "sets": sets
        }
    pass


class Day02PartA(Day02, FileReaderSolution):
    def solve(self, input_data: str) -> int:
        amounts = {
            "red": 12,
            "green": 13,
            "blue": 14
        }

        total = 0

        for line in input_data.split("\n"):
            game = self.parse(line)

            possible = True
            for set in game["sets"]:
                for color in amounts.keys():
                    if set[color] > amounts[color]:
                        possible = False
                        break

            if possible:
                total += game["id"]

        return total


class Day02PartB(Day02, FileReaderSolution):
    def solve(self, input_data: str) -> int:
        total = 0

        for line in input_data.split("\n"):
            amounts = {
                "red": 0,
                "green": 0,
                "blue": 0
            }

            game = self.parse(line)

            for gameset in game["sets"]:
                for color in amounts.keys():
                    amounts[color] = max(amounts[color], gameset[color])

            total += reduce(operator.mul, list(amounts.values()), 1)

        return total
