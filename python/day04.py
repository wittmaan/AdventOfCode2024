import fileinput
from typing import List

# --- Day 4: Ceres Search ---
# --- Part one ---


sample_input = """MMMSXXMASM
MSAMXMSMSA
AMXSXMAAMM
MSAMASMSMX
XMASAMXAMM
XXAMMXXAMA
SMSMSASXSS
SAXAMASAAA
MAMMMXMMMM
MXMXAXMASX""".split(
    "\n"
)


def count_xmas(grid: List[str]):
    target = "XMAS"
    count = 0
    rows = len(grid)
    cols = len(grid[0]) if rows > 0 else 0

    # all 8 possible directions: (dx, dy)
    directions = [
        (0, 1),  # Right
        (1, 0),  # Down
        (1, 1),  # Down-Right
        (-1, 0),  # Up
        (0, -1),  # Left
        (-1, -1),  # Up-Left
        (1, -1),  # Down-Left
        (-1, 1),  # Up-Right
    ]

    for i in range(rows):
        for j in range(cols):
            for dx, dy in directions:
                # calc end position for the word
                end_i = i + dx * (len(target) - 1)
                end_j = j + dy * (len(target) - 1)

                # check if the end position is within bounds
                if 0 <= end_i < rows and 0 <= end_j < cols:
                    word = ""
                    for k in range(len(target)):
                        ni = i + dx * k
                        nj = j + dy * k
                        word += grid[ni][nj]

                    if word == target:
                        count += 1

    return count


def create_grid(data_input):
    return [line.strip().upper() for line in data_input]


assert count_xmas(create_grid(sample_input)) == 18


puzzle_input = [line.rstrip() for line in fileinput.input()]

solution_part1 = count_xmas(create_grid(puzzle_input))

assert solution_part1 == 2557
print(f"solution part1: {solution_part1}")


# --- Part two ---


def count_x_mas(grid):
    count = 0
    rows = len(grid)
    cols = len(grid[0]) if rows > 0 else 0
    valid_sequences = {"MAS", "SAM"}

    # Iterate through possible center positions
    for i in range(1, rows - 1):
        for j in range(1, cols - 1):
            center_char = grid[i][j]
            if center_char != "A":
                continue  # The center must be 'A'

            # Diagonal 1: Top-Left to Bottom-Right
            tl = grid[i - 1][j - 1]
            br = grid[i + 1][j + 1]
            diag1 = tl + center_char + br

            # Diagonal 2: Top-Right to Bottom-Left
            tr = grid[i - 1][j + 1]
            bl = grid[i + 1][j - 1]
            diag2 = tr + center_char + bl

            # check if both diagonals form "MAS" or "SAM"
            if diag1 in valid_sequences and diag2 in valid_sequences:
                count += 1

    return count


assert count_x_mas(create_grid(sample_input)) == 9

solution_part2 = count_x_mas(create_grid(puzzle_input))

assert solution_part2 == 1854
print(f"solution part2: {solution_part2}")
