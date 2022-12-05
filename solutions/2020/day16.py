from utils.abstract import FileReaderSolution
import math


class Ticket:
    def __init__(self, values):
        self.values = [int(x) for x in values.split(",")]


class Validation:
    field: str
    valid_ranges: []

    def __init__(self, key):
        self.field = key
        self.valid_ranges = []

    def add_range(self, min_value, max_value):
        self.valid_ranges.append({
            'min': int(min_value),
            'max': int(max_value)
        })

    def is_valid(self, value):
        for valid_range in self.valid_ranges:
            if valid_range['min'] <= value <= valid_range['max']:
                return True

        return False


class Day16:
    ticket: Ticket
    tickets: []
    valid_tickets: []
    error_rate: int
    field_names: []

    def __init__(self):
        self.validations = {}
        self.tickets = []
        self.valid_tickets = []
        self.error_rate = 0
        self.field_names = []

    def is_value_valid_for_any_field(self, value):
        for field, validation in self.validations.items():
            if validation.is_valid(value):
                return True

        self.error_rate += value

        return False

    @staticmethod
    def parse_tickets(input_data):
        tickets = []
        lines = input_data.splitlines()

        for line in lines[1:]:
            tickets.append(Ticket(line))

        if len(tickets) == 1:
            return tickets[0]

        return tickets

    def parse_validations(self, section):
        lines = section.split("\n")

        for line in lines:
            elements = line.split(": ")
            field_name = elements[0]
            self.field_names.append(field_name)
            self.validations[field_name] = Validation(field_name)

            for valid_range in elements[1].split(" or "):
                bounds = valid_range.split("-")
                self.validations[field_name].add_range(bounds[0], bounds[1])

    def solve(self, input_data: str) -> int:
        sections = input_data.split("\n\n")
        self.parse_validations(sections[0])

        self.ticket = self.parse_tickets(sections[1])
        self.tickets = self.parse_tickets(sections[2])

        self.valid_tickets = []

        for ticket in self.tickets:
            valid_ticket = True
            for value in ticket.values:
                if not self.is_value_valid_for_any_field(value):
                    valid_ticket = False

            if valid_ticket:
                self.valid_tickets.append(ticket)

        return self.calculate_solution()

    def calculate_solution(self):
        raise NotImplementedError


class Day16PartA(Day16, FileReaderSolution):
    def calculate_solution(self):
        return self.error_rate


class Day16PartB(Day16, FileReaderSolution):
    def remove_options(self, field_name, ordered_field_names):
        for index, column in enumerate(ordered_field_names):
            if len(column) == 1:
                continue

            if field_name in column:
                ordered_field_names[index].remove(field_name)

            if len(column) == 1:
                ordered_field_names = self.remove_options(column[0], ordered_field_names)

        return ordered_field_names

    def calculate_solution(self):
        field_options = []

        for i in range(0, len(self.field_names)):
            field_options.append(self.field_names.copy())

        for ticket in self.valid_tickets:
            for index, field_value in enumerate(ticket.values):
                for field_name in field_options[index]:
                    validation = self.validations[field_name]
                    if not validation.is_valid(field_value):
                        field_options[index].remove(field_name)

            for column_options in field_options:
                if len(column_options) == 1:
                    field_options = self.remove_options(column_options[0], field_options)

        mapped_ticket = dict(zip(list(map(lambda x: x[0], field_options)), self.ticket.values))

        return math.prod([v for k, v in mapped_ticket.items() if k.startswith('departure')])
