from . import read_input

EXAMPLE = """32T3K 765
T55J5 684
KK677 28
KTJJT 220
QQQJA 483"""

CARD_ORDER = {str(i): i for i in range(2, 10)} | {"T": 10, "J": 11, "Q": 12, "K": 13, "A": 14}
JOKER_ORDER = CARD_ORDER | {"J": 1}


def hand_order(hand: str, joker: bool) -> int:
    cards = list(hand)
    hand_description = {card: hand.count(card) for card in cards}
    if joker:
        joker_count = hand_description.pop("J", 0)
        card_counts = sorted(hand_description.values(), reverse=True)
        if len(card_counts) > 0:
            card_counts[0] += joker_count
        else:
            card_counts = [joker_count]
    else:
        card_counts = sorted(hand_description.values(), reverse=True)

    if card_counts[0] in {4, 5}:
        return card_counts[0] + 1  # returns 6 for 5-of-a-kind and 5 for 4-of-a-kind
    elif card_counts == [3, 2]:
        return 4
    elif card_counts == [3, 1, 1]:
        return 3
    elif card_counts == [2, 2, 1]:
        return 2
    elif card_counts == [2, 1, 1, 1]:
        return 1
    else:
        return 0


def hand_comparator(hand: str, joker: bool) -> int:
    card_order = JOKER_ORDER if joker else CARD_ORDER
    hand_value = hand_order(hand, joker) * (14**6)
    for i, card in enumerate(hand):
        hand_value += card_order[card] * (14 ** (5 - i))
    return hand_value


def bid_sum(all_hands: str, joker: bool) -> int:
    hand_bids = []
    for row in all_hands.splitlines():
        hand_bids.append(tuple(row.split()))
    return sum(
        [
            (i + 1) * int(bid[1])
            for i, bid in enumerate(sorted(hand_bids, key=(lambda hand_bid: hand_comparator(hand_bid[0], joker))))
        ]
    )


assert bid_sum(EXAMPLE, False) == 6440
assert bid_sum(EXAMPLE, True) == 5905

puzzle_input = read_input("07")

print(bid_sum(puzzle_input, False))
print(bid_sum(puzzle_input, True))
