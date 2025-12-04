from copy import deepcopy

map = list(map(list, open("real.input", "r").read().splitlines()))
print(map)


def part_one(map: list[list[str]]):
    directions = [(1, 0), (-1, 0), (0, 1), (0, -1), (1, 1), (1, -1), (-1, 1), (-1, -1)]
    new_map = deepcopy(map)
    rolls_reachable = 0
    for row in range(len(map)):
        for column in range(len(map[0])):
            if map[row][column] != "@":
                continue
            neigbor_count = 0
            for y, x in directions:
                if row + y not in range(len(map)) or column + x not in range(
                    len(map[0])
                ):
                    continue

                if map[row + y][column + x] == "@":
                    neigbor_count += 1

            if neigbor_count < 4:
                new_map[row][column] = "x"
                rolls_reachable += 1

    visualize_map(new_map)
    print(f"solution1={rolls_reachable}")


def visualize_map(map: list[list[str]]):
    for row in range(len(map)):
        print("".join(map[row]))


def part_two(map: list[list[str]]):
    directions = [(1, 0), (-1, 0), (0, 1), (0, -1), (1, 1), (1, -1), (-1, 1), (-1, -1)]
    rolls_reachable = 0
    new_map = deepcopy(map)
    while True:
        for row in range(len(map)):
            for column in range(len(map[0])):
                if map[row][column] != "@":
                    continue
                neigbor_count = 0
                for y, x in directions:
                    if row + y not in range(len(map)) or column + x not in range(
                        len(map[0])
                    ):
                        continue

                    if map[row + y][column + x] == "@":
                        neigbor_count += 1

                if neigbor_count < 4:
                    new_map[row][column] = "."
                    rolls_reachable += 1

        visualize_map(new_map)
        print("=" * 40)

        if new_map == map:
            break

        map = deepcopy(new_map)
    print(f"solution2={rolls_reachable}")


part_one(map)
part_two(map)
