def is_safe(r: list[int]) -> bool:
    VALID_DIFF = [1, 2, 3]
    return all((r[i + 1] - r[i]) in VALID_DIFF for i in range(len(r) - 1)) or all(
        (r[i] - r[i + 1]) in VALID_DIFF for i in range(len(r) - 1)
    )


def is_safe_joker(r: list[int]) -> bool:
    return is_safe(r) or any(
        is_safe([x for (j, x) in enumerate(r) if i != j]) for i in range(len(r))
    )


reports = list(
    map(
        lambda x: [int(el) for el in x.split() if el.isdigit()],
        open("two.input", "r").read().splitlines(),
    )
)
print(len(list(filter(is_safe, reports))))
print(len(list(filter(is_safe_joker, reports))))
