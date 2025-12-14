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


manual = list(map(lambda x: x.split(" "), open("test.input").read().splitlines()))
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


def part_two(joltages, buttons):
    total = 0
    for i, (t, b) in enumerate(zip(joltages, buttons), 1):
        print(f"{i}/{len(joltages)}")
        a = joltage_and_buttons_to_matrix(t, b)
        a = transfrom_matrix_in_row_echolon_form(a)
        print(a)
        x = search_in_back_substitution(a)
        print(x)

    print("solution2 =", total)


def joltage_and_buttons_to_matrix(
    joltage: list[int], buttons: list[list[int]]
) -> list[list[float]]:
    matrix_row_size = len(joltage)
    matrix_column_size = len(buttons) + 1

    matrix = [
        [float(0) for _ in range(matrix_column_size)] for _ in range(matrix_row_size)
    ]

    for row in range(matrix_row_size):
        for column in range(matrix_column_size):
            if column >= len(buttons):
                matrix[row][column] = joltage[row]
            elif row in buttons[column]:
                matrix[row][column] = float(1)

    return matrix


def transfrom_matrix_in_row_echolon_form(
    matrix: list[list[float]],
) -> list[list[float]]:
    if len(matrix) == 0:
        return matrix

    pivot_row, pivot_column = 0, 0
    matrix_row_size = len(matrix)
    matrix_column_size = len(matrix[0])

    while pivot_row < matrix_row_size and pivot_column < matrix_column_size:
        max_row_index, max_column_value = max(
            [
                (i, abs(matrix[i][pivot_column]))
                for i in range(pivot_row, matrix_row_size)
            ],
            key=lambda x: x[1],
        )
        if max_column_value == 0:
            pivot_column += 1
        else:
            matrix[pivot_row], matrix[max_row_index] = (
                matrix[max_row_index],
                matrix[pivot_row],
            )

            for row in range(pivot_row + 1, matrix_row_size):
                coefficient = (
                    matrix[row][pivot_column] / matrix[pivot_row][pivot_column]
                )
                matrix[row][pivot_column] = 0

                for column in range(pivot_column + 1, matrix_column_size):
                    matrix[row][column] = (
                        matrix[row][column] - matrix[pivot_row][column] * coefficient
                    )

            pivot_row, pivot_column = pivot_row + 1, pivot_column + 1
    return matrix


def search_in_back_substitution(matrix: list[list[float]]) -> list[int]:
    for pivot_row_index, row in enumerate(reversed(matrix)):
        print(pivot_row_index, row)


part_one(lights, buttons)
part_two(joltage, buttons_joltage)
