from functools import reduce
import operator
import time
from typing import overload

def parse_robot(raw: str) -> tuple[tuple[int, int], tuple[int, int]]:
    (position_raw, velocity_raw) = raw.split()
    (position_raw_x, position_raw_y) = position_raw.split(",")
    (velocity_raw_x, velocity_raw_y) = velocity_raw.split(",")
    position_x = int(position_raw_x.split("=")[1])
    position_y = int(position_raw_y)
    velocity_x = int(velocity_raw_x.split("=")[1])
    velocity_y = int(velocity_raw_y)
    return ((position_x, position_y), (velocity_x, velocity_y))


def count_robots_in_quadrants(
    robots: list[tuple[int, int]],
    bounds: tuple[int, int]
) -> list[int]:
    middle = (bounds[0] // 2, bounds[1] // 2)
    quadrant_count = [0, 0, 0, 0]
    for (x, y) in robots:
        if x == middle[0] or y == middle[1]:
            continue
        if x < middle[0]:
            if y < middle[1]:
                quadrant_count[1] += 1
            else:
                quadrant_count[2] += 1
        else:
            if y < middle[1]:
                quadrant_count[0] += 1
            else:
                quadrant_count[3] += 1
    return quadrant_count


def simulate(
    robots: list[tuple[tuple[int, int], tuple[int, int]]],
    steps: int,
    bounds: tuple[int, int]
) -> list[tuple[int, int]]:
    new_robots = []
    for i in range(len(robots)):
        (velocity_x, velocity_y) = robots[i][1]
        new_robots += [(
            (robots[i][0][0] + steps * velocity_x) % bounds[0],
            (robots[i][0][1] + steps * velocity_y) % bounds[1]
        )]
    return new_robots

def draw_robots(robots: list[tuple[int,int]], bounds: tuple[int, int]) -> None:
    for y in range(bounds[1]):
        print("".join(["#" if (x,y) in robots else "." for x in range(bounds[0])]))

def draw_simulate(
    robots: list[tuple[tuple[int, int], tuple[int, int]]],
    steps: int,
    bounds: tuple[int, int]
) -> None:
    max_delta = 0
    max_delta_index = 0
    current_robots = list(map(lambda x: x[0], robots.copy()))
    for t in range(1,steps+1):
        for i in range(len(robots)):
            (velocity_x, velocity_y) = robots[i][1]
            current_robots[i] = (
                (current_robots[i][0] + velocity_x) % bounds[0],
                (current_robots[i][1] + velocity_y) % bounds[1]
            )
        count = count_robots_in_quadrants(current_robots, bounds)
        if max_delta < max(count) - min(count):
            max_delta = max(count) - min(count)
            max_delta_index = t
    draw_robots(simulate(robots, max_delta_index, bounds), bounds)
    print(max_delta_index)

robots = list(map(
    parse_robot,
    open("fourteen.input", "r").read().splitlines()
))
bounds = (101, 103)
print(reduce(
    operator.mul,
    count_robots_in_quadrants(simulate(robots, 100, bounds), bounds),
    1
))
draw_simulate(robots, 10000, bounds)
