from copy import deepcopy
from math import sqrt

boxes = list(
    map(
        lambda x: (int(x.split(",")[0]), int(x.split(",")[1]), int(x.split(",")[2])),
        open("test.input", "r").read().splitlines(),
    )
)
print(boxes)


def part_one(boxes: list[tuple[int, int, int]]):
    visited = set()
    for box in boxes:
        for other in boxes:
            if other == box:
                continue


def min_distance(
    boxes: list[tuple[int, int, int]], v: tuple[int, int, int]
) -> tuple[int, int, int]:
    x = deepcopy(boxes)
    x.remove(v)
    return (0, 0, 0)


def distance(u: tuple[int, int, int], v: tuple[int, int, int]) -> float:
    return sqrt((u[0] - v[0]) ** 2 + (u[1] - v[1]) ** 2 + (u[2] - v[2]) ** 2)
