from utils.abstract import FileReaderSolution
from abc import abstractmethod
from copy import deepcopy

class Amphipod:
    def __init__(self, letter, pos):
        #self.start = pos
        self.pos = pos
        self.letter = letter
        self.has_moved = False
        self.at_target = False

    def __str__(self):
        return f"{self.letter} -> {self.pos} ({self.at_target})"

    def __repr__(self):
        return f"{self.letter} -> {self.pos} ({self.at_target})"


class Day23:
    def __init__(self):
        self.grid = []
        self.amphipods = []
        self.best_score = 999999999999
        self.best_path = []

    @abstractmethod
    def solve_part(self):
        pass

    def solve(self, input_data: str) -> int:
        self.parse_input(input_data)

        return self.solve_part()

    def parse_input(self, input_data: str):
        self.amphipods = []
        self.grid = []
        y = 0
        for line in input_data.splitlines():
            x = 0
            self.grid.append([])
            for char in line:
                if char == "#":
                    self.grid[y].append('#')
                elif char == ".":
                    self.grid[y].append(".")
                elif char == " ":
                    self.grid[y].append(".")
                else:
                    self.grid[y].append(char)
                    self.amphipods.append(Amphipod(char, [x, y]))
                x += 1
            y += 1

    def perform_move(self, state, move):
        def get_energy(letter):
            if letter == "A":
                return 1
            if letter == "B":
                return 10
            if letter == "C":
                return 100
            if letter == "D":
                return 1000

        state.path.append(move)
        dx = abs(move["from"][0] - move["to"][0])
        dy = abs(move["from"][1] + move["to"][1]) - 2
        #print(f"Moving {move['letter']} from {move['from']} to {move['to']}")
        energy = get_energy(move["letter"])*(dx+dy)
        state.score += energy

        #update amphipod
        state.grid[move["from"][1]][move["from"][0]] = "."
        state.grid[move["to"][1]][move["to"][0]] = move["letter"]

        for amphipod in state.amphipods:
            if amphipod.pos == move["from"]:
                amphipod.pos = move["to"]
                amphipod.has_moved = True

                if move["to"] in self.rooms[amphipod.letter]:
                    amphipod.at_target = True
                break

        return state

    def everything_in_place(self, amphipods):
        count = 0

        for amphipod in amphipods:
            if amphipod.pos in self.rooms[amphipod.letter]:
                count += 1

        return count == len(amphipods)

    def find_best_path(self, state):
        #self.pretty_print(state.grid)
        next_moves = self.get_next_moves(state)
        if self.everything_in_place(state.amphipods):
            if state.score < self.best_score:
                print(state.score)
                print(state.path)
                self.best_score = state.score
                self.best_path = state.path
        else:
            for move in next_moves:
                new_state = self.perform_move(deepcopy(state), move)
                if new_state.score >= self.best_score:
                    return

                self.find_best_path(new_state)

        return

    def pretty_print(self, grid):
        for y in range(len(grid)):
            print("".join(grid[y]))

    def find_free_hallway_spots(self, grid, pos):
        hallway_spots = [1, 2, 4, 6, 8, 10, 11]
        left = list(filter(lambda x: x < pos, hallway_spots))
        left.reverse()
        right = list(filter(lambda x: x > pos, hallway_spots))

        free_spots = []
        for x in left:
            if not grid[1][x] == ".":
                break
            free_spots.append(x)

        for x in right:
            if not grid[1][x] == ".":
                break
            free_spots.append(x)

        return free_spots

    def is_room_available(self, grid, letter):
        #print(f"Checking if room {letter} is available")
        coords = self.rooms[letter]

        for c in coords:
            if grid[c[1]][c[0]] != "." and grid[c[1]][c[0]] != letter:
                return False

        return True

    def can_move_to_room(self, grid, amphipod):
        #print("Checking if we can move the amphipod to a room")
        letter = amphipod.letter

        if not self.is_room_available(grid, letter):
            return False

        min_x = min(amphipod.pos[0], self.rooms[letter][0][0])
        max_x = max(amphipod.pos[0], self.rooms[letter][0][0])
        obstructed = False

        for x in range(min_x + 1, max_x):
            if grid[1][x] != ".":
                obstructed = True
                break

        return not obstructed

    def get_spot_in_room(self, grid, letter):
        #self.pretty_print(grid)
        room_x= self.rooms[letter][0][0]

        for y in range(5, 1, -1):
            if grid[y][room_x] == ".":
                return [room_x, y]


    def get_next_moves(self, state):
        #print(self.rooms)
        #self.pretty_print(grid)
        possible_moves = []

        for amphipod in state.amphipods:
            #print(amphipod.letter)
            #print(amphipod.start)
            #print(amphipod.pos)
            if amphipod.at_target:
                continue

            #print(f"Amphipod {amphipod.letter} has moved? {amphipod.has_moved}")
            if not amphipod.has_moved:
                # check if space above is free
                x = amphipod.pos[0]
                y = amphipod.pos[1]
                if not state.grid[y-1][x] == ".":
                    continue

                #print(f"Pos {x},{y - 1} above amphipod is free")

                # 1 check if amphipod can go to a room, best option at all time, return only that move

                if self.can_move_to_room(state.grid, amphipod):
                    #print (f"{amphipod.letter} is able to move to his room")
                    #possible_moves.append({})
                    to = self.get_spot_in_room(state.grid, amphipod.letter)
                    possible_moves.append({
                        "letter": amphipod.letter,
                        "from": amphipod.pos,
                        "to": to
                    })
                    return possible_moves

                #print(f"{amphipod.letter} is not able to move to his room")
                #print("Checking for possible hallway spots")

                # 2 if not, check possible hallway spots
                #amphipod is able to move, find free places in hallway
                hallway_spots = self.find_free_hallway_spots(state.grid, x)
                for spot in hallway_spots:
                    possible_moves.append({
                        "letter": amphipod.letter,
                        "from": amphipod.pos,
                        "to": [spot, 1]
                    });
            else:
                # check if a target space is reachable
                if self.can_move_to_room(state.grid, amphipod):
                    to = self.get_spot_in_room(state.grid, amphipod.letter)
                    possible_moves.append({
                        "letter": amphipod.letter,
                        "from": amphipod.pos,
                        "to": to
                    })

        return possible_moves


