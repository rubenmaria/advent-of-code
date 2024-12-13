def get_direction(directions: list[str], map: list[list[str]]) -> str:
    for row in map:
        for el in row:
            if el in directions:
                return el
    assert False


def get_position(direction: str, map: list[list[str]]) -> tuple[int, int]:
    for row in range(len(map)):
        for column in range(len(map[0])):
            if map[row][column] == direction:
                return (row, column)
    assert False


def is_cycle_with(map: list[list[str]], obstacle: tuple[int, int]) -> bool:
    if map[obstacle[0]][obstacle[1]] == "#":
        return False

    DIRECTIONS_STRING = [">", "v", "<", "^"]
    DIRECTIONS = [(0, 1), (1, 0), (0, -1), (-1, 0)]
    visited = set()
    obstacle_direction_visited = set()
    current_direction_index = DIRECTIONS_STRING.index(
        get_direction(DIRECTIONS_STRING, map)
    )
    current_position = get_position(DIRECTIONS_STRING[current_direction_index], map)

    while True:
        visited.add(current_position)
        current_direction = DIRECTIONS[current_direction_index]
        new_position = (
            current_position[0] + current_direction[0],
            current_position[1] + current_direction[1],
        )
        if not is_in_bounds(new_position, map):
            return False
        if map[new_position[0]][new_position[1]] == "#" or new_position == obstacle:
            if (new_position, current_direction_index) in obstacle_direction_visited:
                return True
            obstacle_direction_visited.add((new_position, current_direction_index))
            current_direction_index = (current_direction_index + 1) % len(DIRECTIONS)
        else:
            current_position = new_position


def is_in_bounds(x: tuple[int, int], m: list[list[str]]) -> bool:
    return 0 <= x[0] < len(m) and 0 <= x[1] < len(m[0])


DIRECTIONS_STRING = [">", "v", "<", "^"]
DIRECTIONS = [(0, 1), (1, 0), (0, -1), (-1, 0)]
map = list(map(list, open("six.input").read().splitlines()))
visited = set()
current_direction_index = DIRECTIONS_STRING.index(get_direction(DIRECTIONS_STRING, map))
current_position = get_position(DIRECTIONS_STRING[current_direction_index], map)
while True:
    visited.add(current_position)
    current_direction = DIRECTIONS[current_direction_index]
    new_position = (
        current_position[0] + current_direction[0],
        current_position[1] + current_direction[1],
    )
    if not is_in_bounds(new_position, map):
        break
    if map[new_position[0]][new_position[1]] == "#":
        current_direction_index = (current_direction_index + 1) % len(DIRECTIONS)
    else:
        current_position = new_position
print(len(visited))

obstacles = [(y, x) for y in range(len(map)) for x in range(len(map[0]))]
print(len(list(filter(lambda x: is_cycle_with(map, x), obstacles))))
