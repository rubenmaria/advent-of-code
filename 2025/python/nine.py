red_tiles = list(
    map(
        lambda x: (int(x.split(",")[0]), int(x.split(",")[1])),
        open("real.input").read().splitlines(),
    )
)


def part_one(red_tiles: list[tuple[int, int]]):
    pairs = [
        (red_tiles[i], red_tiles[j])
        for i in range(len(red_tiles))
        for j in range(i + 1, len(red_tiles))
    ]
    areas = sorted([area_of_red_tile_pair(x, y) for x, y in pairs], reverse=True)
    print(f"solution1={areas[0]}")


def area_of_red_tile_pair(x: tuple[int, int], y: tuple[int, int]) -> int:
    height = abs(x[1] - y[1]) + 1
    width = abs(x[0] - y[0]) + 1
    return height * width


def part_two(red_tiles: list[tuple[int, int]]):
    rectangles = rectilinear_polygon_to_rectangles(red_tiles)

    pairs = [
        normalize_rect(red_tiles[i], red_tiles[j])
        for i in range(len(red_tiles))
        for j in range(i + 1, len(red_tiles))
    ]
    valid_pairs = list(filter(lambda x: rectangle_in_polygon(rectangles, x), pairs))
    areas = sorted([area_of_red_tile_pair(x, y) for x, y in valid_pairs], reverse=True)
    print(f"solution2={areas[0]}")


def rectangle_in_polygon(
    polygon: list[tuple[tuple[int, int], tuple[int, int]]],
    rectangle: tuple[tuple[int, int], tuple[int, int]],
) -> bool:
    rectangle_area = area_of_red_tile_pair(rectangle[0], rectangle[1])
    area_sum = 0
    for polygon_rectangle in polygon:
        intersection = rectangle_intersection(rectangle, polygon_rectangle)
        if not intersection:
            continue
        area_sum += area_of_red_tile_pair(intersection[0], intersection[1])

    return rectangle_area == area_sum


def rectangle_intersection(
    a: tuple[tuple[int, int], tuple[int, int]],
    b: tuple[tuple[int, int], tuple[int, int]],
) -> tuple[tuple[int, int], tuple[int, int]] | None:
    (ax1, ay1), (ax2, ay2) = a
    (bx1, by1), (bx2, by2) = b

    x_left = max(ax1, bx1)
    x_right = min(ax2, bx2)

    y_top = max(ay1, by1)
    y_bottom = min(ay2, by2)

    if x_left <= x_right and y_top <= y_bottom:
        return ((x_left, y_top), (x_right, y_bottom))
    return None


def normalize_rect(
    p1: tuple[int, int],
    p2: tuple[int, int],
) -> tuple[tuple[int, int], tuple[int, int]]:
    x1 = min(p1[0], p2[0])
    y1 = min(p1[1], p2[1])
    x2 = max(p1[0], p2[0])
    y2 = max(p1[1], p2[1])
    return ((x1, y1), (x2, y2))


def rectilinear_polygon_to_rectangles(
    polygon: list[tuple[int, int]],
) -> list[tuple[tuple[int, int], tuple[int, int]]]:
    rectangles = []
    unique_xs = sorted(list(set([x for x, _ in polygon])))
    edges = list(zip(polygon, polygon[1:] + [polygon[0]]))
    horizontal_lines = [
        (min(x1, x2), max(x1, x2), y1) for (x1, y1), (x2, y2) in edges if y1 == y2
    ]
    horizontal_slices = list(zip(unique_xs, unique_xs[1:]))
    for i, (x_start, x_end) in enumerate(horizontal_slices):
        ys = iter(
            sorted(
                [y for x1, x2, y in horizontal_lines if x1 <= x_start <= x_end <= x2]
            )
        )
        if i == len(horizontal_slices) - 1:
            rectangles.extend([((x_start, y1), (x_end, next(ys))) for y1 in ys])
        else:
            rectangles.extend([((x_start, y1), (x_end - 1, next(ys))) for y1 in ys])

    return rectangles


part_one(red_tiles)
part_two(red_tiles)
