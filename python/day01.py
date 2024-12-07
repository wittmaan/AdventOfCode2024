import fileinput
from collections import Counter
from typing import List

# --- Day 1: Historian Hysteria ---
# --- Part one ---


sample_input = """3   4
4   3
2   5
1   3
3   9
3   3""".split(
    "\n"
)


def parse_input(lines: List[str]) -> (List[int], List[int]):
    left_list = []
    right_list = []
    for line in lines:
        left, right = map(int, line.split())
        left_list.append(left)
        right_list.append(right)
    return left_list, right_list


def calculate_total_distance(lines: List[str]) -> int:
    left_list, right_list = parse_input(lines)
    left_list.sort()
    right_list.sort()
    return sum(abs(a - b) for a, b in zip(left_list, right_list))


assert calculate_total_distance(sample_input) == 11

puzzle_input = [line.rstrip() for line in fileinput.input()]
solution_part1 = calculate_total_distance(puzzle_input)

assert solution_part1 == 3246517
print(f"solution part1: {solution_part1}")


# --- Part two ---


def calculate_similarity_score(lines: List[str]) -> int:
    left_list, right_list = parse_input(lines)
    right_count = Counter(right_list)
    return sum(num * right_count[num] for num in left_list)


assert calculate_similarity_score(sample_input) == 31

solution_part2 = calculate_similarity_score(puzzle_input)

assert solution_part2 == 29379307
print(f"solution part2: {solution_part2}")
