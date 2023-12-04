from utils.abstract import FileReaderSolution
import re
import math


class Day22:
    def __init__(self):
        self.instructions = ""
        self.maze = {}
        self.size = [-1, -1]
        self.pos = (-1, -1)
        self.dirs = ">v<^"
        self.current_dir = 0
        self.face_size = 0

    def parse(self, input_data):
        parts = input_data.split("\n\n")
        self.parse_maze(parts[0])
        self.parse_instructions(parts[1])

    def parse_instructions(self, instructions):
        self.instructions = []
        matches = re.finditer(r"[A-Z]+|\d+", instructions)

        for matchNum, match in enumerate(matches, start=1):
            match = match.group()
            instruction = ("move", int(match)) if match.isdigit() else ("turn", match)
            self.instructions.append(instruction)

    def parse_maze(self, maze):
        lines = maze.split("\n")
        h = len(lines)
        w = max(len(line) for line in lines)
        self.size = [w, h]

        for y in range(h):
            for x in range(w):
                line = lines[y]
                if x < len(line):
                    if line[x] != " ":
                        self.maze[(x, y)] = line[x]
                    if self.pos == (-1, -1) and line[x] == ".":
                        self.pos = (x, y)
        self.face_size = int(math.sqrt(len(self.maze) / 6))

    def pretty_print(self):
        for y in range(self.size[1]):
            line = ""
            for x in range(self.size[0]):
                if (x, y) == self.pos:
                    line += "X"
                else:
                    line += str(self.maze[(x, y)]) if (x, y) in self.maze.keys() else " "
            print(line)
        print()
        print("Current direction: ", self.dirs[self.current_dir])

    def start(self):
        for action, value in self.instructions:
            print(action, value)
            if action == "move":
                for i in range(value):
                    res = self.move()
                    if not res: #movement not possible, break for loop
                        break
            else: #make a turn
                self.current_dir += 1 if value == "R" else -1
                if self.current_dir < 0:
                    self.current_dir += 4
                self.current_dir %= 4
                #print("New direction: ", self.dirs[self.current_dir])

    def move(self):
        dy = dx = 0
        match self.dirs[self.current_dir]:
            case ">":
                dx = 1
            case "<":
                dx = -1
            case "v":
                dy = 1
            case "^":
                dy = -1

        return self.handle_move(dx, dy)


class Day22PartA(Day22, FileReaderSolution):
    def solve(self, input_data: str) -> int:
        self.parse(input_data)
        self.start()

        return sum([
            1000 * (self.pos[1]+1),
            4 * (self.pos[0]+1),
            self.current_dir
        ])

    def handle_move(self, dx, dy):
        new_pos = (self.pos[0]+dx, self.pos[1]+dy)
        if new_pos in self.maze.keys(): # check i
            if self.maze[new_pos] == ".":
                self.pos = new_pos
            else: # we hit a wall, return False
                return False
        else: # we are moving off the edge of the map
            #print("Moving off the edge", new_pos)
            new_x, new_y = new_pos
            if dx != 0:
                new_x = 0 if dx == 1 else self.size[0] - 1
            elif dy != 0:
                new_y = 0 if dy == 1 else self.size[1] - 1

            new_pos = (new_x, new_y)
            while new_pos not in self.maze.keys():
                new_pos = (
                    (new_pos[0] + dx) % self.size[0],
                    (new_pos[1] + dy) % self.size[1]
                )
                #print(new_pos, dx, dy)
            self.pos = new_pos
        return True


