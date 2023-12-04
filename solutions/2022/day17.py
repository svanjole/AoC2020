from utils.abstract import FileReaderSolution
from math import lcm

class Day17:
    def __init__(self):
        self.rocks = [
            [[1, 1, 1, 1]],
            [[0, 1, 0], [1, 1, 1], [0, 1, 0]],
            [[0, 0, 1], [0, 0, 1], [1, 1, 1]],
            [[1], [1], [1], [1]],
            [[1, 1], [1, 1]],
        ]

        self.width = 7
        self.grid = {}
        self.height = 0
        for i in range(self.width):
            self.grid[(i, 0)] = "-"
        self.jets = ""
        self.j_index = 0
        self.r_index = 0
        self.floor = [0] * self.width

    def pretty_print(self):
        maxy = max([y[1] for y in self.grid.keys()])
        for y in range(maxy, -1, -1):
            line = "|" if y > 0 else "+"
            for x in range(0, 7):
                line += self.grid[(x,y)] if (x,y) in self.grid else "."
            line += "|" if y > 0 else "+"
            print(line)
        print()

    def start(self, rock_amount):
        for i in range(rock_amount):
            # select rock
            self.fall()
            self.height = max(pos[1] for pos in self.grid.keys())

    def get_moving_items(self):
        return [(x, y) for x in range(0, 8) for y in range(self.height, self.height-4, -1) if (x, y) in self.grid.keys() and self.grid[(x, y)] == "@"]

    def handle_move(self, direction):
        items = self.get_moving_items()
        min_y, max_y = min(pos[1] for pos in items), max(pos[1] for pos in items)

        def is_block_able_to_move():
            for y in range(max_y, min_y-1, -1):
                items_to_evaluate = [pos[0] for pos in items if pos[1] == y]
                check_x = max(items_to_evaluate) if direction == 1 else min(items_to_evaluate)
                if (check_x + direction, y) in self.grid.keys() and self.grid[(check_x + direction, y)] in ["#", "-"]:
                    return False

                if check_x + direction < 0 or check_x + direction >= self.width:
                    return False

            return True

        if is_block_able_to_move():
            for pos in items:
                del self.grid[pos]

            for pos in items:
                self.grid[(pos[0]+direction, pos[1])] = "@"

    def reset(self):
        self.width = 7
        #self.grid = {}
        self.height = 0
        for i in range(self.width):
            self.grid[(i, 0)] = "-"
        self.floor = [0] * self.width

    def handle_fall(self):
        items = self.get_moving_items()
        if len(items) == 0:
            return False

        min_x, max_x = min(pos[0] for pos in items), max(pos[0] for pos in items)

        def is_block_able_to_move():
            for x in range(min_x, max_x + 1):
                items_to_evaluate = [pos[1] for pos in items if pos[0] == x]
                check_y = min(items_to_evaluate) #check lowest in column
                if (x, check_y - 1) in self.grid.keys() and self.grid[(x, check_y - 1)] == "#":
                    return False

                if check_y - 1 <= 0:
                    return False

            return True

        for pos in items:
            del self.grid[pos]

        if is_block_able_to_move():
            for pos in items:
                self.grid[(pos[0], pos[1] - 1)] = "@"
        else:
            for pos in items:
                self.grid[(pos[0], pos[1])] = "#"

        if is_block_able_to_move():
            self.height -= 1

        return is_block_able_to_move()

    def fall(self):
        rock = self.rocks[self.r_index % len(self.rocks)]
        self.r_index += 1
        rock_width, rock_height = len(rock[0]), len(rock)
        falling = True

        self.height += 3+rock_height
        for y_r in range(rock_height):
            for x_r in range(rock_width):
                if rock[y_r][x_r] == 1:
                    self.grid[(2+x_r, self.height-y_r)] = "@"
        #print("A new rock begins falling:")
        #self.pretty_print()
        while falling:
            direction = -1 if self.jets[self.j_index % len(self.jets)] == "<" else 1
            #print(f"Jet of gas pushes rock {'right' if direction == 1 else 'left'}:")
            self.handle_move(direction)
            #self.pretty_print()

            falling = self.handle_fall()
            #if falling:
            #    print(f"Rock falls 1 unit:")
           # else:
            #    print(f"Rock falls 1 unit, causing it to come to rest:")

            self.j_index += 1
        #self.pretty_print()


class Day17PartA(Day17, FileReaderSolution):
    def solve(self, input_data: str) -> int:
        self.jets = input_data
        self.start(1000000000000)
        #self.pretty_print()

        #max_y = max([pos[1] for pos in self.grid.keys()])
        return self.height


class Day17PartB(Day17, FileReaderSolution):
    def solve(self, input_data: str) -> int:
        self.jets = input_data

        i = 0
        sets = {}
        count = 0
        prev_difference = 0
        first_index = None
        height = 0
        while True:
            self.start(1)
            #print(f"{i}\t{self.j_index % len(self.jets)}\t{self.r_index % len(self.rocks)}\t{self.height}")
            i += 1
            key = (self.j_index % len(self.jets), self.r_index % len(self.rocks))

            if key not in sets:
                sets[key] = {
                    "curr": i,
                    "height": self.height
                }
                first_index = None
            else:
                sets[key]["prev"] = sets[key]["curr"]
                sets[key]["curr"] = i
                difference = sets[key]["curr"] - sets[key]["prev"]
                print(key, sets[key], difference, first_index, i, sets[key]["prev"]-first_index if first_index is not None else None)
                prev_key = key
                #quit()
                if difference == prev_difference and first_index != None:
                    count += 1
                else:
                    count = 0
                    prev_difference = difference
                    first_index = i - difference - 1
                    height = self.height-sets[key]["height"]
                    #print("NOK", first_index)

                if count > 100:
                    break

        # rock nr when first loop starts
        # amount of rocks
        # height increase


        # calculate height until rock nr
        # calculate amount of times amount of rocks fits in remainder
        # calculate remainder
        # reset
        # cacluc
        first_index += difference
        print(first_index, difference, height)
        print("OK")

        self.reset()
        current_height = 0
        for i in range(first_index):
            self.start(1)

        current_height += self.height
        max_rocks = 1000000000000 - first_index

        how_many_loops = max_rocks // difference - 1
        print("Loops:", max_rocks, how_many_loops)
        current_height += how_many_loops * height
        remainder = max_rocks % difference
        print("Remainder: ", remainder)
        self.reset()
        for i in range(remainder):
            self.start(1)

        current_height += self.height - 1
        print(current_height)

        print(current_height)
        quit()