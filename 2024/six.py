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


def print_visited(v: set[tuple[int, int]], map: list[list[str]]) -> None:
    for row in range(len(map)):
        for column in range(len(map[0])):
            if (row, column) in v and map[row][column] != "#":
                print("X", end="")
            else:
                print(map[row][column], end="")
        print("\n")


DIRECTIONS = [">", "<", "^", "v"]
map = list(map(list, open("six.input").read().splitlines()))
visited = set()
current_direction = get_direction(DIRECTIONS, map)
current_position = get_position(current_direction, map)

while True:
    old_visited_length = len(visited)
    if current_direction == ">":
        right_of_guard = map[current_position[0]][current_position[1] + 1:]
        print("right of guard: ", right_of_guard)
        if "#" in right_of_guard:
            index_object = current_position[1] + right_of_guard.index("#") + 1
            visited |= set(
                [
                    (current_position[0], x)
                    for x in range(current_position[1], index_object)
                ]
            )
            current_direction = "v"
            current_position = (current_position[0], index_object - 1)
        else:
            visited |= set(
                    [
                        (current_position[0], x)
                        for x in range(current_position[1], len(map[0]))
                    ]
            )
            break
    elif current_direction == "<":
        left_of_guard = map[current_position[0]][:current_position[1]]
        left_of_guard = left_of_guard[::-1]
        print("left of guard: ", left_of_guard)
        if "#" in left_of_guard:
            index_object = len(left_of_guard) - 1 - left_of_guard.index("#")
            visited |= set(
                [
                    (current_position[0], x)
                    for x in range(index_object + 1, current_position[1] + 1)
                ]
            )
            current_position = (current_position[0], index_object + 1)
            current_direction = "^"
        else:
            visited |= set(
                    [
                        (current_position[0], x)
                        for x in range(0, current_position[1] + 1)
                    ]
            )
            break
    elif current_direction == "^":
        up_of_guard = [x[current_position[1]] for x in map[:current_position[0]]]
        up_of_guard = up_of_guard[::-1]
        print("up of guard: ", up_of_guard)
        if "#" in up_of_guard:
            index_object = len(up_of_guard) - 1 - up_of_guard.index("#")
            visited |= set(
                [
                    (y, current_position[1])
                    for y in range(index_object + 1, current_position[0] + 1)
                ]
            )
            current_direction = ">"
            current_position = (index_object + 1, current_position[1])
        else:
            visited |= set(
                    [
                        (y, current_position[1])
                        for y in range(0, current_position[1] + 1)
                    ]
            )
            break
    elif current_direction == "v":
        down_of_guard = [x[current_position[1]] for x in map[current_position[0]+1:]]
        print("down of guard: ", down_of_guard)
        if "#" in down_of_guard:
            index_object = current_position[0] + 1 + down_of_guard.index("#")
            visited |= set(
                [
                    (y, current_position[1])
                    for y in range(current_position[0], index_object)
                ]
            )
            current_direction = "<"
            current_position = (index_object - 1, current_position[1])
        else:
            visited |= set(
                    [
                        (y, current_position[1])
                        for y in range(current_position[1], len(map))
                    ]
            )
            break
    print("new position: ", current_position)
    if old_visited_length == len(visited):
        print("CYCLE :(")
        break

print_visited(visited, map)
print(len(visited))
