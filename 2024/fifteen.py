
def get_position(map: list[list[str]]) -> tuple[int, int]:
    for x in range(len(map)):
        for y in range(len(map[0])):
            if map[x][y] == "@": 
                return (x,y)
    raise Exception()


MOVE_TO_DIR = {"<": (0,-1), ">": (0,1), "^": (-1, 0), "v": (1,0)}
map_move_raw = open("dummy-fifteen.input", "r").read().splitlines()
map = list(map(list, map_move_raw[:map_move_raw.index("")]))
moves = list("".join(map_move_raw[map_move_raw.index("")+1:]))
robot_position = get_position(map)
print(map, moves, robot_position)

for move in moves:
    dir = MOVE_TO_DIR[move]
