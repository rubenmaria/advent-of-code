ranges = list(
    map(
        lambda x: tuple(map(int, x.split("-"))),
        open("real.input", "r").read().split(","),
    )
)


def part_one(intervals: list[tuple]):
    invalid_id_sum = 0
    for interval in intervals:
        for number in range(interval[0], interval[1] + 1):
            number_string = str(number)
            number_length = len(number_string)
            if number_length % 2 != 0:
                continue
            if (
                number_string[: number_length // 2]
                == number_string[number_length // 2 :]
            ):
                invalid_id_sum += number
    print(f"solution1: {invalid_id_sum}")


def part_two(intervals: list[tuple]):
    invalid_id_sum = 0
    for interval in intervals:
        for number in range(interval[0], interval[1] + 1):
            number_string = str(number)
            number_length = len(number_string)
            for part_length in range(1, len(number_string) // 2 + 1):
                duplicates = set()
                for start_index in range(0, number_length, part_length):
                    devided_number = number_string[
                        start_index : start_index + part_length
                    ]
                    duplicates.add(devided_number)

                if len(duplicates) == 1:
                    invalid_id_sum += number
                    break

    print(f"solution2: {invalid_id_sum}")


part_one(ranges)
part_two(ranges)
