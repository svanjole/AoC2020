from utils.abstract import FileReaderSolution


class Day11:
    width: int
    height: int
    data: [[]]
    has_changed: bool

    def solve(self, input_data: str) -> int:
        self.set_data(input_data)

        while True:
            self.next_iteration()
            if not self.has_changed:
                break

        return str(self).count('#')

    def set_data(self, input_data):
        self.data = input_data.splitlines()
        self.height = len(self.data)
        self.width = len(self.data[0])

        for y in range(0, self.height):
            self.data[y] = [char for char in self.data[y]]

    def __str__(self):
        grid = ""
        for y in range(0, self.height):
            grid += ''.join(self.data[y])
            grid += "\r\n"

        return grid

    def next_iteration(self):
        self.has_changed = False
        new_data = [row[:] for row in self.data]

        for y in range(0, self.height):
            for x in range(0, self.width):
                nb = self.count_neighbours(x, y)
                self.handle_adjacency_rules(new_data, x, y, nb)

        self.data = new_data

    def is_valid_position(self, x, y):
        if y < 0 or y >= self.height:
            return False

        if x < 0 or x >= self.width:
            return False

        return True

    def count_neighbours(self, x, y):
        raise NotImplementedError

    def handle_adjacency_rules(self, new_data, x, y, nb):
        raise NotImplementedError


class Day11PartA(Day11, FileReaderSolution):
    def handle_adjacency_rules(self, new_data, x, y, nb):
        if self.data[y][x] == 'L':
            if nb == 0:
                new_data[y][x] = "#"
                self.has_changed = True
        elif self.data[y][x] == '#':
            if nb >= 4:
                new_data[y][x] = 'L'
                self.has_changed = True

    def count_neighbours(self, x, y):
        count = 0
        for dy in range(-1, 2):
            for dx in range(-1, 2):
                if dy == dx == 0:
                    continue

                if not self.is_valid_position(dx+x, dy+y):
                    continue

                if self.data[dy + y][dx + x] == '#':
                    count += 1

        return count


class Day11PartB(Day11, FileReaderSolution):
    def count_neighbours(self, x, y):
        count = 0
        for dy in range(-1, 2):
            for dx in range(-1, 2):
                if dy == dx == 0:
                    continue

                step = 1

                while self.is_valid_position(dx*step + x, dy*step+y):
                    if self.data[dy*step+y][dx*step + x] == '#':
                        count += 1
                        break
                    elif self.data[dy*step+y][dx*step + x] == 'L':
                        break

                    step += 1

        return count

    def handle_adjacency_rules(self, new_data, x, y, nb):
        if self.data[y][x] == 'L':
            if nb == 0:
                new_data[y][x] = "#"
                self.has_changed = True
        elif self.data[y][x] == '#':
            if nb >= 5:
                new_data[y][x] = 'L'
                self.has_changed = True
