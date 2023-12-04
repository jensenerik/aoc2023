from typing import Dict

from . import read_input

DIGITS = {str(digit): digit for digit in range(10)}  # map from string representation to integer for 1 digit ints

WORD_DIGITS = DIGITS | {
    "one": 1,
    "two": 2,
    "three": 3,
    "four": 4,
    "five": 5,
    "six": 6,
    "seven": 7,
    "eight": 8,
    "nine": 9,
}

EXAMPLE_TEXT = """1abc2
pqr3stu8vwx
a1b2c3d4e5f
treb7uchet"""

WORD_EXAMPLE_TEXT = """two1nine
eightwothree
abcone2threexyz
xtwone3four
4nineeightseven2
zoneight234
7pqrstsixteen"""


def first_last_digit(mixed_alphanum: str, digits: Dict[str, int], first: bool) -> int:
    """
    Searches in mixed_alphanum for keys of digits.
    Returns value of digits for first (if first is True) or last found key.
    Iterates over unlimited windows, which could be limited to max key length.
    """
    for limit in range(len(mixed_alphanum)):
        for key in digits:
            if key in (mixed_alphanum[: limit + 1] if first else mixed_alphanum[-limit - 1 :]):
                return digits[key]
    raise Exception(f"{mixed_alphanum} has no {'first' if first else 'last'} digit")


def first_and_last_sum(alphanum_text: str, digits: Dict[str, int]) -> int:
    """
    Sums up integers from first and last digits of a collection of lines.
    Doesn't construct a two-digit number, decimalizes manually.
    """
    running_sum = 0
    lines = alphanum_text.splitlines()
    for line in lines:
        running_sum += 10 * first_last_digit(line, digits, True)
        running_sum += first_last_digit(line, digits, False)
    return running_sum


assert first_and_last_sum(EXAMPLE_TEXT, DIGITS) == 142
assert first_and_last_sum(WORD_EXAMPLE_TEXT, WORD_DIGITS) == 281

input_text = read_input("01")

print(first_and_last_sum(input_text, DIGITS))
print(first_and_last_sum(input_text, WORD_DIGITS))
