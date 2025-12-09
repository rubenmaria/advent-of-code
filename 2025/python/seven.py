from copy import deepcopy
from functools import lru_cache

tachyon_map = list(map(list, open("real.input", "r").read().splitlines()))
print(tachyon_map)


def part_one(map: list[list[str]]):
    start_column = map[0].index("S")
    beams = set([(1, start_column)])
    beams_splitted = 0
    while True:
        # visualize_map(map)
        old_beams = deepcopy(beams)
        beams = set()

        for row, column in old_beams:
            updated_row, updated_column = (row + 1, column)
            if not in_bounds(map, (updated_row, updated_column)):
                continue

            if map[updated_row][updated_column] == ".":
                beams.add((updated_row, updated_column))
            else:
                beams_splitted += 1
                left = (updated_row, updated_column - 1)
                right = (updated_row, updated_column + 1)
                if in_bounds(map, right):
                    beams.add(right)
                if in_bounds(map, left):
                    beams.add(left)

        if beams == old_beams:
            break

    print(f"solution1={beams_splitted}")


def visualize_map(map: list[list[str]]):
    for row in map:
        print("".join(row))


def in_bounds(map: list[list], position: tuple[int, int]) -> bool:
    if map == []:
        return False
    row, column = position
    return row in range(len(map)) and column in range(len(map[0]))


def part_two(map: list[list[str]]):
    start_column = map[0].index("S")
    time_splits = time_line_simulator((0, start_column))
    print(f"solution2={time_splits}")


@lru_cache()
def time_line_simulator(node: tuple[int, int]) -> int:
    row, column = node
    updated_row, updated_column = (row + 1, column)
    updated_node = (updated_row, updated_column)
    time_lines = 0

    while (
        in_bounds(tachyon_map, updated_node)
        and tachyon_map[updated_row][updated_column] == "."
    ):
        row, column = updated_node
        updated_row, updated_column = (row + 1, column)
        updated_node = (updated_row, updated_column)

    if (
        in_bounds(tachyon_map, updated_node)
        and tachyon_map[updated_row][updated_column] == "^"
    ):
        left = (updated_row, updated_column - 1)
        right = (updated_row, updated_column + 1)
        if in_bounds(tachyon_map, right):
            time_lines += time_line_simulator(right)
        if in_bounds(tachyon_map, left):
            time_lines += time_line_simulator(left)

    if len(tachyon_map) <= updated_row:
        return time_lines + 1
    else:
        return time_lines


part_one(tachyon_map)
part_two(tachyon_map)
