from math import prod, sqrt

boxes = list(
    map(
        lambda x: (int(x.split(",")[0]), int(x.split(",")[1]), int(x.split(",")[2])),
        open("real.input", "r").read().splitlines(),
    )
)


def part_one(boxes: list[tuple[int, int, int]], n: int):
    circuits: list[set[tuple[int, int, int]]] = [set([x]) for x in boxes]
    for u, v in box_pairs_with_min_distance(boxes)[:n]:
        mergeable_circuits = [i for i, x in enumerate(circuits) if u in x or v in x]
        parent_circuit_index = mergeable_circuits.pop()
        for i in mergeable_circuits:
            circuits[parent_circuit_index] = circuits[parent_circuit_index].union(
                circuits[i]
            )
            circuits.remove(circuits[i])

    biggest_three_circuits = sorted(circuits, key=lambda x: len(x), reverse=True)[:3]
    print(f"solution={prod(map(len, biggest_three_circuits))}")


def box_pairs_with_min_distance(
    boxes: list[tuple[int, int, int]],
) -> list[tuple[tuple[int, int, int], tuple[int, int, int]]]:
    pairs = [
        (boxes[i], boxes[j])
        for i in range(len(boxes))
        for j in range(i + 1, len(boxes))
    ]
    return sorted(pairs, key=lambda x: distance(x[0], x[1]))


def distance(u: tuple[int, int, int], v: tuple[int, int, int]) -> float:
    return sqrt((u[0] - v[0]) ** 2 + (u[1] - v[1]) ** 2 + (u[2] - v[2]) ** 2)


def part_two(boxes: list[tuple[int, int, int]]):
    circuits: list[set[tuple[int, int, int]]] = [set([x]) for x in boxes]
    for u, v in box_pairs_with_min_distance(boxes):
        mergeable_circuits = [i for i, x in enumerate(circuits) if u in x or v in x]
        parent_circuit_index = mergeable_circuits.pop()
        for i in mergeable_circuits:
            circuits[parent_circuit_index] = circuits[parent_circuit_index].union(
                circuits[i]
            )
            circuits.remove(circuits[i])

        if len(circuits) == 1:
            print(f"solution2={u[0] * v[0]}")
            break


part_one(boxes, 1000)
part_two(boxes)
