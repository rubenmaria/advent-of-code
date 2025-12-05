ranges_raw, ids_raw = open("test.input", "r").read().split("\n\n")
ranges = list(
    map(lambda x: (int(x.split("-")[0]), int(x.split("-")[1])), ranges_raw.splitlines())
)
ids = list(map(int, ids_raw.splitlines()))
ranges.sort()


def merge_sorted_overlapping(ranges: list[tuple[int, int]]) -> list[tuple[int, int]]:
    i = 0
    while True:
        if i + 1 >= len(ranges):
            break

        if ranges[i][1] > ranges[i + 1][0]:
            ranges[i] = (ranges[i][0], ranges[i + 1][1])
            ranges.pop(i + 1)
            i = 0

        i += 1

    return ranges


ranges = merge_sorted_overlapping(ranges)
print(ranges)
