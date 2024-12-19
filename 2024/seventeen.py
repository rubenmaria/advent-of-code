def run_input_program(
    register_a: int,
    register_b: int,
    register_c: int
) -> list[int]:
    out: list[int] = []
    while True:
        register_b = register_a % 8
        register_b = register_b ^ 7
        register_c = register_a // (2**register_b)
        register_a = register_a // 8
        register_b = register_b ^ register_c
        register_b = register_b ^ 7
        out += [register_b % 8]
        if register_a == 0:
            break
    return out


def find_initial_a(out: list[int]) -> int:
    to_visit: list[tuple[int, int]] = [(len(out), 0)]
    while len(to_visit) > 0:
        (pos, a) = to_visit.pop(0)
        for i in range(8):
            new_a = a * 8 + i
            current_out = run_input_program(new_a, 0, 0)
            if current_out == out[pos-1:]:
                print(current_out)
                to_visit += [(pos - 1, new_a)]
                if len(current_out) == len(out):
                    return new_a
    raise Exception()

def get_combo_operand(
    operand: int,
    register_a: int,
    register_b: int,
    register_c: int
) -> int:
    match operand:
        case 0 | 1 | 2 | 3:
            return operand
        case 4:
            return register_a
        case 5: 
            return register_b
        case 6:
            return register_c
        case _:
            raise Exception()

def simulate_program(
    program: list[int],
    register_a: int,
    register_b: int,
    register_c: int
) -> list[int]:
    out: list[int] = []
    program_counter: int = 0
    while True:
        instruction = program[program_counter]
        match instruction:
            case 0: 
                operand = program[program_counter + 1]
                combo_operand = get_combo_operand(
                    operand,
                    register_a,
                    register_b,
                    register_c
                )
                numerator = register_a
                denominator = 2**combo_operand
                register_a = numerator // denominator
                program_counter += 2
            case 1:
                operand = program[program_counter + 1]
                register_b = register_b ^ operand
                program_counter += 2
            case 2:
                operand = program[program_counter + 1]
                combo_operand = get_combo_operand(
                    operand,
                    register_a,
                    register_b,
                    register_c
                )
                register_b = combo_operand % 8
                program_counter += 2
            case 3: 
                if register_a != 0:
                    operand = program[program_counter + 1]
                    program_counter = operand
                else:
                    program_counter += 2
            case 4:
                register_b = register_b ^ register_c
                program_counter += 2
            case 5:
                operand = program[program_counter + 1]
                combo_operand = get_combo_operand(
                    operand,
                    register_a,
                    register_b,
                    register_c
                )
                out += [combo_operand % 8]
                program_counter += 2
            case 6:
                operand = program[program_counter + 1]
                combo_operand = get_combo_operand(
                    operand,
                    register_a,
                    register_b,
                    register_c
                )
                numerator = register_a
                denominator = 2**combo_operand
                register_b = numerator // denominator
                program_counter += 2
            case 7:
                operand = program[program_counter + 1]
                combo_operand = get_combo_operand(
                    operand,
                    register_a,
                    register_b,
                    register_c
                )
                numerator = register_a
                denominator = 2**combo_operand
                register_c = numerator // denominator
                program_counter += 2
        if program_counter >= len(program):
            break
    return out


program_and_register_raw = open("seventeen.input").read().splitlines()
program_raw = program_and_register_raw[4].split(":")[1]
program: list[int] = eval("[" + program_raw + "]")
register_a: int = int(program_and_register_raw[0].split(":")[1])
register_b: int = int(program_and_register_raw[1].split(":")[1])
register_c: int = int(program_and_register_raw[2].split(":")[1])

print(find_initial_a([
    2, 4, 1, 7, 7, 5, 0, 3, 4, 0, 1, 7, 5, 5, 3, 0
]))



