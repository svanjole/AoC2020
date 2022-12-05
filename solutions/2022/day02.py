from utils.abstract import FileReaderSolution


class Day02:
    moves = {
        "A": 0, "B": 1, "C": 2,
        "X": 0, "Y": 1, "Z": 2
    }

    @staticmethod
    def evaluate(opponent, player):
        if opponent == player:
            return 3 + player + 1

        if (opponent + 1) % 3 == player:
            return 6 + player + 1

        return player + 1


class Day02PartA(Day02, FileReaderSolution):
    def solve(self, input_data: str) -> int:
        score = 0

        for line in input_data.split("\n"):
            moves = list(map(lambda x: self.moves[x], line.split(" ")))
            score += self.evaluate(moves[0], moves[1])

        return score


class Day02PartB(Day02, FileReaderSolution):
    def solve(self, input_data: str) -> int:
        score = 0

        for line in input_data.split("\n"):
            moves = list(map(lambda x: self.moves[x], line.split(" ")))

            if moves[1] == 0:
                move = (moves[0] - 1 + 3) % 3
            elif moves[1] == 1:
                move = moves[0]
            else:
                move = (moves[0] + 1) % 3

            score += self.evaluate(moves[0], move)

        return score
