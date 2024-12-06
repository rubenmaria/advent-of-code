def get_direction(directions: list[str], map: list[list[str]]) -> str:
    for row in map:
        for el in row:
            if el in directions:
                return el
    assert False


def get_position(direction: str, map: list[list[str]]) -> tuple[int,int]:
    for row in range(len(map)):
        for column in range(len(map[0])):
            if map[row][column]  == direction:
                return (row, column)
    assert False

DIRECTIONS = [">", "<", "^", "v"]
map = list(map(list, open("dummy-six.input").read().splitlines()))
visited = set()

while True:
    current_visited = set()
    current_direction = get_direction(DIRECTIONS, map)
    current_position = get_position(current_direction, map)
    new_poistion = current_position
    index_object = len(map[0])

    if current_direction == ">": 
        right_of_guard = map[current_position[0]][current_position[1]+1:]
        if "#" in right_of_guard:
            index_object = right_of_guard.index("#") + current_position[1] + 1
            current_visited |= set(
                [(current_position[0], x) for x in range(current_position[1], index_object)]
            )
        current_direction = "v"
        new_poistion = (current_position[0], index_object - 1)
    elif current_direction == "<": 
        left_of_guard = map[current_position[0]][:current_position[1]-1]
        if "#" in left_of_guard:
            index_object = left_of_guard.index("#")
            current_visited |= set(
                [(current_position[0], x) for x in range(index_object+1, current_position[1] + 1)]
            )
        new_poistion = (current_position[0], index_object - 1)
    elif current_direction == "^": 
        up_of_guard = [x[current_position[1]] for x in map[:current_position[0]]]
        if "#" in up_of_guard:
            index_object = up_of_guard.index("#")
            current_visited |= set(
                [(x,current_position[1]) for x in range(index_object+1, current_position[0] + 1)]
            )
        current_direction = ">"
        new_poistion = (current_position[0], index_object - 1)
    elif current_direction == "v": 
        down_of_guard = [x[current_position[1]] for x in map[current_position[0]+1:]]
        if "#" in down_of_guard:
            index_object = down_of_guard.index("#") + current_position[0] + 1
            current_visited |= set(
                [(x,current_position[1]) for x in range(current_position[0], index_object)]
            )
        current_direction = "<"
        new_poistion = (current_position[0], index_object - 1)
    print(current_visited)
    if current_visited | visited == visited:
        break
    visited = current_visited | visited
    
print(len(visited))
