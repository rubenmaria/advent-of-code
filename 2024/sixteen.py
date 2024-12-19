from collections import defaultdict
from enum import Enum
import heapq as h
import math
from typing import TypeAlias

Point: TypeAlias = tuple[int, int]
State: TypeAlias = tuple[Point, Point]

class Direction(Enum):
    EAST = 1
    NORTH = 2
    WEST = 3
    SOUTH = 4

    def __lt__(self, other):
        if self.__class__ is other.__class__:
            return self.value < other.value
        return NotImplemented

TUPLE_TO_DIRECTION = {
    (0, -1): Direction.WEST,
    (0, 1): Direction.EAST, 
    (1, 0): Direction.SOUTH,
    (-1, 0): Direction.NORTH
}

TURN_90_CLOCKWISE = {
    (-1, 0): (0, 1),
    (0, 1): (1, 0),
    (1, 0): (0, -1),
    (0, -1): (-1, 0)

}

TURN_90_COUNTER_CLOCKWISE = {
    (0, 1): (-1, 0),
    (-1, 0): (0, -1),
    (0, -1): (1, 0),
    (1, 0): (0, 1)
}

def draw_maze(maze: list[list[str]]):
    for row in maze:
        print("".join(row))


def get_special_position(maze: list[list[str]], symbol: str) -> tuple[int, int]:
    for row in range(len(maze)):
        for column in range(len(maze[0])):
            if maze[row][column] == symbol:
                return (row, column)
    raise Exception()

def get_neighbors(
    maze: list[list[str]],
    node: tuple[tuple[int, int], Direction]
) -> list[tuple[tuple[tuple[int, int], Direction], int]]:
    neighbors: list[tuple[tuple[tuple[int, int], Direction], int]] = []
    (node_pos, node_dir) = node
    for tuple_dir in [(-1, 0), (1, 0), (0, 1), (0, -1)]:
        new_position = (node_pos[0] + tuple_dir[0], node_pos[1] + tuple_dir[1])
        if maze[new_position[0]][new_position[1]] == "#":
            continue
        direction = TUPLE_TO_DIRECTION[tuple_dir]
        cost = 1 + 1000 * min(
            (direction.value - node_dir.value) % 4,
            (node_dir.value - direction.value) % 4
        )
        neighbors += [((new_position, direction), cost)]
    #print(f"current_node: {node}, neighbors: {neighbors}")
    return neighbors

def get_state_neighbors(
    maze: list[list[str]],
    current_state: State
) -> list[tuple[State, int]]:
    neighbors: list[tuple[State, int]] = []
    ((row, column), dir) = current_state
    new_position = (row + dir[0], column + dir[1])
    neighbors += [
        (((row, column), TURN_90_CLOCKWISE[dir]), 1000),
        (((row, column), TURN_90_COUNTER_CLOCKWISE[dir]), 1000),
    ]
    if maze[new_position[0]][new_position[1]] != "#":
        neighbors += [((new_position, dir), 1)]
    return neighbors

def shortest_pahth(
    end_position: tuple[int, int],
    prev: dict[tuple[int, int], tuple[int, int]]) -> list[tuple[int, int]]:
    path = [end_position]
    current_node = end_position
    while current_node in prev.keys():
        current_node = prev[current_node]
        path.insert(0, current_node)
    return path

def dijkstra(
    starting_position: tuple[int, int],
    direction: Direction,
    maze: list[list[str]]
) -> tuple[dict[tuple[int, int], float], dict[tuple[int, int], set[tuple[int, int]]]]:
    to_process = []
    h.heappush(to_process, (0,(starting_position, direction)))
    processed = set()
    distance = {
        (row,column) : math.inf
        for row in range(len(maze)) for column in range(len(maze[0]))
    }
    distance[starting_position] = 0
    prev = defaultdict(set)

    while len(to_process) > 0:
        current_node = h.heappop(to_process)[1]
        if current_node[0] in processed:
            continue
        processed.add(current_node[0])
        for (neigbor, cost) in get_neighbors(maze, current_node):
            if distance[current_node[0]] + cost <= distance[neigbor[0]]:
                distance[neigbor[0]] = distance[current_node[0]] + cost
                prev[neigbor[0]].add(current_node[0])
                print(f"from={current_node}; to={neigbor}; cost={cost}")
            h.heappush(to_process, (distance[neigbor[0]], neigbor))
    return distance, prev

def dijkstra_with_states(
    start_state: State,
    end_position: Point,
    maze: list[list[str]]
) -> tuple[dict[State,float], dict[State, set[State]]]:
    to_process: list[tuple[float, State]] = []
    h.heappush(to_process, (0, start_state))
    visited: set[State] = set()
    costs: dict[State,float] = {}
    costs[start_state] = 0
    previous_nodes: dict[State, set[State]] = defaultdict(set)

    while len(to_process) > 0:
        current_state = h.heappop(to_process)[1]
        if current_state[0] == end_position:
            break
        if current_state in visited:
            continue
        visited.add(current_state)
        for (neighbor, cost) in get_state_neighbors(maze, current_state):
            current_cost = costs[neighbor] if neighbor in costs.keys() else float("inf")
            new_cost = costs[current_state] + cost 
            if new_cost <= current_cost:
                costs[neighbor] = new_cost
                previous_nodes[neighbor].add(current_state)
            h.heappush(to_process, (costs[neighbor], neighbor))

    return costs, previous_nodes

def get_shortes_path_graph(
    starting_position: tuple[int, int],
    end_position: tuple[int, int],
    maze: list[list[str]]
) -> dict[tuple[tuple[int, int], Direction], set[tuple[tuple[int, int], Direction]]]:
    distances_to_start = dijkstra(starting_position, Direction.EAST, maze)[0]
    distances_to_end = dijkstra(end_position, Direction.NORTH, maze)[0]

    neighbors = defaultdict(set)
    to_process = [(starting_position, Direction.EAST)]
    processed = set()

    while len(to_process) > 0:
        current_node = to_process.pop()
        if current_node in processed:
            continue
        processed.add(current_node)
        for (neigbor, cost) in get_neighbors(maze, current_node):
            to_process.append(neigbor)
            start_to_current = distances_to_start[current_node[0]]
            end_to_neighbor = distances_to_end[neigbor[0]]
            shortest_path_length = distances_to_start[end_position]
            if start_to_current + cost + end_to_neighbor == shortest_path_length:
                neighbors[neigbor].add(current_node)
    return neighbors

def traverse_shortest_pahts(
    end_position: State,
    graph: dict[State, set[State]]
) -> set[Point]:
    visited = {end_position[0]}
    for u in graph[end_position]:
        visited |= traverse_shortest_pahts(u, graph)
    return visited

maze = list(map(list, open("sixteen.input", "r").read().splitlines()))
draw_maze(maze)
starting_position = get_special_position(maze, "S")
end_position = get_special_position(maze, "E")
costs, previous_nodes = dijkstra_with_states(
    (starting_position, (0, 1)),
    end_position,
    maze
)
print(sum(filter( lambda x: x > 1, [
    len(traverse_shortest_pahts((end_position, dir), previous_nodes)) 
    for dir in [(1,0), (0, 1), (-1, 0), (0, -1)]
])))
print([
    costs[(end_position, dir)]
    for dir in [(1,0), (0, 1), (-1, 0), (0, -1)]
    if (end_position, dir) in  costs.keys()
][0])
