from utils.abstract import FileReaderSolution


class Day12:
    directions = ['North', 'East', 'South', 'West']
    position = {}
    waypoint = {}

    def __init__(self):
        for direction in self.directions:
            self.position[direction] = 0
            self.waypoint[direction] = 0

        self.direction = 'East'

        self.waypoint['East'] = 10
        self.waypoint['North'] = 1

    def execute_route(self, input_data: str):
        instructions = input_data.splitlines();

        for instruction in instructions:
            action = instruction[0]
            value = int(instruction[1:])
            self.handle_instruction(action, value)

    def distance_from(self, x=0, y=0):
        return abs(self.position['East'] - self.position['West'])\
               + abs(self.position['North'] - self.position['South'] - y)

    def get_direction(self, current_direction, rotation, clockwise=True):
        amount = int(rotation / 90)
        return self.directions[(self.directions.index(current_direction) + (amount if clockwise else -amount)) % 4]


class Day12PartA(Day12, FileReaderSolution):
    def solve(self, input_data: str) -> int:
        self.execute_route(input_data)
        return self.distance_from(0, 0)

    def handle_instruction(self, action, value):
        if action == 'F':
            self.position[self.direction] += value
        elif action == 'N':
            self.position['North'] += value
        elif action == 'S':
            self.position['South'] += value
        elif action == 'E':
            self.position['East'] += value
        elif action == 'W':
            self.position['West'] += value
        elif action == 'L':
            self.direction = self.get_direction(self.direction, value, False)
        elif action == 'R':
            self.direction = self.get_direction(self.direction, value)
        else:
            raise ValueError(f"Unknown action: {action}")


class Day12PartB(Day12, FileReaderSolution):
    def solve(self, input_data: str) -> int:
        self.execute_route(input_data)
        return self.distance_from(0, 0)

    def rotate_waypoint(self, degrees, clockwise=True):
        new_waypoint = {}
        for direction in self.directions:
            # invert clockwise to remain order of keys in dictionary...
            new_direction = self.get_direction(direction, degrees, not clockwise)
            new_waypoint[direction] = self.waypoint[new_direction]

        self.waypoint = new_waypoint

    def move_waypoint(self, direction, amount):
        opposite_direction = self.get_direction(direction, 180)
        self.waypoint[direction] += amount

        if self.waypoint[opposite_direction] > 0:
            self.waypoint[opposite_direction] -= amount
            self.waypoint[direction] -= amount - abs(self.waypoint[opposite_direction])
            if self.waypoint[opposite_direction] > 0:
                self.waypoint[direction] = 0
            else:
                self.waypoint[opposite_direction] = 0

    def handle_instruction(self, action, value):
        if action == 'F':
            for direction in self.waypoint.keys():
                self.position[direction] += value * self.waypoint[direction]
        elif action == 'N':
            self.move_waypoint('North', value)
        elif action == 'E':
            self.move_waypoint('East', value)
        elif action == 'S':
            self.move_waypoint('South', value)
        elif action == 'W':
            self.move_waypoint('West', value)
        elif action == 'L':
            self.rotate_waypoint(value, False)
        elif action == 'R':
            self.rotate_waypoint(value)
