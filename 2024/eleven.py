from typing import DefaultDict


def stone_amount_blinking(blinks: int, grave_stones: list[int]) -> int:
    grave_stones_zero = 0
    grave_stones_even: dict[int, int] = DefaultDict(int)
    grave_stones_other: dict[int, int] = DefaultDict(int)

    for num in grave_stones:
        if num == 0:
            grave_stones_zero += 1
        elif len(str(num)) % 2 == 0:
            grave_stones_even[num] += 1
        else:
            grave_stones_other[num] += 1

    for _ in range(blinks):
        new_other: dict[int, int] = DefaultDict(int)
        new_even: dict[int, int] = DefaultDict(int)
        new_zero: int = 0

        for k, v in grave_stones_other.items():
            new_key = k * 2024
            if len(str(new_key)) % 2 == 0:
                new_even[new_key] += v
            else:
                new_other[new_key] += v

        for k, v in grave_stones_even.items():
            grave_str = str(k)
            half = len(grave_str) // 2

            first_number = int(grave_str[:half])
            if len(str(first_number)) % 2 == 0:
                new_even[first_number] += v
            elif first_number == 0:
                new_zero += v
            else:
                new_other[first_number] += v
            second_number = int(grave_str[half:])
            if len(str(second_number)) % 2 == 0:
                new_even[second_number] += v
            elif second_number == 0:
                new_zero += v
            else:
                new_other[second_number] += v

        if grave_stones_zero > 0:
            new_other[1] += grave_stones_zero

        grave_stones_other = new_other
        grave_stones_even = new_even
        grave_stones_zero = new_zero

    other_count = sum([v for v in grave_stones_other.values()])
    even_count = sum([v for v in grave_stones_even.values()])
    return other_count + even_count + grave_stones_zero


grave_stones = list(map(int, open("eleven.input").read().split()))
print(stone_amount_blinking(25, grave_stones))
print(stone_amount_blinking(75, grave_stones))
