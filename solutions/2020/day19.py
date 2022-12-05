from dataclasses import dataclass
from utils.abstract import FileReaderSolution
from typing import Dict, List, Tuple


class Matcher:
    def match(self, s: str) -> Tuple[bool, str]:
        raise NotImplementedError()


@dataclass
class LiteralMatcher(Matcher):
    literal: str

    def match(self, s: str) -> Tuple[bool, str]:
        if s.startswith(self.literal):
            return True, s[1:]
        else:
            return False, s


@dataclass
class CompositionMatcher(Matcher):
    matchers: List[Matcher]

    def match(self, s: str) -> Tuple[bool, str]:
        orig = s
        for matcher in self.matchers:
            res, s = matcher.match(s)
            if not res:
                return False, orig
        return True, s


@dataclass
class OptionMatcher(Matcher):
    matchers: List[Matcher]

    def match(self, s: str) -> Tuple[bool, str]:

        orig = s
        for matcher in self.matchers:
            res, s = matcher.match(s)
            if res:
                return res, s
        return False, orig



class Day19:
    def __init__(self):
        self.rules = {}
        self.inputs = []

    def build_matcher(self, rule: str, rules: Dict[int, str]) -> Matcher:
        if rule.startswith('"') and rule.endswith('"'):
            return LiteralMatcher(rule.strip('"'))
        elif "|" in rule:
            return OptionMatcher(
                [self.build_matcher(sub_rule.strip(), rules) for sub_rule in rule.split("|")]
            )
        else:
            return CompositionMatcher(
                [self.build_matcher(rules[int(idx)], rules) for idx in rule.split()]
            )

    def parse_input_file(self, input_data: str):
        sections = input_data.split("\n\n")

        self.parse_rules(sections[0])
        self.parse_inputs(sections[1])

    def parse_rules(self, input_data):
        for rule in input_data.splitlines():
            (key, value) = rule.split(": ")
            self.rules[int(key)] = value

            #0: 4 1 5
            #1: 2 3 | 3 2
            #2: 4 4 | 5 5
            #3: 4 5 | 5 4
            #4: "a"
            #5: "b"

    def parse_inputs(self, input_data):
        self.inputs = input_data.splitlines()

    def solve(self, input_data: str) -> int:
       raise NotImplementedError


class Day19PartA(Day19, FileReaderSolution):
    def validate(self, message, rule_id):
        return self.rules[rule_id].validate(message, self.rules)

    def solve(self, input_data: str) -> int:
        self.parse_input_file(input_data)
        matcher = self.build_matcher(self.rules[0], self.rules)

        for input in self.inputs:
            result = matcher.match(input)
            print(result)

        return sum(matcher.match(input) == (True, "") for input in self.inputs)


class Day19PartB(Day19, FileReaderSolution):
    def solve(self, input_data: str) -> int:
        self.parse_input_file(input_data)
        return 0