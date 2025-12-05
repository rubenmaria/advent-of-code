ranges_raw, ids_raw = open("real.input", "r").read().split("\n\n")
ranges = list(
    map(lambda x: (int(x.split("-")[0]), int(x.split("-")[1])), ranges_raw.splitlines())
)
ids = list(map(int, ids_raw.splitlines()))


def merge_sorted_overlapping(ranges: list[tuple[int, int]]) -> list[tuple[int, int]]:
    i = 0
    while True:
        if i + 1 >= len(ranges):
            break

        if ranges[i][1] >= ranges[i + 1][0]:
            ranges[i] = (ranges[i][0], max(ranges[i][1], ranges[i + 1][1]))
            ranges.pop(i + 1)
            i = 0

        i += 1

    return ranges

def binary_search_ranges(ranges: list[tuple[int, int]], number: int) -> bool:
    if not ranges:
        return False
    
    lower_bound = 0
    upper_bound = len(ranges) - 1

    while lower_bound <= upper_bound:
        mid = (lower_bound + upper_bound) // 2
        start, end = ranges[mid]

        if start <= number <= end:
            return True
        
        if number < start:
            upper_bound = mid - 1
        else:
            lower_bound = mid + 1

    return False 


def part_one_simple(ranges: list[tuple[int,int]], ids: list[int]):
    fresh_count = 0
    for id in ids:
        for r in ranges:
            if r[0] <= id <= r[1]:
                fresh_count += 1
                break
    print(f"solution1={fresh_count}")



def part_one_efficient(ranges: list[tuple[int,int]], ids: list[int]):
    ranges.sort()
    ranges = merge_sorted_overlapping(ranges)
    fresh_count = 0
    for id in ids:
        if binary_search_ranges(ranges, id):
            fresh_count += 1
    print(f"solution1={fresh_count}")

def part_two(ranges: list[tuple[int, int]]):
    ranges = merge_sorted_overlapping(ranges)
    fresh_ids = 0
    for r in ranges:
        fresh_ids += r[1] - r[0] + 1

    print(f"solution2={fresh_ids}")

part_one_simple(ranges, ids)
part_one_efficient(ranges, ids)
part_two(ranges)