import math

battery_banks = list(open("real.input", "r").read().splitlines())
print(battery_banks)


def part_one(battery_banks: list[str]):
    batteries = list(map(list, battery_banks))
    batteries_joltage = list(map(lambda x: list(map(int, x)), batteries))
    max_sum_joltage = 0
    for battery_joltage in batteries_joltage:
        current_max_joltage = -math.inf
        visited_first = set()
        visited_second = set()
        while True:
            first_candidates = get_first_available(battery_joltage, visited_first)
            first_index, first_value = argmax(first_candidates)
            second_candidates = from_frist_get_available_second(
                battery_joltage, first_index, visited_second
            )
            if second_candidates == []:
                visited_first.add(first_index)
                continue

            second_index, second_value = argmax(second_candidates)

            joltage_value = int(str(first_value) + str(second_value))

            if joltage_value <= current_max_joltage:
                break

            current_max_joltage = joltage_value
            visited_first.add(first_index)
            visited_second.add(second_index)

        max_sum_joltage += current_max_joltage
    print(f"solution1={max_sum_joltage}")


def argmax(x: list[int]) -> tuple[int, int]:
    return max(list(enumerate(x)), key=lambda x: x[1])


def from_frist_get_available_second(
    battery_joltage: list[int], first_index: int, visited_second: set
) -> list[int]:
    available = []

    for i in range(first_index + 1, len(battery_joltage)):
        if i not in visited_second:
            available.append(battery_joltage[i])

    return available


def get_first_available(
    battery_joltage: list[int], visited_first: set[int]
) -> list[int]:
    available = []

    for i in range(len(battery_joltage)):
        if i not in visited_first:
            available.append(battery_joltage[i])

    return available


def from_previous_get_argmax(
    battery_joltage: list[int],
    prev_index: int,
    visited_current: set,
    joltage_amount: int,
    joltages_done: int,
) -> tuple[int, int] | None:
    current_max = -math.inf
    current_max_index = 0

    for i in range(prev_index + 1, len(battery_joltage)):
        if i > len(battery_joltage) - joltage_amount + joltages_done:
            break
        if i not in visited_current and current_max < battery_joltage[i]:
            current_max_index = i
            current_max = battery_joltage[i]

    return (current_max_index, int(current_max)) if current_max != -math.inf else None


def get_first_argmax(
    battery_joltage: list[int], visited: set, joltage_amount: int
) -> tuple[int, int]:
    current_max = -math.inf
    current_max_index = 0
    for i in range(len(battery_joltage)):
        if i > len(battery_joltage) - joltage_amount:
            break
        if i not in visited and current_max < battery_joltage[i]:
            current_max_index = i
            current_max = battery_joltage[i]

    return (current_max_index, int(current_max))


def part_two(battery_banks: list[str], joltage_amount: int):
    batteries = list(map(list, battery_banks))
    batteries_joltage = list(map(lambda x: list(map(int, x)), batteries))
    max_sum_joltage = 0
    for battery_joltage in batteries_joltage:
        current_max_joltage = -math.inf
        joltages_visited = [set() for _ in range(joltage_amount)]
        while True:
            joltage_values = [
                get_first_argmax(battery_joltage, joltages_visited[0], joltage_amount)
            ]

            for i in range(1, joltage_amount):
                previous_best_index = joltage_values[i - 1][0]
                value = from_previous_get_argmax(
                    battery_joltage,
                    previous_best_index,
                    joltages_visited[i],
                    joltage_amount,
                    i,
                )

                if value is None:
                    joltage_value = current_max_joltage
                    break

                joltage_values.append(value)

            joltage_value = int(
                "".join(list(map(str, map(lambda x: x[1], joltage_values))))
            )

            if joltage_value <= current_max_joltage:
                break

            current_max_joltage = joltage_value

            for i in range(joltage_amount):
                joltages_visited[i].add(joltage_values[i][0])
        max_sum_joltage += current_max_joltage
    print(f"solution1+2={max_sum_joltage}")


part_one(battery_banks)
part_two(battery_banks, 12)
