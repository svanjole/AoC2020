from utils.abstract import FileReaderSolution
from abc import abstractmethod
from math import prod


class BasePacket:
    version: int
    type_id: int

    def __init__ (self, version, type_id):
        self.version = version
        self.type_id = type_id

    @abstractmethod
    def get_version_sum(self):
        pass

    @abstractmethod
    def get_value(self):
        pass


class LiteralPacket(BasePacket):
    value: int

    def __init__(self, version, type_id, value):
        BasePacket.__init__(self, version, type_id)
        self.value = value

    def get_version_sum(self):
        return self.version

    def get_value(self):
        return self.value


class OperatorPacket(BasePacket):
    length_type_id: int
    subpackets: []

    def __init__(self, version, type_id, length_type_id):
        BasePacket.__init__(self, version, type_id)
        self.length_type_id = length_type_id
        self.subpackets = []

    def get_version_sum(self):
        return self.version + sum(sub.get_version_sum() for sub in self.subpackets)

    def get_value(self):
        if self.type_id == 0:
            return sum(sub.get_value() for sub in self.subpackets)

        elif self.type_id == 1:
            return prod(sub.get_value() for sub in self.subpackets)

        elif self.type_id == 2:
            return min(sub.get_value() for sub in self.subpackets)

        elif self.type_id == 3:
            return max(sub.get_value() for sub in self.subpackets)

        elif self.type_id == 5:
            return 1 if self.subpackets[0].get_value() > self.subpackets[1].get_value() else 0

        elif self.type_id == 6:
            return 1 if self.subpackets[0].get_value() < self.subpackets[1].get_value() else 0

        elif self.type_id == 7:
            return 1 if self.subpackets[0].get_value() == self.subpackets[1].get_value() else 0

        return -1

class Day16:
    pos: int

    def __init__(self):
        self.binary = ""
        self.packet = None

    @abstractmethod
    def solve_part(self, median):
        pass

    @staticmethod
    def read_integer(binary, start, length):
        return int(binary[start: start+length], 2)

    def parse_packet(self, binary, pointer):
        if binary.find("1", pointer) == -1:
            return None, pointer

        # read header info
        version = self.read_integer(binary, pointer, 3)
        type_id = self.read_integer(binary, pointer + 3, 3)
        pointer += 6

        if type_id == 4:
            continue_reading = True
            bits = ""
            while continue_reading:
                continue_reading = binary[pointer] == "1"
                bits += binary[pointer + 1: pointer + 5]
                pointer += 5

            return LiteralPacket(version, type_id, int(bits, 2)), pointer
        else:
            length_type_id = self.read_integer(binary, pointer, 1)
            pointer += 1

            length_size = 15 if length_type_id == 0 else 11
            packet = OperatorPacket(version, type_id, length_type_id)

            length = self.read_integer(binary, pointer, length_size)
            pointer += length_size

            if length_type_id == 0:
                bits_left = length
                while bits_left > 0:
                    subpacket, new_pointer = self.parse_packet(binary, pointer)
                    packet.subpackets.append(subpacket)
                    bits_left -= new_pointer - pointer
                    pointer = new_pointer
            else:
                for i in range(length):
                    subpacket, pointer = self.parse_packet(binary, pointer)
                    packet.subpackets.append(subpacket)

            return packet, pointer

    def solve(self, input_data: str) -> int:
        binary = ""
        for char in input_data:
            binary += bin(int(char, 16))[2:].zfill(4)

        self.packet, pointer = self.parse_packet(binary, 0)

        return self.solve_part()


    def common_solver(self):
        pass


class Day16PartA(Day16, FileReaderSolution):
    def solve_part(self) -> int:
        return self.packet.get_version_sum()


class Day16PartB(Day16, FileReaderSolution):
    def solve_part(self) -> int:
        return self.packet.get_value()

