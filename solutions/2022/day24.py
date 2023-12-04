from collections import deque
from functools import cache

from utils.abstract import FileReaderSolution
from copy import deepcopy


class Day24:
    def __init__(self):
        self.dimensions = {}
        self.blizzard = []
        self.states = []
        self.start = ()
        self.goal = ()
        self.dirs = {
            ">": (1,0),
            "<": (-1,0),
            "v": (0,1),
            "^": (0,-1)
        }

    def get_dimensions(self):
        return tuple(op([x[i] for x in self.blizzard.keys()]) for i in [0, 1] for op in [min, max])

    def parse(self, input_data):
        lines = input_data.split("\n")
        for y in range(len(lines)):
            for x in range(len(lines[y])):
                if lines[y][x] not in [".", "#"]:
                    self.blizzard.append(((x, y), lines[y][x]))

        self.dimensions = {
            "x": (0, len(lines[y])),
            "y": (0, len(lines))
        }
        self.start = (1, 0)
        self.goal = (self.dimensions["x"][1]-2, self.dimensions["y"][1]-1)

    def pretty_print(self, padding=2, state=None, pos=None):
        if not state:
            state = self.blizzard

        min_x, max_x = self.dimensions["x"]
        min_y, max_y = self.dimensions["y"]
        for y in range(min_y-padding, max_y + padding):
            line = ""
            for x in range(min_x-padding, max_x + padding):
                items = [(pos, dir) for (pos, dir) in state if pos == (x, y)]
                count = len(items)
                #self.blizzard.index
                if count > 0:
                    line += str(count) if count > 1 else items[0][1]
                else:
                    if (x, y) == self.start:
                        line += "."
                    elif (x, y) == self.goal:
                        line += "."
                    elif (x, y) == pos:
                        line += "E"
                    else:
                        line += "." if x != 0 and y != 0 and x != max_x - 1 and y != max_y - 1 else "#"

            print(line)
        print()

    def move_blizzard(self):
        for idx, (pos, d) in enumerate(self.blizzard):
            new_pos = [sum(x) for x in zip(pos, self.dirs[d])]

            if new_pos[0] <= 0:
                new_pos[0] = self.dimensions["x"][1] - 2
            if new_pos[0] >= self.dimensions["x"][1] - 1:
                new_pos[0] = 1

            if new_pos[1] <= 0:
                new_pos[1] = self.dimensions["y"][1] - 2
            if new_pos[1] >= self.dimensions["y"][1] - 1:
                new_pos[1] = 1

            self.blizzard[idx] = (tuple(new_pos), d)

    def bfs(self, start, goal, start_idx):
        q = deque()
        visited = [(start, start_idx)]
        q.append((start, start_idx))

        while len(q) > 0:
            current_pos, current_state_idx = q.popleft()
            print(current_pos, current_state_idx)
            #self.pretty_print(0, self.states[current_state_idx], current_pos)
            if current_pos == goal:
                return current_state_idx

            next_state, next_state_idx = self.get_next_state(current_state_idx)
            next_blizzard_positions = [pos for pos, _ in next_state]


            # Action wait: check if current pos is empty in next state
            next_node = (current_pos, next_state_idx)
            if current_pos not in next_blizzard_positions and next_node not in visited:
                visited.append(next_node)
                q.append((current_pos, next_state_idx))

            neighbours_pos = [[sum(x) for x in zip(current_pos, dirs)] for dirs in self.dirs.values()]

            for nb in neighbours_pos:
                if tuple(nb) == goal:
                    return next_state_idx

                if nb[0] <= 0 or nb[1] <= 0: #wall
                    continue

                if nb[0] >= self.dimensions["x"][1] - 1: #wall
                    continue

                if nb[1] >= self.dimensions["y"][1] - 1:  # wall
                    continue

                next_node = (tuple(nb), next_state_idx)
                if tuple(nb) not in next_blizzard_positions and next_node not in visited:
                    visited.append(next_node)
                    q.append(next_node)

    def get_next_state(self, state_idx):
        if state_idx + 1 >= len(self.states):
            self.generate_new_state()

        return self.states[state_idx + 1], state_idx + 1

    def generate_new_state(self):
        self.blizzard = deepcopy(self.states[-1])
        self.move_blizzard()
        self.states.append(deepcopy(self.blizzard))


class Day24PartA(Day24, FileReaderSolution):
    def solve(self, input_data: str) -> int:
        self.parse(input_data)
        self.pretty_print(0)
        self.states = []
        self.states.append(deepcopy(self.blizzard))
        idx = self.bfs(self.start, self.goal)

        return idx


class Day24PartB(Day24, FileReaderSolution):
    def solve(self, input_data: str) -> int:
        self.parse(input_data)
        self.pretty_print(0)
        self.states = []
        self.states.append(deepcopy(self.blizzard))
        idx = self.bfs(self.start, self.goal, 0)
        idx = self.bfs(self.goal, self.start, idx)
        idx = self.bfs(self.start, self.goal, idx)
        return idx
