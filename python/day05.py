import fileinput
from collections import defaultdict, deque
from typing import Dict, List, Set, Tuple

# --- Day 5: Print Queue ---
# --- Part one ---

sample_input = """47|53
97|13
97|61
97|47
75|29
61|13
75|53
29|13
97|29
53|29
61|53
97|53
61|29
47|13
75|47
97|75
47|61
75|61
47|29
75|13
53|13

75,47,61,53,29
97,61,53,29,13
75,29,13
75,97,47,61,53
61,13,29
97,13,75,29,47""".split(
    "\n"
)


class PrintQueue:
    def __init__(self, lines_raw: List[str]) -> None:
        self.lines = [line.strip() for line in lines_raw if line.strip()]
        self.rules: List[Tuple[int, int]] = []
        self.updates: List[List[int]] = []
        self.incorrect_updates: List[List[int]] = []
        self._build_rules_and_updates()

    def _build_rules_and_updates(self) -> None:
        separator_index = self._find_separator_index()
        self.rules = self._parse_rules(self.lines[:separator_index])
        self.updates = self._parse_updates(self.lines[separator_index:])

    @staticmethod
    def _determine_separator_index(lines: List[str]) -> int:
        for i, line in enumerate(lines):
            if "|" not in line and "," in line:
                return i
        return len(lines)

    def _find_separator_index(self) -> int:
        return self._determine_separator_index(self.lines)

    @staticmethod
    def _parse_rules(rules_lines: List[str]) -> List[Tuple[int, int]]:
        rule_pairs = []
        for rule in rules_lines:
            if "|" in rule:
                parts = rule.split("|")
                if len(parts) != 2:
                    print(f"Invalid rule format: '{rule}'")
                    continue
                try:
                    x, y = map(int, map(str.strip, parts))
                    rule_pairs.append((x, y))
                except ValueError:
                    print(f"Non-integer rule values: '{rule}'")
            else:
                print(f"Rule missing '|': '{rule}'")
        return rule_pairs

    @staticmethod
    def _parse_updates(updates_lines: List[str]) -> List[List[int]]:
        update_pages = []
        for update in updates_lines:
            try:
                pages = [int(p.strip()) for p in update.split(",") if p.strip()]
                if pages:  # check the update is not empty
                    update_pages.append(pages)
                else:
                    print("Encountered an empty update line.")
            except ValueError:
                print(f"Non-integer page in update: '{update}'")
        return update_pages

    def _build_graph(self, pages_in_update: Set[int]) -> Tuple[Dict[int, List[int]], Dict[int, int]]:
        graph = defaultdict(list)
        in_degree = defaultdict(int)

        for x, y in self.rules:
            if x in pages_in_update and y in pages_in_update:
                graph[x].append(y)
                in_degree[y] += 1
                in_degree.setdefault(x, in_degree[x])  # check x is in in_degree

        return graph, in_degree

    @staticmethod
    def _topological_sort(pages: List[int], graph: Dict[int, List[int]], in_degree: Dict[int, int]) -> List[int]:
        queue = deque([node for node in pages if in_degree.get(node, 0) == 0])
        sorted_list = []

        while queue:
            node = queue.popleft()
            sorted_list.append(node)
            for neighbor in graph.get(node, []):
                in_degree[neighbor] -= 1
                if in_degree[neighbor] == 0:
                    queue.append(neighbor)

        if len(sorted_list) != len(pages):
            raise ValueError("Cycle detected or not all nodes processed")

        return sorted_list

    @staticmethod
    def is_correct(update: List[int], rules: List[Tuple[int, int]]) -> bool:
        page_to_index = {page: idx for idx, page in enumerate(update)}
        for x, y in rules:
            if x in page_to_index and y in page_to_index:
                if page_to_index[x] >= page_to_index[y]:
                    return False
        return True

    def collect_middle_pages(self) -> int:
        middle_pages = []

        for update in self.updates:
            if self.is_correct(update, self.rules):
                if not update:
                    print("Encountered an empty update.")
                    continue
                middle_idx = len(update) // 2
                middle_page = update[middle_idx]
                middle_pages.append(middle_page)
            else:
                self.incorrect_updates.append(update)

        total = sum(middle_pages)
        return total

    def collect_incorrect_updates_middle_pages(self) -> int:
        middle_pages = []

        for update in self.incorrect_updates:
            pages_in_update = set(update)
            graph, in_degree = self._build_graph(pages_in_update)
            try:
                sorted_update = self._topological_sort(update, graph, in_degree)
                if not sorted_update:
                    print("Sorted update is empty.")
                    continue
                middle_idx = len(sorted_update) // 2
                middle_page = sorted_update[middle_idx]
                middle_pages.append(middle_page)
            except ValueError as e:
                print(f"Error processing update {update}: {e}")

        total = sum(middle_pages)
        return total


pq_sample = PrintQueue(sample_input)

assert pq_sample.collect_middle_pages() == 143

puzzle_input = [line.rstrip() for line in fileinput.input()]

pq_puzzle = PrintQueue(puzzle_input)
solution_part1 = pq_puzzle.collect_middle_pages()

assert solution_part1 == 5651
print(f"solution part1: {solution_part1}")


# --- Part two ---

assert pq_sample.collect_incorrect_updates_middle_pages() == 123

solution_part2 = pq_puzzle.collect_incorrect_updates_middle_pages()

assert solution_part2 == 4743
print(f"solution part2: {solution_part2}")
