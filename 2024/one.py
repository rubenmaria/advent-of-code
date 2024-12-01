from collections import Counter


def line_to_number_tuple(raw: str) ->  tuple[int, int]:
    numbers = raw.split()
    return (int(numbers[0]), int(numbers[1]))

valid_data = list(filter(lambda x: x != "", open("one.input", "r").read().split("\n")))
number_tuples = list(map(line_to_number_tuple, valid_data));
f = lambda x, acc: (acc[0] + [x[0]], acc[1] + [x[1]])
acc = ([],[]); [acc := f(x, acc) for x in number_tuples]
(first_list, second_list) = acc
first_list.sort()
second_list.sort()
list_combined = zip(first_list, second_list)
deltas = map(lambda x: abs(x[0] - x[1]), list_combined)
delta_sum = 0; [delta_sum := x + delta_sum for x in deltas]
print(delta_sum)


counter = Counter(second_list)
occurences_first_in_second = [counter[x] for x in first_list]
score = 0; [
    score := score + occurences_first_in_second[i] * first_list[i]
    for i in range(len(first_list))
]
print(score)