class State:
    def __init__(self, grid, amphipods, score, path):
        self.grid = grid
        self.amphipods = amphipods
        self.score = score
        self.path = path


class Day23PartA(Day23, FileReaderSolution):
    def solve_part(self) -> int:
        amphipods = self.amphipods
        #    0123456789012
        #   0#############
        #   1#...........#
        #   2###B#C#B#D###
        #   3  #A#D#C#A#
        #   4  #########

        self.rooms = {
            "A": [[3, 2], [3, 3]],
            "B": [[5, 2], [5, 3]],
            "C": [[7, 2], [7, 3]],
            "D": [[9, 2], [9, 3]]
        }

        for amphipod in amphipods:
            if amphipod.pos in self.rooms[amphipod.letter]:
                if amphipod.pos[1] == 2 and self.grid[amphipod.pos[1]+1][amphipod.pos[0]] == amphipod.letter:
                    amphipod.at_target = True
                elif amphipod.pos[1] == 3:
                    amphipod.at_target = True

        state = State(self.grid, amphipods, 0, [])

        self.find_best_path(state)
        print(self.best_score)
        print(self.best_path)

        return self.best_score



class Day23PartB(Day23, FileReaderSolution):
    def solve_part(self) -> int:
        amphipods = self.amphipods
        #    0123456789012
        #   0#############
        #   1#...........#
        #   2###B#C#B#D###
        #   3  #A#D#C#A#
        #   4  #########

        self.rooms = {
            "A": [[3, 2], [3, 3], [3, 4], [3, 5]],
            "B": [[5, 2], [5, 3], [5, 4], [5, 5]],
            "C": [[7, 2], [7, 3], [7, 4], [7, 5]],
            "D": [[9, 2], [9, 3], [9, 4], [9, 5]]
        }

        self.pretty_print(self.grid)
        for amphipod in amphipods:
            if amphipod.pos in self.rooms[amphipod.letter]:
                amphipod.at_target = True
                for y in range(amphipod.pos[1]+1, 6):
                    if self.grid[y][amphipod.pos[0]] != amphipod.letter:
                        amphipod.at_target = False

        state = State(self.grid, amphipods, 0, [])

        self.find_best_path(state)
        print(self.best_score)
        print(self.best_path)

        return self.best_score

