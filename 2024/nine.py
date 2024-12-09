import copy
import math


memory_line = list(map(int, open("nine.input", "r").read().splitlines()[0]))
check_sum = 0
memory_position = 0
end_memory_line = copy.deepcopy(memory_line)[::-1]
end_index = 0
file_id_visited = set()
for i in range(len(memory_line)):
    if i % 2 == 0:
        file_id = int(i / 2)
        space = memory_line[i]

        if file_id in file_id_visited:
            space = end_memory_line[end_index]
            new_add = sum([
                file_id * pos 
                for pos in range(memory_position, memory_position + space)
            ])
            print(f"last: file_id: {file_id}, space: {space}, sum_added: {new_add}")
            check_sum += new_add
            break

        new_add = sum([
            file_id * pos 
            for pos in range(memory_position, memory_position + space)
        ])
        print(f"file_id: {file_id}, space: {space}, sum_added: {new_add}")
        check_sum += new_add
        memory_position += space
        file_id_visited.add(file_id)
    else:
        free_space = memory_line[i]
        for pos in range(memory_position, memory_position + free_space):
            file_id = int((len(memory_line) - 1 - end_index) / 2)
            file_id_visited.add(file_id)
            check_sum += file_id * pos
            print(f"file_id: {file_id}, space: {free_space}, file_added: {file_id*pos}, file_left:{end_memory_line[end_index]}")
            end_memory_line[end_index] -= 1
            if end_memory_line[end_index] == 0:
                end_index += 2
        memory_position += free_space

#print(memory_line)
print(len(memory_line))
print(check_sum)





"""
disk = []; [
    disk := disk + ([str(int(i/2)) * int(d)] if i % 2 == 0 else ["." * int(d)])
    for i,d in enumerate(memory_line)
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

