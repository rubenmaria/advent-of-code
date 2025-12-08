from math import prod

problems = list(map(lambda x: list(filter(lambda x: x != "", map(
    lambda x: x.strip(), x.split(" ")))),
    open("real.input", "r").read().splitlines()))

problems_with_spaces = list(
    open("real.input", "r").read().splitlines()
)


def part_one(problems: list[list[str]]):
    grand_total = 0

    for column in range(len(problems[0])):
        problem_length = len(problems)
        operator = problems[problem_length - 1][column]
        if operator == "+":
            problem_result = 0
            for row in range(problem_length - 1):
                problem_result += int(problems[row][column])
        else:
            problem_result = 1
            for row in range(problem_length - 1):
                problem_result *= int(problems[row][column])

        grand_total += problem_result

    print(f"solution1={grand_total}")


def part_two(rows: list[str]):
    grand_total = 0
    current_number_string = ""
    numbers = []
    problem_start = 0
    for column in range(len(rows[0])):
        for row in range(len(rows) - 1):
            if rows[row][column] != " ":
                current_number_string += rows[row][column]

        if current_number_string != "":
            numbers.append(int(current_number_string))
            current_number_string = ""
        else:
            if rows[len(rows)-1][problem_start] == "*":
                grand_total += prod(numbers)
            else:
                grand_total += sum(numbers)
            numbers.clear()
            problem_start = column + 1
    if rows[len(rows)-1][problem_start] == "*":
        grand_total += prod(numbers)
    else:
        grand_total += sum(numbers)
    print(f"solution2={grand_total}")



part_one(problems)
part_two(problems_with_spaces)