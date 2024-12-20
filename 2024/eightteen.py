import heapq as h

def generate_map(
    falling_bytes: list[tuple[int, int]],
    falling_bytes_count: int,
    size: int
) -> list[list[str]]:
    byte_positions = falling_bytes[:falling_bytes_count]
    memory: list[list[str]] = []
    for y in range(size):
        memory += [[ 
            "#" if (x, y) in byte_positions else "."
            for x in range(size)
        ]]
    return memory


def draw_map(memory: list[list[str]]) -> None:
    for row in memory:
        print("".join(row))

def get_neighbors(
    position: tuple[int, int],
    memory: list[list[str]]
) -> list[tuple[int, int]]:
    neighbors: list[tuple[int, int]] = []
    for dir in [(1, 0), (-1, 0), (0, 1), (0, -1)]:
        neighbor = (position[0] + dir[0], position[1] + dir[1])
        if not (0 <= neighbor[0] < len(memory) 
            and 0 <= neighbor[1] < len(memory)):
            continue
        if memory[neighbor[0]][neighbor[1]] == ".":
            neighbors += [(neighbor)]
    return neighbors

def dijkstra(
    start: tuple[int,int],
    end: tuple[int, int],
    memory: list[list[str]],
) -> dict[tuple[int, int], float]:
    to_visit = [(float(0), start)]
    distances = {
        (x,y) : float("inf")
        for x in range(len(memory[0])) for y in range(len(memory))
    }
    distances[start] = 0
    visited = set()
    previous = {}

    while len(to_visit) > 0:
        _, position = h.heappop(to_visit)
        if position == end:
            break
        if position in visited:
            continue
        visited.add(position)
        for neighbor in get_neighbors(position, memory):
            if distances[position] + 1 <= distances[neighbor]:
                distances[neighbor] = distances[position] + 1
                previous[neighbor] = position
            h.heappush(to_visit, (distances[neighbor], neighbor))
    return distances


falling_bytes: list[tuple[int, int]] = list(
    map(eval, open("eightteen.input").read().splitlines())
)
size = 71
fallen_count = 2850

while True:
    memory = generate_map(falling_bytes, fallen_count, size)
    distances = dijkstra((0,0), (70, 70), memory)
    draw_map(memory)
    if distances[(70,70)] == float("inf"):
        break
    fallen_count += 1
    print(fallen_count)

print(falling_bytes[fallen_count-1])
