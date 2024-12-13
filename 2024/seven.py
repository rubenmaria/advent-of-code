import copy


def parse_numbers(num: str) -> list[int]:
    numbers = []
    for n in num.split():
        numbers.append(int(n))
    return numbers


def is_equation_solvable(eq: tuple[int, list[int]]) -> bool:
    (anwser, numbers) = eq
    if len(numbers) == 1:
        return anwser == numbers[0]
    x = numbers.pop(0)
    y = numbers.pop(0)
    return is_equation_solvable((anwser, [x + y] + numbers)) or is_equation_solvable(
        (anwser, [x * y] + numbers)
    )


def is_equation_solvable_concatenation(eq: tuple[int, list[int]]) -> bool:
    (anwser, numbers) = eq
    if len(numbers) == 1:
        return anwser == numbers[0]
    x = numbers.pop(0)
    y = numbers.pop(0)
    return (
        is_equation_solvable_concatenation((anwser, [x + y] + numbers))
        or is_equation_solvable_concatenation((anwser, [x * y] + numbers))
        or is_equation_solvable_concatenation(
            (anwser, [int(str(x) + str(y))] + numbers)
        )
    )


equations_raw = open("seven.input", "r").read().splitlines()
equations = list(
    map(lambda x: (int(x.split(":")[0]), parse_numbers(x.split(":")[1])), equations_raw)
)
solvalbe_sum = sum(
    map(lambda x: x[0], filter(is_equation_solvable, copy.deepcopy(equations)))
)
print(solvalbe_sum)

solvalbe_sum_concat = sum(
    map(lambda x: x[0], filter(is_equation_solvable_concatenation, equations))
)
print(solvalbe_sum_concat)
