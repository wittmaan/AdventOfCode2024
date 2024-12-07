import fileinput

# --- Day 7: Bridge Repair ---
# --- Part one ---

sample_input = """190: 10 19
3267: 81 40 27
83: 17 5
156: 15 6
7290: 6 8 6 15
161011: 16 10 13
192: 17 8 14
21037: 9 7 18 13
292: 11 6 16 20""".split(
    "\n"
)


def parse_input(data):
    equations = []
    for line in data:
        target, numbers = line.split(":")
        target = int(target.strip())
        numbers = list(map(int, numbers.strip().split()))
        equations.append((target, numbers))
    return equations


def is_valid_equation(numbers, target, current=0, index=0, include_concat=False):
    if index == len(numbers):
        return current == target

    next_number = numbers[index]
    # Try addition
    if is_valid_equation(numbers, target, current + next_number, index + 1, include_concat):
        return True
    # Try multiplication
    if is_valid_equation(numbers, target, current * next_number, index + 1, include_concat):
        return True

    # Try concatenation (current treated as a string concatenated with next_number)
    concat_result = int(str(current) + str(next_number))
    if include_concat and is_valid_equation(numbers, target, concat_result, index + 1, include_concat):
        return True

    return False


def sum_valid_equations(equations, include_concat=False):
    valid_targets = []
    for target, numbers in equations:
        # start with the first number as the initial total
        if is_valid_equation(numbers, target, numbers[0], 1, include_concat):
            valid_targets.append(target)
    return sum(valid_targets)


assert sum_valid_equations(parse_input(sample_input)) == 3749

puzzle_input = [line.rstrip() for line in fileinput.input()]
solution_part1 = sum_valid_equations(parse_input(puzzle_input))

assert solution_part1 == 6083020304036
print(f"solution part1: {solution_part1}")

# --- Part two ---

assert sum_valid_equations(parse_input(sample_input), include_concat=True) == 11387

solution_part2 = sum_valid_equations(parse_input(puzzle_input), include_concat=True)

assert solution_part2 == 59002246504791
print(f"solution part2: {solution_part2}")
