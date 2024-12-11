def calculate_check_sum(memory: list[tuple[int,int]]) -> int:
    check_sum = 0
    memory_index = 0
    for file in memory:
        (file_id, blocks_used) = file
        check_sum += sum([
            pos * file_id 
            for pos in range(memory_index, memory_index + blocks_used)
            if file_id != -1
        ])
        memory_index += blocks_used
    return check_sum


memory_line = list(map(int, open("nine.input", "r").read().splitlines()[0]))

files = [(int(i/2), v) for i,v in enumerate(memory_line) if i % 2 == 0]
free_spaces = [v for i,v in enumerate(memory_line) if i % 2 == 1]
deframented_memory: list[tuple[int,int]] = []
for i in range(len(memory_line)):
    if len(files) == 0:
        break
    if i % 2 == 0:
        deframented_memory.append(files.pop(0))
    else:
        space = free_spaces.pop(0)
        while len(files) > 0 and space > 0:
            if space >= (files[-1])[1]:
                done_file = files.pop()
                space = space - done_file[1]
                deframented_memory.append(done_file)
            else:
                files[-1] = (files[-1][0], files[-1][1] - space)
                deframented_memory.append((files[-1][0], space))
                break
print(calculate_check_sum(deframented_memory))

files = [(int(i/2), v) for i,v in enumerate(memory_line) if i % 2 == 0]
free_spaces = [v for i,v in enumerate(memory_line) if i % 2 == 1]
files_and_spaces = [
    (-1,free_spaces[i//2]) if i % 2 == 1 else files[i//2] 
    for i in range(len(memory_line))
]
for file in files[::-1]:
    f_index = files_and_spaces.index(file)
    for space_index, free_space in enumerate(files_and_spaces[:f_index]):
        if free_space[0] != -1:
            continue
        space = free_space[1]
        if space == file[1]:
            file_index = files_and_spaces.index(file)
            files_and_spaces[file_index], files_and_spaces[space_index] = files_and_spaces[space_index], files_and_spaces[file_index]
            break
        if space > file[1]:
            space -= file[1]
            left_free_space = (-1, space)
            new_free_space = (-1, file[1])
            files_and_spaces.pop(space_index)
            file_index = files_and_spaces.index(file)
            files_and_spaces.pop(file_index)
            files_and_spaces.insert(file_index, new_free_space)
            files_and_spaces.insert(space_index, file)
            files_and_spaces.insert(space_index+1, left_free_space)
            break

print(calculate_check_sum(files_and_spaces))
