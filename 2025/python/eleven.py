from functools import lru_cache

servers = dict(
    map(
        lambda x: (
            x.split(":")[0],
            list(filter(lambda x: x != "", x.split(":")[1].split(" "))),
        ),
        open("real.input").read().splitlines(),
    )
)


def part_one(servers: dict[str, list[str]]):
    paths = all_paths_iterative(servers, "you", "out")
    print(f"solution1: {len(paths)}")


def part_two(servers: dict[str, list[str]]):
    paths_svr_fft_count = all_paths_count("svr", "fft")
    paths_fft_dac_count = all_paths_count("fft", "dac")
    paths_dac_out_count = all_paths_count("dac", "out")

    paths_svr_dac_count = all_paths_count("svr", "dac")
    paths_dac_fft_count = all_paths_count("dac", "fft")
    paths_fft_out_count = all_paths_count("fft", "out")

    path_count = (
        paths_svr_fft_count * paths_fft_dac_count * paths_dac_out_count
        + paths_svr_dac_count * paths_dac_fft_count * paths_fft_out_count
    )

    print(f"solution2: {path_count}")


def all_paths(
    servers: dict[str, list[str]], start: str, end: str, path: list[str] = []
) -> list[list[str]]:
    path = path + [start]
    print(path)

    if start == end:
        return [path]

    if start not in servers:
        return []

    paths = []

    for server in servers[start]:
        if server not in path:
            new_paths = all_paths(servers, server, end, path)
            paths.extend(new_paths)

    return paths


def all_paths_iterative(
    servers: dict[str, list[str]], start: str, end: str
) -> list[list[str]]:
    stack = [(start, [start])]
    paths = []

    while stack:
        (server, path) = stack.pop()

        if server == end:
            paths.append(path)
            continue

        neighbors = servers[server]
        for neighbor in neighbors:
            if neighbor not in path:
                stack.append((neighbor, path + [neighbor]))

    return paths


@lru_cache
def all_paths_count(start: str, end: str) -> int:
    if start == end:
        return 1

    if start not in servers:
        return 0

    count = 0
    for server in servers[start]:
        count += all_paths_count(server, end)

    return count


part_one(servers)
part_two(servers)
