from posixpath import curdir

rotations = list(
    filter(lambda x: len(x) > 0, open("real.input", "r").read().split("\n"))
)


def part_two(rotations: list[str]):
    current_value = 50
    through_zero = 0

    for rotation in rotations:
        rotation_amount = int(rotation[1:])
        if rotation[0] == "R":
            smallest_amount_to_zero = (100 - current_value) % 100

            def rotate(x, y):
                return x + y
        else:
            smallest_amount_to_zero = current_value % 100

            def rotate(x, y):
                return x - y

        if smallest_amount_to_zero > rotation_amount:
            current_value = rotate(current_value, rotation_amount) % 100
            continue

        if smallest_amount_to_zero == 0:
            through_zero += rotation_amount // 100
        else:
            through_zero += 1 + (rotation_amount - smallest_amount_to_zero) // 100

        current_value = rotate(current_value, rotation_amount) % 100

    print(f"solution2={through_zero}")


def part_one(rotations: list[str]):
    current_value = 50
    zero_ending = 0

    for rotation in rotations:
        rotation_amount = int(rotation[1:])
        if rotation[0] == "R":
            current_value = (current_value + rotation_amount) % 100
        else:
            current_value = (current_value - rotation_amount) % 100

        if current_value == 0:
            zero_ending += 1

    print(f"solution1={zero_ending}")


part_one(rotations)
part_two(rotations)
