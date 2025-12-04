from collections import defaultdict
from itertools import combinations
from typing import DefaultDict
import functools


def get_all_substrings(string: str) -> list[str]:
    length = len(string) + 1
    return [string[x:y] for x, y in combinations(range(length), r=2)]


@functools.cache
def exists_towel_sequence_naive(
    towels: tuple,
    design: str
) -> bool:
    if design == "":
        return True

    for i in range(1, len(design) + 1):
        prefix = design[:i]
        if (prefix in towels and
                exists_towel_sequence_naive(towels, design[i:])):
            return True
    return False


@functools.cache
def towel_sequences_naive(
    towels: tuple[str,...],
    design: str
) -> int:
    if design == "":
        return 1
    
    paths = 0
    for towel in towels:
        if design.startswith(towel):
            paths += towel_sequences_naive(towels, design[len(towel):])

    return paths

def get_diffrent_ways(towels: tuple, design: str) -> int:
    towels_in_design = get_all_substrings(design)
    towels_needed = list(set(towels) & set(towels_in_design))
    towels_length: dict[int, set[str]] = DefaultDict(set)
    towels_count: dict[str, int] = defaultdict(int)

    combinations_to_length = {
        i: [
            (x, y) for x in range(i) for y in range(i) if x+y == i
        ]
        for i in range(1, len(design) + 1)
    }

    for i in range(1, len(design) + 1):
        for towel in towels_needed:
            if len(towel) == i:
                towels_count[towel] += 1
                towels_length[i].add(towel)
        for (x, y) in combinations_to_length[i]:
            for prefix in towels_length[x]:
                for suffix in towels_length[y]:
                    new_towel = prefix + suffix
                    if new_towel == design[:i]:
                        new_towel_count = towels_count[prefix] * towels_count[suffix]
                        towels_count[new_towel] += new_towel_count
                        towels_length[i].add(prefix + suffix)
    return towels_count[design]


def exists_towel_sequence(towels: tuple, design: str) -> bool:
    towels_in_design = get_all_substrings(design)
    towels_needed = list(set(towels) & set(towels_in_design))
    towels_length: dict[int, set[str]] = DefaultDict(set)
    combinations_to_length = {
        i: [
            (x, y) for x in range(i) for y in range(i) if x+y == i
        ]
        for i in range(1, len(design) + 1)
    }

    for i in range(1, len(design) + 1):
        for towel in towels_needed:
            if len(towel) == i:
                towels_length[i].add(towel)
        for (x, y) in combinations_to_length[i]:
            for prefix in towels_length[x]:
                for suffix in towels_length[y]:
                    if (prefix + suffix) == design[:i]:
                        towels_length[i].add(prefix + suffix)
    return design in towels_length[len(design)]


def exist_towel_sequence_optimized(towels: tuple, design: str) -> bool:
    is_constructable_length = [False for _ in range(len(design) + 1)]
    is_constructable_length[0] = True

    for i in range(len(design) + 1):
        for j in range(i):
            if is_constructable_length[j] and design[j:i] in towels:
                is_constructable_length[i] = True
                break

    return is_constructable_length[len(design)]


def towel_sequence_paths(towels: tuple, design: str) -> int:
    constructable_length_count = defaultdict(int)
    constructable_length_count[0] = 1

    for i in range(len(design) + 1):
        for j in range(i):
            if constructable_length_count[j] > 0 and design[j:i] in towels:
                constructable_length_count[i] += constructable_length_count[j] * towel_sequence_paths(towels, design[j:i])

    return constructable_length_count[len(design)]


towels_raw = open("nineteen.input").read().split("\n\n")
patterns = tuple(map(lambda x: x.strip(), towels_raw[0].split(",")))
designs = list(filter(lambda x: x != "", map(lambda x: x.strip(), towels_raw[1].split("\n"))))

print(
    len(list(filter(lambda x: exists_towel_sequence_naive(patterns, x), designs)))
)
print(
    sum(map(lambda x: towel_sequences_naive(patterns, x), designs))
)
