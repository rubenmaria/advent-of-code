from functools import reduce
from itertools import combinations, combinations_with_replacement
from operator import xor


def parse_lights(light: str) -> int:
    bits = 0
    for i, x in enumerate(light.strip("[]")):
        if x == "#":
            bits |= 1 << (i)
    return bits


def parse_buttons(row: list[str]) -> list[int]:
    buttons = list(
        map(
            lambda x: list(map(int, x.strip("()").split(","))),
            list(filter(lambda x: x.startswith("("), row)),
        )
    )
    operations = []
    for button in buttons:
        bits = 0
        for light_toggle in button:
            bits |= 1 << light_toggle
        operations.append(bits)
    return operations


def parse_buttons_non_binary(row: list[str]) -> list[list[int]]:
    return list(
        map(
            lambda x: list(map(int, x.strip("()").split(","))),
            list(filter(lambda x: x.startswith("("), row)),
        )
    )


def parse_joltage(joltage: str) -> list[int]:
    return list(map(int, joltage.strip("{}").split(",")))


manual = list(map(lambda x: x.split(" "), open("real.input").read().splitlines()))
lights = [parse_lights(x) for row in manual for x in row if x.startswith("[")]
buttons = [parse_buttons(row) for row in manual]
buttons_joltage = [parse_buttons_non_binary(row) for row in manual]
joltage = [parse_joltage(x) for row in manual for x in row if x.startswith("{")]


def part_one(lights: list[int], operations: list[list[int]]):
    min_presses = []
    for light_pattern, operation_set in zip(lights, operations):
        if light_pattern in operation_set:
            min_presses += [1]
            continue
        min = 0
        for i in range(2, len(operation_set)):
            for comb in combinations(operation_set, i):
                if reduce(xor, comb) == light_pattern:
                    min = i
                    break
            if min > 0:
                min_presses.append(min)
                break
    print(f"solution1={sum(min_presses)}")


def part_two(joltages: list[list[int]], operations: list[list[list[int]]]):
    min_presses = []
    for i, (joltage_pattern, operation_set) in enumerate(zip(joltages, operations)):
        print(f"{i + 1}/{len(joltages)}")
        min = 0
        for i in range(max(joltage_pattern), sum(joltage_pattern)):
            for comb in combinations_with_replacement(operation_set, i):
                if is_correct_button_combination(comb, joltage_pattern):
                    min = i
                    break
            if min > 0:
                min_presses.append(min)
                break
    print(f"solution1={sum(min_presses)}")


def is_correct_button_combination(buttons: tuple, joltage_pattern: list[int]) -> bool:
    joltage = [0 for _ in range(len(joltage_pattern))]
    for button in buttons:
        for i in button:
            joltage[i] += 1

    return joltage == joltage_pattern


part_one(lights, buttons)
part_two(joltage, buttons_joltage)
