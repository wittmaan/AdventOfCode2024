import fileinput

# --- Day 9: Disk Fragmenter ---
# --- Part one ---

sample_input1 = "12345"
sample_input2 = "2333133121414131402"


def parse_disk_map(disk_map):
    grid = []
    blocks = []
    gaps = []
    file_id = 0  # Start file IDs from 0
    is_file = True

    for i, char in enumerate(disk_map):
        length = int(char)
        if is_file and length > 0:  # File blocks
            blocks.append((len(grid), file_id, length))
            grid.extend([file_id] * length)
            file_id += 1
        else:  # Free space
            gaps.append((length, len(grid)))
            grid.extend(["."] * length)
        is_file = not is_file  # Toggle between file and free space

    return grid, blocks, gaps


def compact_disk(grid):
    free_space = grid.index(".")
    for i in reversed(range(0, len(grid))):
        if grid[i] != ".":
            grid[free_space] = grid[i]
            grid[i] = "."
            while grid[free_space] != ".":
                free_space += 1
            if i - free_space <= 1:
                break
    return grid


def calculate_checksum(grid):
    checksum = 0
    for position, block in enumerate(grid):
        if block != ".":  # Skip free spaces
            checksum += position * block
    return checksum


def move_blocks(grid, blocks, gaps):
    for block in reversed(blocks):
        (position, file_id, length) = block
        for idx, (gap_length, gap_position) in enumerate(gaps):
            if gap_position > position:
                break

            if gap_length >= length:
                for i in range(length):
                    grid[position + i] = "."
                    grid[gap_position + i] = file_id

                diff = gap_length - length
                if diff > 0:
                    gaps[idx] = (diff, gap_position + length)
                else:
                    gaps.pop(idx)
                break
    return grid


def main(disk_map, move_whole_files: bool = False):
    # Step 1: Parse the disk map
    grid, blocks, gaps = parse_disk_map(disk_map)

    # Step 2: Compact the disk
    if move_whole_files:
        compacted_grid = move_blocks(grid, blocks, gaps)
    else:
        compacted_grid = compact_disk(grid)

    # Step 3: Calculate the checksum
    checksum = calculate_checksum(compacted_grid)
    return checksum


assert main(sample_input1) == 60
assert main(sample_input2) == 1928

puzzle_input = [line.rstrip() for line in fileinput.input()]
solution_part1 = main(puzzle_input[0])

assert solution_part1 == 6398608069280
print(f"solution part1: {solution_part1}")

# --- Part two ---


assert main(sample_input1, move_whole_files=True) == 132
assert main(sample_input2, move_whole_files=True) == 2858

solution_part2 = main(puzzle_input[0], move_whole_files=True)

assert solution_part2 == 6427437134372
print(f"solution part2: {solution_part2}")
