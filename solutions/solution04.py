from . import read_input

EXAMPLE = """Card 1: 41 48 83 86 17 | 83 86  6 31 17  9 48 53
Card 2: 13 32 20 16 61 | 61 30 68 82 17 32 24 19
Card 3:  1 21 53 59 44 | 69 82 63 72 16 21 14  1
Card 4: 41 92 73 84 69 | 59 84 76 51 58  5 54 83
Card 5: 87 83 26 28 32 | 88 30 70 12 93 22 82 36
Card 6: 31 18 13 56 72 | 74 77 10 23 35 67 36 11"""


def card_value(single_card: str) -> int:
    split_card = single_card.split(":")[1].split("|")
    winning_nums = set([int(item) for item in split_card[0].split()])
    card_nums = set([int(item) for item in split_card[1].split()])
    return len(winning_nums.intersection(card_nums))


def sum_up_cards(all_cards: str) -> int:
    running_sum = 0
    for card in all_cards.splitlines():
        card_overlap = card_value(card)
        running_sum += 2 ** (card_overlap - 1) if card_overlap > 0 else 0
    return running_sum


def card_accumulator(all_cards: str) -> int:
    indiv_cards = all_cards.splitlines()
    card_counts = {i: 1 for i in range(len(indiv_cards))}  # zero-based index
    for card_num, card in enumerate(indiv_cards):
        card_overlap = card_value(card)
        if card_overlap > 0:
            for j in range(1, card_overlap + 1):
                card_counts[card_num + j] = card_counts[card_num + j] + card_counts[card_num]
    return sum(card_counts.values())


assert sum_up_cards(EXAMPLE) == 13
assert card_accumulator(EXAMPLE) == 30

puzzle_input = read_input("04")

print(sum_up_cards(puzzle_input))
print(card_accumulator(puzzle_input))
