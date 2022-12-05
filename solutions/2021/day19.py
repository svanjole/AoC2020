from utils.abstract import FileReaderSolution
from abc import abstractmethod
import numpy as np
import math

class Scanner:
    coords = {}
    grid = None

    def __init__(self):
        self.beacons = {}

    def add_beacon(self, char, line):
        coord = list(map(lambda x: int(x), line.split(',')))
        self.beacons[chr(char)] = coord

    def get_overlap(self, s):
        def all_rotations(polycube):
            """List all 24 rotations of the given 3d array"""

            def rotations4(polycube, axes):
                """List the four rotations of the given 3d array in the plane spanned by the given axes."""
                for i in range(4):
                    yield np.rot90(polycube, i, axes)

            # imagine shape is pointing in axis 0 (up)

            # 4 rotations about axis 0
            yield from rotations4(polycube, (1, 2))

            # rotate 180 about axis 1, now shape is pointing down in axis 0
            # 4 rotations about axis 0
            yield from rotations4(np.rot90(polycube, 2, axes=(0, 2)), (1, 2))

            # rotate 90 or 270 about axis 1, now shape is pointing in axis 2
            # 8 rotations about axis 2
            yield from rotations4(np.rot90(polycube, axes=(0, 2)), (0, 1))
            yield from rotations4(np.rot90(polycube, -1, axes=(0, 2)), (0, 1))

            # rotate about axis 2, now shape is pointing in axis 1
            # 8 rotations about axis 1
            yield from rotations4(np.rot90(polycube, axes=(0, 1)), (0, 2))
            yield from rotations4(np.rot90(polycube, -1, axes=(0, 1)), (0, 2))

        for rotation in all_rotations(s):
            print("YAY")

class Day19:
    def __init__(self):
        self.scanners = []

    @abstractmethod
    def solve_part(self):
        pass

    def solve(self, input_data: str) -> int:
        self.parse_input(input_data)

        return self.solve_part()

    def parse_input(self, input_data: str):
        scanners = input_data.split("\n\n")

        for scanner in scanners:
            first_line = True
            char = 65
            s = Scanner()
            for line in scanner.splitlines():
                if first_line:
                    first_line = False
                    continue

                s.add_beacon(char, line)
                char += 1

            self.scanners.append(s)

    def common_solver(self):
        pass


class Day19PartA(Day19, FileReaderSolution):
    def distance(self,a ,b):
        return math.sqrt((b[0] - a[0]) ** 2 + (b[1] - a[1]) ** 2 + (b[2] - a[2]) ** 2)

    def solve_part(self) -> int:
        lambdas = []
        lambdas.append(lambda c: (+c[0], +c[1], +c[2]))
        lambdas.append(lambda c: (+c[0], +c[1], -c[2]))
        lambdas.append(lambda c: (+c[0], -c[1], +c[2]))
        lambdas.append(lambda c: (+c[0], -c[1], -c[2]))
        lambdas.append(lambda c: (-c[0], +c[1], +c[2]))
        lambdas.append(lambda c: (-c[0], +c[1], -c[2]))
        lambdas.append(lambda c: (-c[0], -c[1], +c[2]))
        lambdas.append(lambda c: (-c[0], -c[1], -c[2]))
        lambdas.append(lambda c: (+c[0], +c[2], +c[1]))
        lambdas.append(lambda c: (+c[0], +c[2], -c[1]))
        lambdas.append(lambda c: (+c[0], -c[2], +c[1]))
        lambdas.append(lambda c: (+c[0], -c[2], -c[1]))
        lambdas.append(lambda c: (-c[0], +c[2], +c[1]))
        lambdas.append(lambda c: (-c[0], +c[2], -c[1]))
        lambdas.append(lambda c: (-c[0], -c[2], +c[1]))
        lambdas.append(lambda c: (-c[0], -c[2], -c[1]))

        lambdas.append(lambda c: (+c[1], +c[0], +c[2]))
        lambdas.append(lambda c: (+c[1], +c[0], -c[2]))
        lambdas.append(lambda c: (+c[1], -c[0], +c[2]))
        lambdas.append(lambda c: (+c[1], -c[0], -c[2]))
        lambdas.append(lambda c: (-c[1], +c[0], +c[2]))
        lambdas.append(lambda c: (-c[1], +c[0], -c[2]))
        lambdas.append(lambda c: (-c[1], -c[0], +c[2]))
        lambdas.append(lambda c: (-c[1], -c[0], -c[2]))
        lambdas.append(lambda c: (+c[1], +c[2], +c[0]))
        lambdas.append(lambda c: (+c[1], +c[2], -c[0]))
        lambdas.append(lambda c: (+c[1], -c[2], +c[0]))
        lambdas.append(lambda c: (+c[1], -c[2], -c[0]))
        lambdas.append(lambda c: (-c[1], +c[2], +c[0]))
        lambdas.append(lambda c: (-c[1], +c[2], -c[0]))
        lambdas.append(lambda c: (-c[1], -c[2], +c[0]))
        lambdas.append(lambda c: (-c[1], -c[2], -c[0]))

        lambdas.append(lambda c: (+c[2], +c[0], +c[1]))
        lambdas.append(lambda c: (+c[2], +c[0], -c[1]))
        lambdas.append(lambda c: (+c[2], -c[0], +c[1]))
        lambdas.append(lambda c: (+c[2], -c[0], -c[1]))
        lambdas.append(lambda c: (-c[2], +c[0], +c[1]))
        lambdas.append(lambda c: (-c[2], +c[0], -c[1]))
        lambdas.append(lambda c: (-c[2], -c[0], +c[1]))
        lambdas.append(lambda c: (-c[2], -c[0], -c[1]))
        lambdas.append(lambda c: (+c[2], +c[1], +c[0]))
        lambdas.append(lambda c: (+c[2], +c[1], -c[0]))
        lambdas.append(lambda c: (+c[2], -c[1], +c[0]))
        lambdas.append(lambda c: (+c[2], -c[1], -c[0]))
        lambdas.append(lambda c: (-c[2], +c[1], +c[0]))
        lambdas.append(lambda c: (-c[2], +c[1], -c[0]))
        lambdas.append(lambda c: (-c[2], -c[1], +c[0]))
        lambdas.append(lambda c: (-c[2], -c[1], -c[0]))

        reference = self.scanners[0]
        ref_dist = {}

        for k in reference.beacons:
            ref_dist[k] = round(self.distance([0,0,0], reference.beacons[k]), 3)

        print(ref_dist)
        for l in lambdas:
            transformed = {}
            for key in self.scanners[1].beacons:
                transformed[key] = l(self.scanners[1].beacons[key])

            distances = {}
            for t in transformed:
                distances = {}
                dist = []
                for b in reference.beacons:
                    distances[t] = round(self.distance(transformed[t], reference.beacons[b]))
                    dist.append(distances[t])
                    if len(distances) == 25 and len(set(dist)) <= 13:
                        print(distances)
                        print(t, b, len(distances), len(distances) - len(set(dist)))

            #print(distances)




class Day19PartB(Day19, FileReaderSolution):
    def solve_part(self) -> int:
        pass

