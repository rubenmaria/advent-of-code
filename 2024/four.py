def is_in_bounds(row: int, column: int, l: list[list[str]]) -> bool:
    return 0 <= row < len(l) and 0 <= column < len(l[0])


xmas = list(map(list, open("four.input", "r").read().splitlines()))

substrings_one = []
for row in range(len(xmas)):
    for column in range(len(xmas[0])):
        horizontal = xmas[row][column : column + 4]
        vertical = [x[column] for x in xmas[row : row + 4]]
        diagonal_left = [
            xmas[k][l]
            for j in range(4)
            if is_in_bounds(k := row + j, l := column - j, xmas)
        ]
        diagonal_right = [
            xmas[k][l]
            for j in range(4)
            if is_in_bounds(k := row + j, l := column + j, xmas)
        ]
        substrings_one.append("".join(horizontal))
        substrings_one.append("".join(vertical))
        substrings_one.append("".join(diagonal_right))
        substrings_one.append("".join(diagonal_left))
print(substrings_one.count("XMAS") + substrings_one.count("SAMX"))


substrings_two = []
for row in range(len(xmas)):
    for column in range(len(xmas[0])):
        diagonal_right = [
            xmas[k][l]
            for j in range(3)
            if is_in_bounds(k := row + j, l := column + j, xmas)
        ]
        diagonal_left = [
            xmas[k][l]
            for j in range(3)
            if is_in_bounds(k := row + j, l := column + 2 - j, xmas)
        ]
        substrings_two.append("".join(diagonal_right + diagonal_left))
print(
    substrings_two.count("SAMSAM")
    + substrings_two.count("MASSAM")
    + substrings_two.count("SAMMAS")
    + substrings_two.count("MASMAS")
)
