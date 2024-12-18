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
        print("hallo", new_position)
        move_big_box(map, get_big_box(map, new_position), dir)
        if map[new_position[0]][new_position[1]] == ".":
            map[new_position[0]][new_position[1]] = symbol_old_position
            map[position[0]][position[1]] = "."
            return new_position
    return position

def move_big_box(
    map: list[list[str]],
    positions: tuple[tuple[int, int], tuple[int, int]],
    dir: tuple[int, int]
) -> None:
    (left_part, right_part) = positions
    new_position_left = (left_part[0] + dir[0], left_part[1] + dir[1])
    new_position_right = (right_part[0] + dir[0], right_part[1] + dir[1])
    new_symbol_left = map[new_position_left[0]][new_position_left[1]]
    new_symbol_right = map[new_position_right[0]][new_position_right[1]]
    if dir in [(-1,0), (1,0)]:
        if "#" in [new_symbol_left, new_position_right]:
            return
        if map[new_position_left[0]][new_position_left[1]] in ["[", "]"]:
            move_big_box(map, get_big_box(map, new_position_left), dir)
        if map[new_position_right[0]][new_position_right[1]] in ["[", "]"]:
            move_big_box(map, get_big_box(map, new_position_right), dir)
        if (map[new_position_right[0]][new_position_right[1]] == "." and 
                map[new_position_left[0]][new_position_left[1]] == "."):
            map[new_position_left[0]][new_position_left[1]] = "[" 
            map[new_position_right[0]][new_position_right[1]] = "]" 
            map[left_part[0]][left_part[1]] = "."
            map[right_part[0]][right_part[1]] = "."
    elif dir == (0, 1):
        if new_symbol_right == "#":
            return
        if map[new_position_right[0]][new_position_right[1]] == "[":
            move_big_box(map, get_big_box(map, new_position_right), dir)
        if map[new_position_right[0]][new_position_right[1]] == ".":
            map[new_position_left[0]][new_position_left[1]] = "[" 
            map[new_position_right[0]][new_position_right[1]] = "]" 
            map[left_part[0]][left_part[1]] = "."
    else:
        if new_symbol_left == "#":
            return
        print(new_position_left)
        print(map[new_position_left[0]][new_position_left[1]])
        if map[new_position_left[0]][new_position_left[1]] == "]":
            move_big_box(map, get_big_box(map, new_position_left), dir)
        if map[new_position_left[0]][new_position_left[1]] == ".":
            map[new_position_left[0]][new_position_left[1]] = "[" 
            map[new_position_right[0]][new_position_right[1]] = "]" 
            map[right_part[0]][right_part[1]] = "."
        print(map)


def get_big_box(
    map: list[list[str]],
    p: tuple[int, int]
) -> tuple[tuple[int, int], tuple[int, int]]:
    if map[p[0]][p[1]] == "[":
        return (p, (p[0], p[1] + 1))
    if map[p[0]][p[1]] == "]":
        return ((p[0], p[1] - 1), p)
    raise Exception()



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


def get_all_bigger_box_positions(map: list[list[str]]) -> list[tuple[int, int]]:
    boxes = []
    for y in range(len(map)):
        for x in range(len(map[0])):
            if map[y][x] == "[":
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
        new_map += [list("".join(current_row))]
    return new_map


MOVE_TO_DIR = {"<": (0, -1), ">": (0, 1), "^": (-1, 0), "v": (1, 0)}
map_move_raw = open("fifteen.input", "r").read().splitlines()
map_robot = list(map(list, map_move_raw[:map_move_raw.index("")]))
moves = list("".join(map_move_raw[map_move_raw.index("")+1:]))
robot_position = get_position(map_robot)
bigger_map = construct_new_map(map_robot.copy())
robot_position_bigger = get_position(bigger_map)
draw_map(map_robot)
draw_map(bigger_map)

for move_symbol in moves:
    dir = MOVE_TO_DIR[move_symbol]
    robot_position = move(map_robot, robot_position, dir)
    robot_position_bigger = move_bigger(bigger_map, robot_position_bigger, dir)


draw_map(map_robot)
draw_map(bigger_map)
print(sum(map(lambda x: 100*x[0] + x[1], get_all_box_positions(map_robot))))
print(sum(map(lambda x: 100*x[0] + x[1], get_all_bigger_box_positions(bigger_map))))
