def get_position(map: list[list[str]]) -> tuple[int, int]:
    for x in range(len(map)):
        for y in range(len(map[0])):
            if map[x][y] == "@":
                return (x, y)
    raise Exception()


def move(
    map: list[list[str]],
    position: tuple[int, int],
    direciton: tuple[int, int]
) -> tuple[int, int]:
    new_position = (
        position[0] + direciton[0],
        position[1] + direciton[1]
    )
    symbol_new_position = map[new_position[0]][new_position[1]]
    symbol_old_position = map[position[0]][position[1]]
    if symbol_new_position == "#":
        return position
    if symbol_new_position == ".":
        map[new_position[0]][new_position[1]] = symbol_old_position
        map[position[0]][position[1]] = "."
        return new_position
    if symbol_new_position == "O":
        move(map, new_position, direciton)
        if map[new_position[0]][new_position[1]] == ".":
            map[new_position[0]][new_position[1]] = symbol_old_position
            map[position[0]][position[1]] = "."
            return new_position
    return position


def move_bigger(
    map: list[list[str]],
    position: tuple[int, int],
    direciton: tuple[int, int]
) -> tuple[int, int]:
    new_position = (
        position[0] + direciton[0],
        position[1] + direciton[1]
    )
    symbol_new_position = map[new_position[0]][new_position[1]]
    symbol_old_position = map[position[0]][position[1]]
    if symbol_new_position == "#":
        return position
    if symbol_new_position == ".":
        map[new_position[0]][new_position[1]] = symbol_old_position
        map[position[0]][position[1]] = "."
        return new_position
    if symbol_new_position in ["[", "]"]:
        (box_left, box_right) = get_big_box(map, new_position)
        box_neighbor = []
        move(map, new_position, direciton)
        if map[new_position[0]][new_position[1]] == ".":
            map[new_position[0]][new_position[1]] = symbol_old_position
            map[position[0]][position[1]] = "."
            return new_position
    return position


def get_big_box(
    map: list[list[str]],
    p: tuple[int, int]
) -> tuple[tuple[int, int], tuple[int, int]]:
    if map[p[0]][p[1]] == "[":
        return (p, (p[0], p[1] + 1))
    if map[p[0]][p[1]] == "]":
        return (p, (p[0], p[1] - 1))
    raise Exception()

def get_box_neighbor_to_move(
    map: list[list[str]],
    box: tuple[tuple[int, int], tuple[int, int]],
    dir: tuple[int, int]
) -> list[tuple[int, int]]:
    new_positions = (
        (box[0][0] + dir[0], box[0][1] + dir[1]),
        (box[1][0] + dir[0], box[1][1] + dir[1])
    )
    new_symbols = (
        map[new_positions[0][0]][new_positions[0][0]],
        map[new_positions[1][0]][new_positions[1][0]],
    )
    if dir in [(0,1), (0,-1)] and new_symbols == ("[","]"):
        pass
    return []


def draw_map(map: list[list[str]]) -> None:
    for row in map:
        print("".join(row))


def get_all_box_positions(map: list[list[str]]) -> list[tuple[int, int]]:
    boxes = []
    for y in range(len(map)):
        for x in range(len(map[0])):
            if map[y][x] == "O":
                boxes += [(y, x)]
    return boxes


def construct_new_map(map: list[list[str]]) -> list[list[str]]:
    new_map = []
    for row in map:
        current_row = []
        for element in row:
            if element == "#":
                current_row += ["##"]
            elif element == "O":
                current_row += ["[]"]
            elif element == "@":
                current_row += ["@."]
            else:
                current_row += [".."]
        new_map += ["".join(current_row)]
    return new_map


MOVE_TO_DIR = {"<": (0, -1), ">": (0, 1), "^": (-1, 0), "v": (1, 0)}
map_move_raw = open("dummy-fifteen-2.input", "r").read().splitlines()
map_robot = list(map(list, map_move_raw[:map_move_raw.index("")]))
moves = list("".join(map_move_raw[map_move_raw.index("")+1:]))
robot_position = get_position(map_robot)
bigger_map = construct_new_map(map_robot.copy())
draw_map(map_robot)

for move_symbol in moves:
    dir = MOVE_TO_DIR[move_symbol]
    robot_position = move(map_robot, robot_position, dir)

draw_map(map_robot)
draw_map(bigger_map)
print(sum(map(lambda x: 100*x[0] + x[1], get_all_box_positions(map_robot))))
