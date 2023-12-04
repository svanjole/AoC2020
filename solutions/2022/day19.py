# Input: Lines like "Blueprint <#>: Each ore robot costs <#> ore.
#                    Each clay robot costs <#> ore.
#                    Each obsidian robot costs <#> ore and <#> clay.
#                    Each geode robot costs <#> ore and <#> obsidian."
# Output: Starting with one ore-collecting robot and one blueprint,
#         spending 1 minute to build any one robot,
#         how many geodes could you collect within 24 minutes?
#         Calculate sum(ID * max geodes) over all blueprints

from functools import cache

blueprints = []

input_data = open(r"./solutions/2022/data/day19.txt")
for input_line in input_data.read().splitlines():
    input_line = input_line.replace("\n", "")
    parts = input_line.split(": Each ore robot costs ")
    parts[0] = parts[0].replace("Blueprint ", "")
    blueprint_index = int(parts[0])
    rest_of_line = parts[1]
    parts = rest_of_line.split(" ore. Each clay robot costs ")
    ore_robot_cost_ore = int(parts[0])
    rest_of_line = parts[1]
    parts = rest_of_line.split(" ore. Each obsidian robot costs ")
    clay_robot_cost_ore = int(parts[0])
    rest_of_line = parts[1]
    parts = rest_of_line.split(" clay. Each geode robot costs ")
    # At this point, parts[0] = "<#> ore and <#>" [clay]
    #            and parts[1] = "<#> ore and <#> obsidian."
    obsidian_parts = parts[0].split(" ore and ")
    obsidian_robot_cost_ore = int(obsidian_parts[0])
    obsidian_robot_cost_clay = int(obsidian_parts[1])
    geode_parts = parts[1].split(" ore and ")
    geode_parts[1] = geode_parts[1].replace(" obsidian.", "")
    geode_robot_cost_ore = int(geode_parts[0])
    geode_robot_cost_obsidian = int(geode_parts[1])
    blueprints.append([
        blueprint_index,
        ore_robot_cost_ore,
        clay_robot_cost_ore,
        obsidian_robot_cost_ore,
        obsidian_robot_cost_clay,
        geode_robot_cost_ore,
        geode_robot_cost_obsidian
    ])

