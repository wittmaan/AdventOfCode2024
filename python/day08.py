import fileinput

# --- Day 8: Resonant Collinearity ---
# --- Part one ---


sample_input = """............
........0...
.....0......
.......0....
....0.......
......A.....
............
............
........A...
.........A..
............
............""".split(
    "\n"
)


def parse_map(grid):
    antennas = {}
    for y, row in enumerate(grid):
        for x, cell in enumerate(row):
            if cell != ".":
                if cell not in antennas:
                    antennas[cell] = []
                antennas[cell].append((x, y))
    return antennas


def find_antinodes(antennas, grid_width, grid_height):
    antinodes = set()
    for freq, positions in antennas.items():
        for i in range(len(positions)):
            for j in range(i + 1, len(positions)):
                x1, y1 = positions[i]
                x2, y2 = positions[j]

                # Midpoint and difference vector
                dx, dy = x2 - x1, y2 - y1
                mx, my = x1 + dx // 2, y1 + dy // 2

                # Ensure midpoint is valid and divisible
                if dx % 2 == 0 and dy % 2 == 0:
                    antinodes.add((mx, my))

                # Extend to create antinodes
                antinodes.add((x1 - dx, y1 - dy))
                antinodes.add((x2 + dx, y2 + dy))

    # Filter by valid grid coordinates
    return {(x, y) for x, y in antinodes if 0 <= x < grid_width and 0 <= y < grid_height}


def calc_total_unique_antinodes(grid):
    antennas = parse_map(grid)
    antinodes = find_antinodes(antennas, len(grid[0]), len(grid))
    return len(antinodes)


assert calc_total_unique_antinodes(sample_input) == 14

puzzle_input = [line.rstrip() for line in fileinput.input()]
solution_part1 = calc_total_unique_antinodes(puzzle_input)

assert solution_part1 == 259
print(f"solution part1: {solution_part1}")
