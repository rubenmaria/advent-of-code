from fractions import Fraction


def determinant(
    equation: tuple[tuple[int, int], tuple[int, int], tuple[int, int]]
) -> int:
    a = equation[0]
    b = equation[1]
    return a[0] * b[1] - a[1] * b[0]


def solve(
    equation: tuple[tuple[int, int], tuple[int, int], tuple[int, int]]
) -> tuple[Fraction, Fraction]:
    a = equation[0]
    b = equation[1]
    p = equation[2]
    equation_matrix = ((a[0], b[0]), (a[1], b[1]))
    factor = Fraction(
        1, (equation_matrix[0][0] * equation_matrix[1][1] -
            equation_matrix[0][1] * equation_matrix[1][0])
    )
    inverse = (
        (factor * equation_matrix[1][1], factor * (-equation_matrix[0][1])),
        (factor * (-equation_matrix[1][0]), factor * (equation_matrix[0][0]))
    )
    return (
        inverse[0][0] * p[0] + inverse[0][1] * p[1],
        inverse[1][0] * p[0] + inverse[1][1] * p[1]
    )


equations_raw = list(filter(
    lambda x: x != "",
    open("thirteen.input", "r").read().splitlines()
))
equations: list[tuple[tuple[int, int], tuple[int, int], tuple[int, int]]] = []
for i in range(0, len(equations_raw), 3):
    (a_x_raw, a_y_raw) = equations_raw[i].split(",")
    (b_x_raw, b_y_raw) = equations_raw[i+1].split(",")
    (price_x, price_y) = equations_raw[i+2].split(",")
    a = (int(a_x_raw.split("+")[1]), int(a_y_raw.split("+")[1]))
    b = (int(b_x_raw.split("+")[1]), int(b_y_raw.split("+")[1]))
    prices = (int(price_x.split("=")[1]), int(price_y.split("=")[1]))
    equations += [(a, b, prices)]
solvable_equations = list(filter(
    lambda x: all(map(Fraction.is_integer, solve(x))),
    equations
))
equations_fixed = list(map(
    lambda x: (x[0], x[1], (x[2][0]+10000000000000, x[2][1]+10000000000000)),
    equations
))
solvable_fixed_equations = list(filter(
    lambda x: all(map(Fraction.is_integer, solve(x))),
    equations_fixed
))
print(
    sum(
        map(
            lambda x: 3 * x[0].numerator + x[1].numerator,
            map(solve, solvable_equations)
        )
    )
)
print(
    sum(
        map(
            lambda x: 3 * x[0].numerator + x[1].numerator,
            map(solve, solvable_fixed_equations)
        )
    )
)
