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
region_and_perimiers: list[tuple[list[tuple[int, int]], list[tuple[int, int]]]] = list()
visited = set()
for row in range(len(plant_map)):
    for column in range(len(plant_map[0])):
        if (row, column) not in visited:
            new_region = get_region(plant_map, (row, column), set())
            region_and_perimiers.append(
                (list(new_region), get_perimeter(plant_map, new_region))
            )
            visited |= new_region

price = 0
for region,_ in region_and_perimiers:
    visited = set()
    side_count = 0
    for (row,column) in region:
        for (dir_row,dir_column) in [(1,0), (-1,0), (0,1), (0, -1)]:
            side_point = (row + dir_row, column + dir_column)
            region_point = (row + dir_column, column + dir_row)
            if side_point in region:
                continue
            while side_point not in region and region_point in region:
                side_point = (
                    side_point[0] + dir_column,
                    side_point[1] + dir_row
                )
                region_point = (
                    region_point[0] + dir_column,
                    region_point[1] + dir_row
                )
            if (region_point, dir_row, dir_column) not in visited:
                visited.add((region_point, dir_row, dir_column))
                side_count += 1  
    price += side_count * len(region)

print(price)
print(sum(map(lambda x: len(x[0]) * len(x[1]), region_and_perimiers)))
