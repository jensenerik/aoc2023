import itertools
from typing import Dict, List, NamedTuple, Optional, Tuple

from . import read_input

EXAMPLE = """???.### 1,1,3
.??..??...?##. 1,1,3
?#?#?#?#?#?#?#? 1,3,1,6
????.#...#... 4,1,1
????.######..#####. 1,6,5
?###???????? 3,2,1"""


def parse_input(input: str) -> List[Tuple[List[str], List[int]]]:
    output_rows = []
    for row in input.splitlines():
        spring_map = list(row.split()[0])
        contiguous_cnts = [int(item) for item in row.split()[1].split(",")]
        output_rows.append((spring_map, contiguous_cnts))
    return output_rows


def construct_arrangements(spring_map: List[str], contiguous_cnt: List[int]) -> int:
    needed_springs = sum(contiguous_cnt) - len([item for item in spring_map if item == "#"])
    question_slots = [i for i, item in enumerate(spring_map) if item == "?"]
    spring_choices = itertools.combinations(question_slots, needed_springs)
    good_choices = 0
    for choice in spring_choices:
        filled_in_map = [(item if item != "?" else ("#" if i in choice else ".")) for i, item in enumerate(spring_map)]
        if check_spring(filled_in_map, contiguous_cnt):
            good_choices += 1
    return good_choices


def check_spring(spring_map: List[str], contiguous_cnt: List[int]) -> bool:
    test_streaks: List[int] = []
    current_streak = 0
    for loc in spring_map:
        if loc == "#":
            current_streak += 1
        elif loc == ".":
            if current_streak:
                test_streaks.append(current_streak)
                current_streak = 0
    if current_streak:
        test_streaks.append(current_streak)
    return test_streaks == contiguous_cnt


def run_and_sum(input: str) -> int:
    running_sum = 0
    for spring_map, contiguous_cnt in parse_input(input):
        running_sum += construct_arrangements(spring_map, contiguous_cnt)
    return running_sum


class partial_solution(NamedTuple):
    completed_streaks: int
    current_streak_required: int
    current_streak_progress: int
    needs_blank: bool


def resolve_dot(part_sol: partial_solution) -> Optional[partial_solution]:
    if part_sol.current_streak_progress == 0:
        return partial_solution(
            part_sol.completed_streaks, part_sol.current_streak_required, part_sol.current_streak_progress, False
        )
    else:
        return None


def resolve_pound(part_sol: partial_solution, contiguous_cnt: List[int]) -> Optional[partial_solution]:
    if not part_sol.needs_blank:
        current_streak_progress = part_sol.current_streak_progress + 1
        if current_streak_progress == part_sol.current_streak_required:
            new_streak = part_sol.completed_streaks + 1
            return partial_solution(
                new_streak, contiguous_cnt[new_streak] if (len(contiguous_cnt) > new_streak) else 0, 0, True
            )
        elif current_streak_progress < part_sol.current_streak_required:
            return partial_solution(
                part_sol.completed_streaks,
                part_sol.current_streak_required,
                part_sol.current_streak_progress + 1,
                False,
            )
        else:
            return None
    return None


def incremental_run(spring_map: List[str], contiguous_cnt: List[int]) -> int:
    solution_counts = {partial_solution(0, contiguous_cnt[0], 0, False): 1}
    for symbol in spring_map:
        new_solutions: Dict[partial_solution, int] = {}
        if symbol == ".":
            for solution, sol_count in solution_counts.items():
                dot_sol = resolve_dot(solution)
                if dot_sol:
                    new_solutions[dot_sol] = new_solutions.get(dot_sol, 0) + sol_count
        elif symbol == "#":
            for solution, sol_count in solution_counts.items():
                pound_sol = resolve_pound(solution, contiguous_cnt)
                if pound_sol:
                    new_solutions[pound_sol] = new_solutions.get(pound_sol, 0) + sol_count
        elif symbol == "?":
            for solution, sol_count in solution_counts.items():
                dot_sol = resolve_dot(solution)
                pound_sol = resolve_pound(solution, contiguous_cnt)
                if dot_sol:
                    new_solutions[dot_sol] = new_solutions.get(dot_sol, 0) + sol_count
                if pound_sol:
                    new_solutions[pound_sol] = new_solutions.get(pound_sol, 0) + sol_count
        solution_counts = new_solutions
    finished_counts = [v for k, v in solution_counts.items() if k.completed_streaks == len(contiguous_cnt)]
    return sum(finished_counts)


def incremental_run_and_sum(input: str, multiplier: int) -> int:
    running_sum = 0
    for spring_map, contiguous_cnt in parse_input(input):
        running_sum += incremental_run(((spring_map + ["?"]) * multiplier)[:-1], contiguous_cnt * multiplier)
    return running_sum


# assert run_and_sum(EXAMPLE) == 21
assert incremental_run_and_sum(EXAMPLE, 1) == 21
assert incremental_run_and_sum(EXAMPLE, 5) == 525152


puzzle_input = read_input("12")

print(incremental_run_and_sum(puzzle_input, 1))
print(incremental_run_and_sum(puzzle_input, 5))