class Day22PartB(Day22, FileReaderSolution):
    def handle_move(self, dx, dy):
        def pyhget_face_idx(pos):
            p = list(pos)
            if p[1] < self.face_size: #top row
                return 2-((p[0]-self.face_size)//self.face_size)

            p[1] -= self.face_size
            if p[1] // self.face_size == 0: # second row
                return 3

            p[1] -= self.face_size
            if p[1] // self.face_size == 0:  # third row
                return 4-((p[0]-self.face_size)//self.face_size)

            return 6

        def get_target_global_pos_example(face, local_pos):
            multipliers = {
                1: [2, 0],
                2: [0, 1],
                3: [1, 1],
                4: [2, 1],
                5: [2, 2],
                6: [3, 2]
            }
            m = multipliers[face]
            return m[0] * self.face_size + local_pos[0], m[1] * self.face_size + local_pos[1]

        def get_target_global_pos(face, local_pos):
            multipliers = {
                1: [2, 0],
                2: [1, 0],
                3: [1, 1],
                4: [1, 2],
                5: [0, 2],
                6: [0, 3]
            }
            m = multipliers[face]
            return m[0] * self.face_size + local_pos[0], m[1] * self.face_size + local_pos[1]

        def get_target_local_pos_example(local_pos, from_face, target_face):
            if from_face == 1 and target_face == 2:
                return self.face_size - 1 - local_pos[0], 0
            if from_face == 1 and target_face == 3:
                return local_pos[1], local_pos[0]
            if from_face == 1 and target_face == 6:
                return self.face_size - 1, self.face_size - 1 - local_pos[1]

            if from_face == 2 and target_face == 1:
                return self.face_size - 1 - local_pos[0], 0
            if from_face == 2 and target_face == 5:
                return self.face_size - 1 - local_pos[0], self.face_size - 1
            if from_face == 2 and target_face == 6:
                return self.face_size - 1, local_pos[1]

            if from_face == 3 and target_face == 1:
                return local_pos[1], local_pos[0]
            if from_face == 3 and target_face == 5:
                return 0, self.face_size - 1 - local_pos[0]

            if from_face == 4 and target_face == 6:
                return self.face_size - 1 - local_pos[1], 0

            if from_face == 5 and target_face == 2:
                return self.face_size - 1 - local_pos[0], self.face_size - 1
            if from_face == 5 and target_face == 3:
                return self.face_size - 1 - local_pos[0], self.face_size - 1

            if from_face == 6 and target_face == 1:
                return self.face_size - 1, self.face_size - 1 - local_pos[1]
            if from_face == 6 and target_face == 4:
                return self.face_size - 1, self.face_size - 1 - local_pos[0]

            print(local_pos, from_face, target_face)
            quit()
            raise "Not implemented"

        def get_target_local_pos(local_pos, from_face, target_face):
            transforms = [
                { ("v","<")}
            ]
            if from_face == 1 and target_face == 3:
                return self.face_size - 1, local_pos[0]
            if from_face == 1 and target_face == 4:
                return local_pos[0], self.face_size - 1 - local_pos[1]
            if from_face == 1 and target_face == 6:
                return local_pos[0], self.face_size - 1

            if from_face == 2 and target_face == 5:
                return local_pos[0], self.face_size-1-local_pos[1]
            if from_face == 2 and target_face == 6:
                return local_pos[1], local_pos[0]

            if from_face == 3 and target_face == 1:
                return local_pos[1], local_pos[0]

            if from_face == 3 and target_face == 5:
                return local_pos[1], local_pos[0]
            if from_face == 4 and target_face == 1:
                return local_pos[0], self.face_size - 1 - local_pos[1]
            if from_face == 4 and target_face == 6:
                return self.face_size - 1, local_pos[0]

            if from_face == 5 and target_face == 2:
                return local_pos[0], self.face_size - 1 - local_pos[1]
            if from_face == 5 and target_face == 3:
                return local_pos[1], local_pos[0]

            if from_face == 6 and target_face == 1:
                return local_pos[0], 0
            if from_face == 6 and target_face == 2:
                return local_pos[1], local_pos[0]
            if from_face == 6 and target_face == 4:
                return local_pos[1], local_pos[0]

            print(local_pos, from_face, target_face)
            quit()
            raise "Not implemented"

        def get_local_pos(pos):
            return pos[0] % self.face_size, pos[1] % self.face_size

        def get_target_face_idx(face, direction):
            targets = {
                (1, "^"): (6, "^"),
                (1, ">"): (4, "<"),
                (1, "v"): (3, "<"),
                (2, "^"): (6, ">"),
                (2, "<"): (5, ">"),
                (3, "<"): (5, "v"),
                (3, ">"): (1, "^"),
                (4, "v"): (6, "<"),
                (4, ">"): (1, "<"),
                (5, "^"): (3, ">"),
                (5, "<"): (2, ">"),
                (6, ">"): (4, "^"),
                (6, "v"): (1, "v"),
                (6, "<"): (2, "v")
            }
            return targets[(face, self.dirs[direction])]

        def get_target_face_idx_example(face, direction):
            targets = {
                (1, "^"): (2, "v"),
                (1, "<"): (3, "v"),
                (1, ">"): (6, "<"),
                (2, "^"): (1, "v"),
                (2, "v"): (5, "^"),
                (2, "<"): (6, "^"),
                (3, "^"): (1, ">"),
                (3, "v"): (5, ">"),
                (4, ">"): (6, "v"),
                (5, "v"): (2, "^"),
                (5, "<"): (3, "^"),
                (6, ">"): (1, "<"),
                (6, "^"): (4, "<")
            }
            return targets[(face, self.dirs[direction])]

        def get_face_idx_example(pos):
            face = 1 if pos[1] < self.face_size else 0
            if face == 0:
                face = 2 + (pos[0] // self.face_size)

            if pos[1] >= self.face_size * 2:
                face += 1
            return face

        #for key in self.maze.keys():
#            self.maze[key] = get_face_idx(list(key))
#
#        self.pretty_print()
#        quit()

        new_pos = (self.pos[0] + dx, self.pos[1] + dy)
        #print("Old pos:" , self.pos, "New Pos: ", new_pos)
        if new_pos in self.maze.keys():  # check i
            if self.maze[new_pos] == ".":
                self.pos = new_pos
            else:  # we hit a wall, return False
                return False
        else:  # we are moving off the edge of the map
            print("OK")
            current_face = get_face_idx(self.pos)
            local_pos = get_local_pos(self.pos)
            target_face, new_dir = get_target_face_idx(current_face, self.current_dir)
            target_local_pos = get_target_local_pos(local_pos, current_face, target_face)
            new_pos = get_target_global_pos(target_face, target_local_pos)
            print(self.pos, current_face, local_pos, target_face, target_local_pos, new_pos)
            if self.maze[new_pos] == ".":
                self.pos = new_pos
                self.current_dir = self.dirs.index(new_dir)
            else:  # we hit a wall, return False
                return False

        return True

    def solve(self, input_data: str) -> int:
        self.parse(input_data)
        # A = (11, 5) -> Face 4
        # B = (14,8) -> Face 6
        # C = (10,11) -> Face 5
        # D = (1,7,11) -> Face 2
        # test case 1 (from face 4 to face 6)
        # self.pos = (0, 4)
        # self.current_dir = 0
        #self.pos = (15, 8)
        #self.current_dir = 0
        #self.instructions = [("move", 1)]
        self.start()
        self.pretty_print()
        return sum([
            1000 * (self.pos[1] + 1),
            4 * (self.pos[0] + 1),
            self.current_dir
        ])
