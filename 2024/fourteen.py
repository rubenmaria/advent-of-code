def parse_robot(raw: str) -> tuple[tuple[int, int], tuple[int, int]]:
    (position_raw, velocity_raw) = raw.split()
    (position_raw_x, position_raw_y) = position_raw.split(",")
    (velocity_raw_x, velocity_raw_y) = velocity_raw.split(",")
    position_x = int(position_raw_x.split("=")[1])
    position_y = int(position_raw_y)
    velocity_x = int(velocity_raw_x.split("=")[1])
    velocity_y = int(velocity_raw_y)
    return ((position_x, position_y), (velocity_x, velocity_y))


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


robots = list(map(
    parse_robot,
    open("dummy-fourteen.input", "r").read().splitlines()
))
print(robots)
