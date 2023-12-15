from typing import List, Tuple

from solutions import read_input

EXAMPLE_HASH = "HASH"

EXAMPLE_STEPS = "rn=1,cm-,qp=3,cm=2,qp-,pc=4,ot=9,ab=5,pc-,pc=6,ot=7"


def hash_code(input: str) -> int:
    running_total = 0
    for item in list(input.encode("ascii")):
        running_total = ((running_total + item) * 17) % 256
    return running_total


def hash_sum(input: str) -> int:
    running_sum = 0
    for item in input.split(","):
        running_sum += hash_code(item)
    return running_sum


def do_boxes(input: str) -> List[List[Tuple[str, int]]]:
    boxes: List[List[Tuple[str, int]]] = [[]] * 256
    for item in input.split(","):
        code = item[:-1] if (item[-1] == "-") else item.split("=")[0]
        box_num = hash_code(code)
        if item[-1] == "-":
            for i, lenses in enumerate(boxes[box_num]):
                if lenses[0] == code:
                    del boxes[box_num][i]
                    break
        else:
            focal = int(item.split("=")[1])
            found = False
            for i, lenses in enumerate(boxes[box_num]):
                if lenses[0] == code:
                    found = True
                    boxes[box_num][i] = (code, focal)
                    break
            if not found:
                boxes[box_num] = boxes[box_num] + [(code, focal)]
    return boxes


def focus_power(boxes: List[List[Tuple[str, int]]]) -> int:
    power = 0
    for box_num, box in enumerate(boxes):
        for lens_num, lens in enumerate(box):
            power += (box_num + 1) * (lens_num + 1) * lens[1]
    return power


assert hash_code(EXAMPLE_HASH) == 52
assert hash_sum(EXAMPLE_STEPS) == 1320
assert focus_power(do_boxes(EXAMPLE_STEPS)) == 145

puzzle_input = read_input("15")

print(hash_sum(puzzle_input))
print(focus_power(do_boxes(puzzle_input)))
