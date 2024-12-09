memory_line = list(map(int, open("dummy-nine.input", "r").read().splitlines()[0]))
print(memory_line)

check_sum = 0
memory_position = 0
file_id_visited = set()
for i in range(len(memory_line)):
    if i % 2 == 0:
        file_id = i / 2
        if file_id in file_id_visited:
            break
        check_sum += sum([
            file_id * pos 
            for pos in range(memory_position, memory_position + memory_line[i])
        ])
        memory_position += memory_line[i]
        file_id_visited.add(file_id)
    else:
        pass






"""
disk = []; [
    disk := disk + ([str(int(i/2)) * int(d)] if i % 2 == 0 else ["." * int(d)])
    for i,d in enumerate(memory_raw_line)
]
disk = list("".join(disk))
for i in range(len(disk)):
    right_of = disk[i+1:]
    has_number_right = list(map(lambda x: x.isdigit(), right_of))
    is_number = list(map(lambda x: x.isdigit(), disk))
    if disk[i] == "." and any(has_number_right):
        index_last_number = len(disk) - 1 - is_number[::-1].index(True)
        disk[i], disk[index_last_number] = disk[index_last_number], disk[i]

disk_numbers = list(map(int, "".join([x if x.isdigit() else "" for x in disk])))
check_sum = 0; [check_sum := check_sum + x * i for i,x in enumerate(disk_numbers)]
"""

