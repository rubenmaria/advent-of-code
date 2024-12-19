import time

opnames = {
    0: 'adv  | A = A // 2**COM',
    1: 'bxl  | B = B ^ LIT',
    2: 'bst  | B = COM % 8',
    3: 'jnz  | if A!=0: goto LIT',
    4: 'bxc  | B = B^C',
    5: 'out  | print( COM % 8 )',
    6: 'bdv  | B = A//2**COM',
    7: 'cdv  | C = A//2**COM'
}

def run_input_program(
    register_a: int,
    register_b: int,
    register_c: int
) -> list[int]:
    return []

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

print(f"   | OP LIT COM | name | operation")
print("-----------------------------------------------")
for i in range(0,len(program),2):
    op = program[i]
    li = program[i+1]
    co = li 
    if co == 4:
        co = 'A'
    if co == 5:
        co = 'B'
    if co == 6:
        co = 'C' 
    print(f"{i:2d} | {op:2d}  {li:2d}   {co} | {opnames[op]}")





