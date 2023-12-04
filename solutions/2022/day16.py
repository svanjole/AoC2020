import re
from utils.abstract import FileReaderSolution
from copy import deepcopy
from functools import cache


class Day16:
    def __init__(self):
        self.valves = {}
        self.current_best = 0
        self.amount = 0

    def parse(self, input_data):
        for line in input_data.split("\n"):
            id = re.match(r"Valve (.*) has",line).groups()[0]
            flow_rate = int(re.match(r"(.*)flow rate=(\d*)", line).groups()[1])
            neighbour_ids = [x.strip() for x in re.match(r"(.*)(valve[s]?)(.*)", line).groups()[2].split(",")]
            self.valves[id] = [flow_rate, neighbour_ids]

        self.amount = len([key for key, valve in self.valves.items() if valve[0] > 0])

    def dfs(self, state):
        if self.amount == len(state["open"]):
            state["total_pressure"] += state["pressure"] * state["time_left"]
            state["time_left"] = 0

        if state["time_left"] == 0:
            if state["total_pressure"] > self.current_best:
                self.current_best = state["total_pressure"]
                print(self.current_best)
                print(state)
            return


        #print(state["path"], state["time_left"], self.current_best)
        current_valve = state['current_valve']
        time_left = state['time_left']
        total_pressure = state['total_pressure']
        #print(f"Current valve: {current_valve}")
        #print(f"Time left: {time_left}")
        #print(f"Total pressure: {total_pressure}")
        #print(f"Open: [{', '.join(state['open'])}]")

        neighbours = []
        # check if valve can be openen and has a positive flowrate
        if current_valve not in state['open'] and state['valves'][current_valve][0] > 0:
#            print(f"Possible top open current valve with flowrate {self.valves[current_valve][0]}")
            new_state = deepcopy(state)
            new_state["total_pressure"] += new_state["pressure"]
            new_state["time_left"] -= 1
            new_state["open"].append(current_valve)
            new_state["history"].append(f"Opening {current_valve}; {state['pressure']}")
            new_state["pressure"] += state['valves'][current_valve][0]

            # current valve has only 1 neighbour
            if len(new_state['valves'][current_valve][1]) == 1:
                # remove current valve from neighbour new_state[valves]
                neighbour = new_state['valves'][current_valve][1][0]
                new_state["history"].append(f"Removing {current_valve} from neighbours of {neighbour}")
                new_state['valves'][neighbour][1].remove(current_valve)

            neighbours.append(new_state)

        # check if neighbour_valve has only 1 neighbour (current), if neighbour == open then remove current from state["valves"] to prune the tree

        for neighbour_valve in state['valves'][current_valve][1]:
            if state["previous_valve"] == neighbour_valve and len(self.valves[current_valve][1]) > 1:
                continue

            new_state = deepcopy(state)
            new_state["time_left"] -= 1
            new_state["path"].append(current_valve)
            new_state["history"].append(f"Moving from {current_valve} to {neighbour_valve}; {state['pressure']}")
            new_state["previous_valve"] = current_valve
            new_state["current_valve"] = neighbour_valve
            new_state["total_pressure"] += new_state["pressure"]

            if len(new_state['valves'][current_valve][1]) == 1 and current_valve in new_state['valves'][neighbour_valve][1]:
                # remove current valve from neighbour new_state[valves]
                #print(new_state)
                #print(current_valve, neighbour_valve)
                #print(new_state['valves'][neighbour_valve][1])
                new_state["history"].append(f"Removing {current_valve} from neighbours of {neighbour_valve}")
                new_state['valves'][neighbour_valve][1].remove(current_valve)

            neighbours.append(new_state)

        for neighbour in neighbours:
            self.bfs(neighbour)

    def base_solve(self):
        state = {
            "open": [],
            "pressure": 0,
            "total_pressure": 0,
            "time_left": 30,
            "current_valve": "AA",
            "previous_valve": None,
            "valves": deepcopy(self.valves),
            "path": [],
            "history": []
        }
        print(state)
        self.dfs(state)

class Day16PartA(Day16, FileReaderSolution):
    def solve(self, input_data: str) -> int:
        def parse(input_data):
            rates = {}
            links = {}
            for line in input_data.split("\n"):
                _, valve, _, _, srate, _, _, _, _, valves = line.split(' ', 9)
                rate = int(srate.rstrip(';').split('=')[1])
                rates[valve] = rate
                links[valve] = valves.split(', ')

            return rates, links

        rates, links = parse(input_data)
        self.parse(input_data)
        print(rates,links)
        print(self.valves)
        @cache
        def dfs(valve, time, visited):
            if time <= 0:
                return 0
            res = 0
            for link in links[valve]:
                res = max(res, dfs(link, time - 1, visited))
            if valve not in visited and rates[valve] > 0:
                visited = tuple(sorted([*visited, valve]))
                #rint(visited)
                res = max(res, dfs(valve, time - 1, visited) + rates[valve] * (time - 1))

            return res

        return dfs("AA", 30, ())


class Day16PartB(Day16, FileReaderSolution):
    def solve(self, input_data: str) -> int:
        return 0
