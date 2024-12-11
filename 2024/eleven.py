grave_stones = list(map(int, open("dummy-eleven.input").read().split()))
grave_stones_zero = 0
grave_stones_even: dict[int,int] = {}
grave_stones_other: dict[int,int] = {}

for num in grave_stones:
    if num == 0:
        grave_stones_zero += 1
    elif len(str(num)) % 2 == 0:
        if not num in grave_stones_even:
            grave_stones_even[num] = 1
        else:
            grave_stones_even[num] += 1
    else:
        if not num in grave_stones_other:
            grave_stones_other[num] = 1
        else:
            grave_stones_other[num] += 1

print(grave_stones_other)
print(grave_stones_even)
print(grave_stones_zero)

COUNT = 25
for _ in range(COUNT):
    new_other = {}
    new_even = {}
    new_zero = 0
    
    for k,v in grave_stones_other.items():
        new_key = k * 2024
        if len(str(new_key)) % 2 == 0:
            if new_key not in  new_even:
                new_even[new_key] = v
            else:
                new_even[new_key] += v
        else:
            if new_key not in  new_other:
                new_other[new_key] = v
            else:
                new_other[new_key] += v

    for k,v in grave_stones_even.items():
        grave_str = str(k)
        half = len(grave_str) // 2
        first_number =  int(grave_str[:half])
        second_number = int(grave_str[half:])
        if len(str(first_number)) % 2 == 0:
            if first_number not in new_even:
                new_even[first_number] = v
            else:
                new_even[first_number] += v
        elif first_number == 0:
            new_zero += 1
        else:
            if first_number not in new_other:
                new_other[first_number] = v
            else:
                new_other[first_number] += v

        if len(str(second_number)) % 2 == 0:
            if second_number not in new_even:
                new_even[second_number] = v
            else:
                new_even[second_number] += v
        elif second_number == 0:
            new_zero += 1
        else:
            if second_number not in new_other:
                new_other[second_number] = v
            else:
                new_other[second_number] += v
    
    if grave_stones_zero > 0:
        if 1 not in new_other:
            new_other[1] = grave_stones_zero
        else:
            new_other[1] += grave_stones_zero

    grave_stones_other = new_other
    grave_stones_even = new_even
    grave_stones_zero = new_zero
    print("even: ", grave_stones_even)
    print("other: ", grave_stones_other)
    print("zero: ", grave_stones_zero)

other_count = sum([v for v in grave_stones_other.values()])
even_count = sum([v for v in grave_stones_even.values()])
print(other_count + even_count + grave_stones_zero)

"""
COUNT = 25
for _ in range(COUNT):
    i = 0
    old_len = len(grave_stones)
    while i < len(grave_stones):
        if grave_stones[i] == 0:
            grave_stones[i] = 1
        elif len(str(grave_stones[i])) % 2 == 0:
            grave_str = str(grave_stones.pop(i))
            half = len(grave_str) // 2
            grave_stones.insert(i, int(grave_str[:half]))
            grave_stones.insert(i+1, int(grave_str[half:]))
            i += 1
        else: 
            grave_stones[i] *= 2024
        i += 1
    print(len(grave_stones) - old_len)
"""

