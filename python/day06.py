import fileinput

from tqdm import tqdm

# --- Day 6: Guard Gallivant ---
# --- Part one ---

sample_input = """....#.....
.........#
..........
..#.......
.......#..
..........
.#..^.....
........#.
#.........
......#...""".split(
    "\n"
)

DIRECTION_SYMBOLS = {"^": "up", ">": "right", "v": "down", "<": "left"}

DIRECTIONS = ["up", "right", "down", "left"]

DIRECTION_DELTAS = {"up": (-1, 0), "right": (0, 1), "down": (1, 0), "left": (0, -1)}


def find_guard(grid):
    for y, row in enumerate(grid):
        for x, cell in enumerate(row):
            if cell in DIRECTION_SYMBOLS:
                return (x, y), DIRECTION_SYMBOLS[cell]
    raise ValueError("Guard not found in the map.")


def move_forward(x, y, direction):
    if direction == "up":
        return x, y - 1
    elif direction == "down":
        return x, y + 1
    elif direction == "left":
        return x - 1, y
    elif direction == "right":
        return x + 1, y


def is_inside(x, y, grid):
    return 0 <= y < len(grid) and 0 <= x < len(grid[0])


def can_move(x, y, direction, grid):
    nx, ny = move_forward(x, y, direction)
    if not is_inside(nx, ny, grid):
        return True  # Moving out is allowed (guard escapes)
    return grid[ny][nx] != "#"


def turn_right(direction):
    idx = DIRECTIONS.index(direction)
    return DIRECTIONS[(idx + 1) % 4]


def count_guard_positions(grid):
    grid = [list(row) for row in grid]

    # Find starting position and direction
    (x, y), direction = find_guard(grid)

    visited = set()
    visited.add((x, y))

    while True:
        if can_move(x, y, direction, grid):
            nx, ny = move_forward(x, y, direction)
            if not is_inside(nx, ny, grid):
                break  # Guard escapes
            x, y = nx, ny
            visited.add((x, y))
        else:
            direction = turn_right(direction)

    return len(visited)


assert count_guard_positions(sample_input) == 41

puzzle_input = [line.rstrip() for line in fileinput.input()]

solution_part1 = count_guard_positions(puzzle_input)

assert solution_part1 == 4515
print(f"solution part1: {solution_part1}")

# --- Part two ---


def simulate(grid, start_pos, start_dir):
    x, y = start_pos
    direction = start_dir
    seen_states = set()

    while True:
        state = (x, y, direction)
        if state in seen_states:
            return True  # Loop detected
        seen_states.add(state)

        if can_move(x, y, direction, grid):
            nx, ny = move_forward(x, y, direction)
            if not is_inside(nx, ny, grid):
                return False  # Guard escapes
            x, y = nx, ny
        else:
            direction = turn_right(direction)


def count_obstruction_options(grid):
    start_pos, start_dir = find_guard(grid)

    # identify all possible obstruction positions, excluding the guard's starting position
    possible_positions = set()
    for y, row in enumerate(grid):
        for x, ch in enumerate(row):
            if ch == "." and (x, y) != start_pos:
                possible_positions.add((x, y))

    loop_count = 0
    total_positions = len(possible_positions)

    for ox, oy in tqdm(possible_positions, total=total_positions, desc="Processing positions"):
        # Create a deep copy of the grid
        modified_grid = [list(row) for row in grid]

        # place the obstruction
        modified_grid[oy][ox] = "#"

        # Convert back to list of strings
        modified_grid = ["".join(row) for row in modified_grid]

        # Simulate the guard's movement
        if simulate(modified_grid, start_pos, start_dir):
            loop_count += 1

    return loop_count


assert count_obstruction_options(sample_input) == 6

solution_part2 = count_obstruction_options(puzzle_input)

assert solution_part2 == 1309
print(f"solution part2: {solution_part2}")
