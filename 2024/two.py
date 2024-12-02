def is_safe(r: list[int]) -> bool:
    return (
        (all(r[i] < r[i+1] for i in range(len(r) - 1))
            or all(r[i] > r[i+1] for i in range(len(r) - 1)))
        and all(abs(r[i] - r[i+1]) <= 3 for i in range(len(r) - 1))
    )


reports = list(map(
    lambda x: [int(el) for el in x.split() if el.isdigit()],
    open("example-two.input", "r").read().splitlines()
))
print(len(list(filter(is_safe, reports))))


def is_safe_joker(r: list[int]) -> bool:
    inc_wrong = [i for i in range(len(r) - 1) if r[i] >= r[i+1]]
    dec_wrong = [i for i in range(len(r) - 1) if r[i] <= r[i+1]]
    if min(len(inc_wrong), len(dec_wrong)) == 0:
        return all([
            abs(r[i] - r[i+1]) <= 3 for i in range(len(r) - 1)
        ])
    else:
        pass


    #[abs(r[i] - r[i+1]) <= 3 for i in range(len(r) - 1)].count(False) <= 1


print(len(list(filter(is_safe_joker, reports))))
