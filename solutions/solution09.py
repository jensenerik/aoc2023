from typing import List

from . import read_input

EXAMPLE = """0 3 6 9 12 15
1 3 6 10 15 21
10 13 16 21 30 45"""


def parse_rows(input: str) -> List[List[int]]:
    rows = input.splitlines()
    return [[int(item) for item in row.split()] for row in rows]


def predict_value(sequence: List[int], left: bool) -> int:
    new_seq = sequence
    firsts = [sequence[0]]
    lasts = [sequence[-1]]
    while any(new_seq):
        new_seq = [new_seq[i + 1] - new_seq[i] for i in range(len(new_seq) - 1)]
        lasts.append(new_seq[-1])
        firsts.append(new_seq[0])
    return sum([(-1) ** (i) * item for i, item in enumerate(firsts)]) if left else sum(lasts)


def sum_up_predictions(input: str, left: bool = False) -> int:
    total_sum = 0
    for row in parse_rows(input):
        total_sum += predict_value(row, left)
    return total_sum


assert sum_up_predictions(EXAMPLE) == 114
assert sum_up_predictions(EXAMPLE, left=True) == 2

puzzle_input = read_input("09")

print(sum_up_predictions(puzzle_input))
print(sum_up_predictions(puzzle_input, left=True))