@cache
def max_geodes(
    blueprint_index,
    ore_robot_cost_ore,
    clay_robot_cost_ore,
    obsidian_robot_cost_ore,
    obsidian_robot_cost_clay,
    geode_robot_cost_ore,
    geode_robot_cost_obsidian,
    ore,
    clay,
    obsidian,
    ore_robots,
    clay_robots,
    obsidian_robots,
    geode_robots,
    minutes_left
):

    if minutes_left == 0:
        return 0

    # Each minute:
    #   * Optionally start building 1 type of robot, materials permitting.
    #   * Each ore robot collects 1 ore.
    #   * Each clay robot collects 1 clay.
    #   * Each obsidian robot collects 1 obsidian.
    #   * Each geode robot collects 1 geode.

    # If we can build a geode robot, then do so
    if ore >= geode_robot_cost_ore and obsidian >= geode_robot_cost_obsidian:
        return geode_robots + max_geodes(
            blueprint_index,
            ore_robot_cost_ore,
            clay_robot_cost_ore,
            obsidian_robot_cost_ore,
            obsidian_robot_cost_clay,
            geode_robot_cost_ore,
            geode_robot_cost_obsidian,
            ore - geode_robot_cost_ore + ore_robots,
            clay + clay_robots,
            obsidian - geode_robot_cost_obsidian + obsidian_robots,
            ore_robots,
            clay_robots,
            obsidian_robots,
            geode_robots + 1,
            minutes_left - 1
        )

    # Otherwise, if we can't build a geode robot by next-to-last minute
    # even if we built an obsidian robot every minute in between,
    # then current geode robots are all we'll get
    possible_obsidian = obsidian
    for i in range(0, minutes_left - 2):
        possible_obsidian += obsidian_robots + i
    if possible_obsidian < geode_robot_cost_obsidian:
        return geode_robots * minutes_left

    # Otherwise, compile all other options and determine the best result
    options = []

    # Option: Don't build a robot.
    options.append(max_geodes(
        blueprint_index,
        ore_robot_cost_ore,
        clay_robot_cost_ore,
        obsidian_robot_cost_ore,
        obsidian_robot_cost_clay,
        geode_robot_cost_ore,
        geode_robot_cost_obsidian,
        ore + ore_robots,
        clay + clay_robots,
        obsidian + obsidian_robots,
        ore_robots,
        clay_robots,
        obsidian_robots,
        geode_robots,
        minutes_left - 1
    ))

    # Option: Build an ore robot
    if ore >= ore_robot_cost_ore:
        options.append(max_geodes(
            blueprint_index,
            ore_robot_cost_ore,
            clay_robot_cost_ore,
            obsidian_robot_cost_ore,
            obsidian_robot_cost_clay,
            geode_robot_cost_ore,
            geode_robot_cost_obsidian,
            ore - ore_robot_cost_ore + ore_robots,
            clay + clay_robots,
            obsidian + obsidian_robots,
            ore_robots + 1,
            clay_robots,
            obsidian_robots,
            geode_robots,
            minutes_left - 1
        ))

    # Option: Build a clay robot
    if ore >= clay_robot_cost_ore:
        options.append(max_geodes(
            blueprint_index,
            ore_robot_cost_ore,
            clay_robot_cost_ore,
            obsidian_robot_cost_ore,
            obsidian_robot_cost_clay,
            geode_robot_cost_ore,
            geode_robot_cost_obsidian,
            ore - clay_robot_cost_ore + ore_robots,
            clay + clay_robots,
            obsidian + obsidian_robots,
            ore_robots,
            clay_robots + 1,
            obsidian_robots,
            geode_robots,
            minutes_left - 1
        ))

    # Option: Build an obsidian robot
    if ore >= obsidian_robot_cost_ore and clay >= obsidian_robot_cost_clay:
        options.append(max_geodes(
            blueprint_index,
            ore_robot_cost_ore,
            clay_robot_cost_ore,
            obsidian_robot_cost_ore,
            obsidian_robot_cost_clay,
            geode_robot_cost_ore,
            geode_robot_cost_obsidian,
            ore - obsidian_robot_cost_ore + ore_robots,
            clay - obsidian_robot_cost_clay + clay_robots,
            obsidian + obsidian_robots,
            ore_robots,
            clay_robots,
            obsidian_robots + 1,
            geode_robots,
            minutes_left - 1
        ))

    return geode_robots + max(options)

def part1():
    total = 0
    for blueprint in blueprints:
        total += blueprint[0] * max_geodes(
            blueprint[0], # index
            blueprint[1], # ore robot cost (ore)
            blueprint[2], # clay robot cost (ore)
            blueprint[3], # obsidian robot cost (ore)
            blueprint[4], # obsidian robot cost (clay)
            blueprint[5], # geode robot cost (ore)
            blueprint[6], # geode robot cost (obsidian)
            0, # ore
            0, # clay
            0, # obsidian
            1, # ore robots
            0, # clay robots
            0, # obsidian robots
            0, # geode robots
            24 # minutes left
        )

    print (total)

def part2():
    total = 1
    for blueprint in blueprints:
        total *= blueprint[0] * max_geodes(
            blueprint[0],  # index
            blueprint[1],  # ore robot cost (ore)
            blueprint[2],  # clay robot cost (ore)
            blueprint[3],  # obsidian robot cost (ore)
            blueprint[4],  # obsidian robot cost (clay)
            blueprint[5],  # geode robot cost (ore)
            blueprint[6],  # geode robot cost (obsidian)
            0,  # ore
            0,  # clay
            0,  # obsidian
            1,  # ore robots
            0,  # clay robots
            0,  # obsidian robots
            0,  # geode robots
            32  # minutes left
        )

    print(total)

part2()