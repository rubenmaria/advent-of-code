def parse_antenna(m: list[list[str]]) -> dict[str, list[tuple[int, int]]]:
    antennas: dict[str, list[tuple[int, int]]] = {}
    for row in range(len(m)):
        for column in range(len(m[0])):
            if (a := m[row][column]) == ".":
                continue
            if a not in antennas:
                antennas[a] = [(row, column)]
            else:
                antennas[a] += [(row, column)]
    return antennas


def is_in_bounds(x: tuple[int, int], map: list[list[str]]) -> bool:
    return 0 <= x[0] < len(map) and 0 <= x[1] < len(map[0])


antennas_map = list(map(list, open("eight.input", "r").read().splitlines()))
antennas_dict = parse_antenna(antennas_map)

antinodes = set()
for antennas in antennas_dict.values():
    for antenna in antennas:
        for neighbor in antennas:
            delta = (antenna[0] - neighbor[0], antenna[1] - neighbor[1])
            if delta == (0, 0):
                continue
            antinode = (antenna[0] + delta[0], antenna[1] + delta[1])
            if is_in_bounds(antinode, antennas_map):
                antinodes.add(antinode)

antinodes_resonant = set()
for _, antennas in antennas_dict.items():
    for antenna in antennas:
        for neighbor in antennas:
            delta = (antenna[0] - neighbor[0], antenna[1] - neighbor[1])
            if delta == (0, 0):
                continue
            for muliplier in range(max(len(antennas_map[0]), len(antennas_map))):
                antinode = (
                    antenna[0] + muliplier * delta[0],
                    antenna[1] + muliplier * delta[1],
                )
                if is_in_bounds(antinode, antennas_map):
                    antinodes_resonant.add(antinode)
print(len(antinodes))
print(len(antinodes_resonant))
