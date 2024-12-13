import copy


def get_region(
    map: list[list[str]], pos: tuple[int, int], visited: set[tuple[int, int]]
) -> set[tuple[int, int]]:
    region = {pos}
    visited.add(pos)
    for dir in [(1, 0), (-1, 0), (0, 1), (0, -1)]:
        new_pos = (pos[0] + dir[0], pos[1] + dir[1])
        if (
            0 <= new_pos[0] < len(map)
            and 0 <= new_pos[1] < len(map[0])
            and map[pos[0]][pos[1]] == map[new_pos[0]][new_pos[1]]
            and new_pos not in visited
        ):
            region |= get_region(map, new_pos, visited)
    return region


def get_perimeter(
    map: list[list[str]], region: set[tuple[int, int]]
) -> list[tuple[int, int]]:
    fences = list()
    for row, column in region:
        for dir in [(1, 0), (-1, 0), (0, 1), (0, -1)]:
            new_pos = (row + dir[0], column + dir[1])
            if (
                not (0 <= new_pos[0] < len(map))
                or not (0 <= new_pos[1] < len(map[0]))
                or map[row][column] != map[new_pos[0]][new_pos[1]]
            ):
                fences.append(new_pos)
    return fences


def has_neighbor(
    fences: list[tuple[int, int]], fence: tuple[int, int]
) -> tuple[int, int] | None:
    (row, column) = fence
    for dir in [(1, 0), (-1, 0), (0, 1), (0, -1)]:
        new_pos = (row + dir[0], column + dir[1])
        if new_pos in fences:
            return new_pos
    return None


plant_map = list(map(list, open("twelve.input", "r").read().splitlines()))
region_and_perimiers: list[tuple[set[tuple[int, int]], list[tuple[int, int]]]] = list()
visited = set()
for row in range(len(plant_map)):
    for column in range(len(plant_map[0])):
        if (row, column) not in visited:
            new_region = get_region(plant_map, (row, column), set())
            region_and_perimiers.append(
                (new_region, get_perimeter(plant_map, new_region))
            )
            visited |= new_region

region_sides_and_perimeters = []
for p, fences in region_and_perimiers:
    fences_left: list[tuple[int, int]] = copy.deepcopy(sorted(fences))
    sides: list[tuple[int, int]] = []
    while len(fences_left) > 0:
        side = fences_left.pop(0)
        if neighbor := has_neighbor(fences_left, side):
            direction = (
                abs(neighbor[0] - side[0]),
                abs(neighbor[1] - side[1]),
            )
            neighbor_one = (
                side[0] + direction[0],
                side[1] + direction[1],
            )
            while neighbor_one in fences_left:
                fences_left.remove(neighbor_one)
                neighbor_one = (
                    neighbor_one[0] + direction[0],
                    neighbor_one[1] + direction[1],
                )

            neighbor_two = (
                side[0] - direction[0],
                side[1] - direction[1],
            )
            while neighbor_two in fences_left:
                fences_left.remove(neighbor_two)
                neighbor_two = (
                    neighbor_two[0] - direction[0],
                    neighbor_two[1] - direction[1],
                )
        sides.append(side)
    region_sides_and_perimeters.append((p, sides))

print(sum(map(lambda x: len(x[0]) * len(x[1]), region_and_perimiers)))
print(sum(map(lambda x: len(x[0]) * len(x[1]), region_sides_and_perimeters)))
