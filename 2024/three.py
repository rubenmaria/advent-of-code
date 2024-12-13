import re
import itertools
import functools


def tuple_to_values(t: tuple[str, str, str, str]) -> int:
    if t[0] != "":
        return int(t[0]) * int(t[1])
    if t[2] != "":
        return -1
    return -2


def do_iteration(acc: tuple[int, int], x: int) -> tuple[int, int]:
    (sum, flag) = acc
    if x >= 0 and flag == -1:
        return (sum + x, flag)
    if x >= 0 and flag == -2:
        return (sum, flag)
    return (sum, x)


memory = open("three.input", "r").read()
numbers = re.findall(r"mul\((\d{1,3}),(\d{1,3})\)", memory)
mulitplied = list(map(lambda x: int(x[0]) * int(x[1]), numbers))
sum = functools.reduce(lambda x, y: x + y, mulitplied, 0)
print(sum)

numbers_do = re.findall(r"mul\((\d{1,3}),(\d{1,3})\)|(do)\(\)|(don't)\(\)", memory)
mulitplied_do = list(map(tuple_to_values, numbers_do))
sum_do_debug = list(itertools.accumulate(mulitplied_do, do_iteration, initial=(0, -1)))
sum_do = functools.reduce(do_iteration, mulitplied_do, (0, -1))
print(sum_do[0])
