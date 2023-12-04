from utils.abstract import FileReaderSolution


class Day03:
    pass


class Day03PartA(Day03, FileReaderSolution):
    def solve(self, input_data: str) -> int:
        grid = input_data.splitlines()
        numbers = []

        for y in range(len(grid)):
            parseState = "scan"
            isPartNumber = False

            for x in range(len(grid[0])):
                if grid[y][x].isnumeric():
                    if parseState == "scan":
                        number = 0
                        parseState = "construct"
                        isPartNumber = False

                    number *= 10
                    number += int(grid[y][x])
                    if not isPartNumber:
                        # scan neighbours
                        for dy in range(-1, 2):
                            for dx in range(-1, 2):
                                if y+dy < 0 or y + dy >= len(grid):
                                    continue

                                if x + dx < 0 or x + dx >= len(grid[0]):
                                    continue
                                neighbour = grid[y+dy][x+dx]
                                if not neighbour.isnumeric() and neighbour != ".":
                                    isPartNumber = True

                else:
                    if parseState == "construct":
                        parseState = "scan"
                        numbers.append((number, isPartNumber))

            #end of line, add number if still constructing
            if parseState == "construct":
                numbers.append((number, isPartNumber))

        return sum(value for value, isPartNumber in numbers if isPartNumber)


class Day03PartB(Day03, FileReaderSolution):
    grid = []

    def find_numbers(self, x, y):
        numbers = []
        evaluated = set()

        for dy in range(-1, 2):
            if y + dy < 0 or y + dy >= len(self.grid):
                continue

            for dx in range(-1, 2):
                if x+dx < 0 or x + dx >= len(self.grid[0]):
                    continue

                # found number, find starting x and start constructing number until "." or EOL
                if self.grid[y+dy][x+dx].isnumeric() and (y+dy, x+dx) not in evaluated:
                    nx = x
                    while self.grid[y+dy][nx+dx].isnumeric():
                        nx -= 1

                    number = 0
                    nx += 1
                    while nx+dx < len(self.grid[0]) and self.grid[y+dy][nx+dx].isnumeric():
                        number *= 10
                        number += int(self.grid[y+dy][nx+dx])
                        nx += 1
                        evaluated.add((y+dy, nx+dx))

                    numbers.append(number)
        return numbers

    def find_positions(self):
        positions = []

        for y in range(len(self.grid)):
            for x in range(len(self.grid[0])):
                if self.grid[y][x] == "*":
                    positions.append((x, y))

        return positions

    def solve(self, input_data: str) -> int:
        self.grid = input_data.splitlines()
        total = 0
        positions = self.find_positions()

        for x, y in positions:
            numbers = self.find_numbers(x, y)
            if len(numbers) == 2:
                total += numbers[0]*numbers[1]

        return total
