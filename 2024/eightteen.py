

def generate_map(
    falling_bytes: list[tuple[int, int]],
    falling_bytes_count: int,
    size: int
) -> list[list[str]]:
    byte_positions = falling_bytes[:falling_bytes_count+1]
    memory: list[list[str]] = []
    for row in range(size):
        memory += [[ 
            "#" if (row, column) in byte_positions else "."
            for column in range(size)
        ]]
    return memory


def draw_map(memory: list[list[str]]) -> None:
    for row in memory:
        print("".join(row))


falling_bytes: list[tuple[int, int]] = list(
    map(eval, open("dummy-eightteen.input").read().splitlines())
)
print(falling_bytes)
draw_map(generate_map(falling_bytes, 12, 7))

