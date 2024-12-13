def trail_head_endings(
    map: list[list[int]], pos: tuple[int, int]
) -> set[tuple[int, int]]:
    if map[pos[0]][pos[1]] == 9:
        return {pos}
    positions: set[tuple[int, int]] = set()
    for dir in [(1, 0), (-1, 0), (0, 1), (0, -1)]:
        new_pos = (pos[0] + dir[0], pos[1] + dir[1])
        if (
            0 <= new_pos[0] < len(map)
            and 0 <= new_pos[1] < len(map[0])
            and map[new_pos[0]][new_pos[1]] - map[pos[0]][pos[1]] == 1
        ):
            positions |= trail_head_endings(map, new_pos)
    return positions


def trail_head_rating(map: list[list[int]], pos: tuple[int, int]) -> int:
    if map[pos[0]][pos[1]] == 9:
        return 1
    rating = 0
    for dir in [(1, 0), (-1, 0), (0, 1), (0, -1)]:
        new_pos = (pos[0] + dir[0], pos[1] + dir[1])
        if (
            0 <= new_pos[0] < len(map)
            and 0 <= new_pos[1] < len(map[0])
            and map[new_pos[0]][new_pos[1]] - map[pos[0]][pos[1]] == 1
        ):
            rating += trail_head_rating(map, new_pos)
    return rating


hiking_map_raw = open("ten.input", "r").read().splitlines()
hiking_map = [[int(x) for x in row] for row in hiking_map_raw]
trail_heads_indecies = [
    (row, column)
    for row in range(len(hiking_map))
    for column in range(len(hiking_map[0]))
    if hiking_map[row][column] == 0
]
score_sum = sum(
    map(lambda x: len(trail_head_endings(hiking_map, x)), trail_heads_indecies)
)
rating_sum = sum(map(lambda x: trail_head_rating(hiking_map, x), trail_heads_indecies))
print(score_sum)
print(rating_sum)
