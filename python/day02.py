import fileinput

# --- Day 2: Red-Nosed Reports ---
# --- Part one ---


# Example input data
sample_input = """7 6 4 2 1
1 2 7 8 9
9 7 6 2 1
1 3 2 4 5
8 6 4 4 1
1 3 6 7 9""".split(
    "\n"
)


def is_safe(levels):
    n = len(levels)

    if n < 2:
        return True

    increasing = all(1 <= levels[i + 1] - levels[i] <= 3 for i in range(n - 1))
    decreasing = all(1 <= levels[i] - levels[i + 1] <= 3 for i in range(n - 1))

    return increasing or decreasing


def count_safe_reports(reports):
    safe_count = 0
    for report in reports:
        levels = list(map(int, report.split()))
        if is_safe(levels):
            safe_count += 1
    return safe_count


assert count_safe_reports(sample_input) == 2

puzzle_input = [line.rstrip() for line in fileinput.input()]
solution_part1 = count_safe_reports(puzzle_input)

assert solution_part1 == 299
print(f"solution part1: {solution_part1}")


# --- Part two ---


def count_safe_reports(reports):
    safe_count = 0

    for report in reports:
        levels = list(map(int, report.split()))
        if is_safe(levels):
            safe_count += 1
            continue

        for i in range(len(levels)):
            modified_levels = levels[:i] + levels[i + 1 :]
            if is_safe(modified_levels):
                safe_count += 1
                break

    return safe_count


assert count_safe_reports(sample_input) == 4


solution_part2 = count_safe_reports(puzzle_input)

assert solution_part2 == 364
print(f"solution part2: {solution_part2}")
