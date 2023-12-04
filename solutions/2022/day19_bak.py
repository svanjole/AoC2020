from utils.abstract import FileReaderSolution
from functools import cache
from copy import deepcopy

class Day19:
    def __init__(self):
        self.robots = {}
        self.resources = {}
        self.blueprints = []
        self.reset()
        self.current_best = 0

    def reset(self):
        self.current_best = 0
        self.robots = {"ore": 1, "clay": 0, "obsidian": 0, "geode": 0 }
        self.resources = {
            "ore": 0,
            "clay": 0,
            "obsidian": 0,
            "geode": 0
        }

    def parse(self, input_data):
        for blueprint in input_data.split("\n"):
            bp = {}
            for line in blueprint.split(". "):
                parts = line.split("costs")
                if parts[0].split(" ")[0] == "Blueprint":
                    type = parts[0].split(" ")[3]
                else:
                    type = parts[0].split(" ")[1]

                costs = parts[1].split(" and ")
                c = []
                for cost in costs:
                    cost = cost.lstrip().replace(".", "")
                    cost = cost.split(" ")
                    c.append((cost[1], int(cost[0])))
                bp[type] = c

            self.blueprints.append(bp)

    def dfs2(self, bp_idx, ore, clay, obsidian, r_ore, r_clay, r_obsidian, time):
        if time == 0:
            return 0


    @cache
    def dfs(self, bp_idx, state, time):
        #print(time, state)
        self.current_best = max(dict(state[0])["geode"], self.current_best)

        def can_construct_robot(resource, resources):
            for cost in bp[resource]:
                if resources[cost[0]] < cost[1]:
                    return False
            return True

        def construct_robot(resource, robots, resources):
            robots["geode"] += 1
            for cost in bp[resource]:
                resources[cost[0]] -= cost[1]

            return robots, resources

        current_robots = deepcopy(dict(state[0]))
        current_resources = deepcopy(dict(state[1]))

        if time == 0:
            return 0

        bp = self.blueprints[bp_idx]

        # increase resources


        #print(current_robots, current_resources)


        # check if we can build a geode robot
        if can_construct_robot("geode", current_resources):
            current_robots, current_resources = construct_robot("geode", current_robots, current_resources)
            for r, v in current_robots.items():
                current_resources[r] += v
            return current_robots["geode"] + self.dfs(bp_idx, self.create_state(current_robots, current_resources), time - 1)

        for r, v in current_robots.items():
            current_resources[r] += v

        options = [self.dfs(bp_idx, self.create_state(current_robots, current_resources), time - 1)]
        for res_type in ["ore", "clay", "obsidian"]:
            option_robots = deepcopy(current_robots)
            option_resources = deepcopy(current_resources)
            if can_construct_robot(res_type, option_resources):
                option_robots, option_resources = construct_robot(res_type, option_robots, option_resources)
                options.append(self.dfs(bp_idx, self.create_state(option_robots, option_resources), time - 1))

        return option_robots["geode"] + max(options)

    def create_state(self, robots, resources):
        return self.freeze(robots), self.freeze(resources)

    def freeze(self, d):
        if isinstance(d, dict):
            return frozenset((key, self.freeze(value)) for key, value in d.items())
        elif isinstance(d, list):
            return tuple(self.freeze(value) for value in d)
        return d


class Day19PartA(Day19, FileReaderSolution):
    def solve(self, input_data: str) -> int:
        self.parse(input_data)

        bests = []
        for i, blueprint in enumerate(self.blueprints):
            state = self.create_state(self.robots, self.resources)
            self.dfs(i, state, 24)
            bests.append((i+1)*self.current_best)
            self.reset()
        print(bests)
        return max(bests)


class Day19PartB(Day19, FileReaderSolution):
    def solve(self, input_data: str) -> int:
        return 0
