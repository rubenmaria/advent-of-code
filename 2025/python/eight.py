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
    circuits: list[set[tuple[int, int, int]]] = []
    for i in range(10):
        min_box = box_with_min_distance_to(boxes, boxes[i])
        print(f"for box={boxes[i]} is min_distace= {min_box}")

        if not any(min_box in circuit for circuit in circuits):
            circuits.append(set([min_box, boxes[i]]))
            continue

        for circuit in circuits:
            if boxes[i] in circuit or min_box in circuit:
                circuit.add(boxes[i])
                circuit.add(min_box)

    print(circuits)


def box_with_min_distance_to(
    boxes: list[tuple[int, int, int]], v: tuple[int, int, int]
) -> tuple[int, int, int]:
    return sorted(boxes, key=lambda x: distance(x, v))[1]


def distance(u: tuple[int, int, int], v: tuple[int, int, int]) -> float:
    return sqrt((u[0] - v[0]) ** 2 + (u[1] - v[1]) ** 2 + (u[2] - v[2]) ** 2)

part_one(boxes)