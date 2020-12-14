from utils.abstract import FileReaderSolution
import math


class Day13:
    @staticmethod
    def get_busses(line):
        busses = []

        for bus in line.split(','):
            busses.append(bus)

        return busses


class Day13PartA(Day13, FileReaderSolution):
    def solve(self, input_data: str) -> int:
        lines = input_data.splitlines()
        timestamp = int(lines[0])

        bus_times = {}

        for bus in self.get_busses(lines[1]):
            if bus == 'x':
                continue

            times = math.ceil(timestamp / int(bus))
            bus_timestamp = times * int(bus)
            bus_times[int(bus)] = bus_timestamp - timestamp

        first_bus = min(bus_times.items(), key=lambda x: x[1])
        return int(math.prod(first_bus))


class Day13PartB(Day13, FileReaderSolution):
    def solve(self, input_data: str) -> int:
        lines = input_data.splitlines()
        busses = self.get_busses(lines[1])

        integers = []
        divisors = []

        for pos in range(0, len(busses)):
            if busses[pos] == 'x':
                continue

            integers.append(pos)
            divisors.append(int(busses[pos]))

        return self.crt(divisors, integers)

    def crt(self, divisors, integers):
        total = 0
        prod = math.prod(divisors)

        for divisor, integer in zip(divisors, integers):
            p = prod // divisor
            total -= integer * self.mul_inv(p, divisor) * p

        return total % prod

    @staticmethod
    def mul_inv(a, mod):
        b = a % mod
        for x in range(1, mod):
            if (b * x) % mod == 1:
                return x

        return 1
