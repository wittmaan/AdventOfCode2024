import fileinput
import re

# --- Day 3: Mull It Over ---
# --- Part one ---

sample_input = "xmul(2,4)%&mul[3,7]!@^do_not_mul(5,5)+mul(32,64]then(mul(11,8)mul(8,5))"
sample_input2 = "xmul(2,4)&mul[3,7]!^don't()_mul(5,5)+mul(32,64](mul(11,8)undo()?mul(8,5))"


def extract_and_sum_multiplications(corrupted_memory):
    pattern = r"mul\(\s*(\d{1,3})\s*,\s*(\d{1,3})\s*\)"
    matches = re.findall(pattern, corrupted_memory)
    result_sum = sum(int(x) * int(y) for x, y in matches)
    return result_sum


assert extract_and_sum_multiplications(sample_input) == 161

solution_part1 = 0
for line in fileinput.input():
    solution_part1 += extract_and_sum_multiplications(line)


assert solution_part1 == 187194524
print(f"solution part1: {solution_part1}")


# --- Part two ---


def parse_and_sum_multiplications(memory):
    mul_pattern = re.compile(r"mul\((\d+),(\d+)\)")
    do_pattern = re.compile(r"do\(\)")
    dont_pattern = re.compile(r"don't\(\)")
    enabled = 1
    total_sum = 0
    instructions = re.findall(r"mul\(\d+,\d+\)|do\(\)|don't\(\)", memory)
    for instr in instructions:
        if do_pattern.match(instr):
            enabled = 1
        elif dont_pattern.match(instr):
            enabled = 0
        else:
            match = mul_pattern.match(instr)
            x, y = int(match.group(1)), int(match.group(2))
            total_sum += x * y * enabled
    return total_sum


assert parse_and_sum_multiplications(sample_input2) == 48

puzzle_input = ""
for line in fileinput.input():
    puzzle_input += line

solution_part2 = parse_and_sum_multiplications(puzzle_input)

assert solution_part2 == 127092535
print(f"solution part2: {solution_part2}")
