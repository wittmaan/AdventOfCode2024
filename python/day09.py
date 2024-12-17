import fileinput

# --- Day 9: Disk Fragmenter ---
# --- Part one ---

sample_input1 = "12345"
sample_input2 = "2333133121414131402"


def parse_disk_map(disk_map):
    """
    Parse the disk map input to generate the disk grid.
    """
    grid = []
    file_id = 0  # Start file IDs from 0
    is_file = True

    for i, char in enumerate(disk_map):
        length = int(char)
        if is_file and length > 0:  # File blocks
            grid.extend([file_id] * length)
            file_id += 1
        else:  # Free space
            grid.extend(["."] * length)
        is_file = not is_file  # Toggle between file and free space

    return grid


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
    """
    Calculate the checksum of the final compacted disk.
    """
    checksum = 0
    for position, block in enumerate(grid):
        if block != ".":  # Skip free spaces
            checksum += position * block
    return checksum


def main(disk_map):
    # Step 1: Parse the disk map
    grid = parse_disk_map(disk_map)

    # Step 2: Compact the disk
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
