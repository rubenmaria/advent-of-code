def is_page_correct(page: list[int], order: dict[int, list[int]]) -> bool:
    for i in range(len(page)):
        must_come_after = order[page[i]] if page[i] in order.keys() else []
        after = page[i+1:]
        for d in must_come_after:
            if d in page and d not in after:
                return False
    return True

def fix_page(page: list[int], order: dict[int, list[int]]) ->  list[int]:
    result = page
    while not is_page_correct(result, order):
        for i in range(len(page)):
            must_come_after = order[result[i]] if result[i] in order.keys() else []
            after = result[i+1:]
            for a in must_come_after:
                if a in result and a not in after:
                    result.remove(a)
                    result.insert(i+1, a)
    return result

order_and_pages = open("five.input", "r").read().splitlines()
seperator = order_and_pages.index("")
(order_raw, pages_raw) = (order_and_pages[:seperator], order_and_pages[seperator+1:])
order_tuple = [(int(x.split("|")[0]), int(x.split("|")[1])) for x in order_raw]
pages = [ [int(x) for x in y.split(",")]  for y in pages_raw]
order = {
    k : list(map(lambda x: x[1], list(filter(lambda x: x[0] == k,order_tuple))))
    for k,_ in order_tuple
}
correct_pages = list(filter(lambda x: is_page_correct(x, order), pages))
correct_middle_sum = sum(list(map(lambda x: x[int((len(x)-1)/2)], correct_pages)))
print(correct_middle_sum)

wrong_pages = list(filter(lambda x: not is_page_correct(x, order), pages))
corrected_pages = list(map(lambda x: fix_page(x, order), wrong_pages))
corrected_middle_sum = sum(list(map(lambda x: x[int((len(x)-1)/2)], corrected_pages)))
print(corrected_middle_sum)
