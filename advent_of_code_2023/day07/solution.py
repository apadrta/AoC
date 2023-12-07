#!/usr/bin/env python
# -*- coding:utf-8 -*-
"""
Advent of code 2023 - Day 7
"""

import argparse
from operator import itemgetter


def get_args():
    """
    Cmd line argument parsing (preprocessing)
    """
    # Assign description to the help doc
    parser = argparse.ArgumentParser(
        description='Advent of code 2023: Day 7'
        )

    # Add arguments
    parser.add_argument(
        '-i',
        '--infile',
        type=str,
        help='Inputfilename',
        required=True
        )

    # Array for all arguments passed to script
    args = parser.parse_args()

    # Return arg variables
    return args.infile


def read_data_struct(filename):
    """
    Read data from file and convert it to data structure
    """
    data = []
    with open(filename, "r", encoding="utf-8") as fileh:
        data = fileh.readlines()
    data = [x.strip() for x in data]
    cards = []
    for line in data:
        card = line.split(' ')
        card[1] = int(card[1])
        card.append('')
        cards.append(card)
    return cards


def eval_type(cards, mapping):
    """
    evaluate type of hands and prepare for sorting
    """

    for idx, card in enumerate(cards):
        # count chars
        counter = {}
        for char in card[0]:
            if char not in counter:
                counter[char] = 0
            counter[char] += 1
        if len(counter) == 5:
            card[2] = 'a'  # 'High card'
        elif len(counter) == 1:
            card[2] = 'g'  # 'Five of kind'
        elif len(counter) == 2 and 4 in counter.values():
            card[2] = 'f'  # 'Four of kind'
        elif len(counter) == 3 and 3 in counter.values():
            card[2] = 'd'  # 'Three of kind'
        elif len(counter) == 3 and 2 in counter.values():
            card[2] = 'c'  # 'Two pairs'
        elif len(counter) == 2 and 3 in counter.values() and 2 in counter.values():
            card[2] = 'e'  # 'Full house'
        else:
            card[2] = 'b'  # 'One pair'
        for jdx in range(0, 5):
            card[2] += mapping[card[0][jdx]]
        cards[idx] = card
    return cards


def sort_cards(cards):
    """
    sort card from weakest to strongest (text string in 3rd column)
    """
    cards = sorted(cards, key=itemgetter(2))
    return cards


def convert_joker(cards):
    """
    convert joker card (J) to other card to make hand most powerfull possible + reevaluate values of hands
    """
    # reeval original hand
    cards = eval_type(cards, mapping={'A': 'm', 'K': 'l', 'Q': 'k', 'T': 'j', '9': 'i', '8': 'h', '7': 'g', '6': 'f', '5': 'e', '4': 'd', '3': 'c', '2': 'b', 'J': 'a'})
    # find most powerfull combination
    for idx, card in enumerate(cards):
        if 'J' not in card[0]:
            cards[idx].append('nochange')
            continue
        possible = []
        vals = 'AKQT98765432'
        works = [card[0]]
        while works:
            work = works.pop()
            for val in vals:
                new = work.replace('J', val, 1)
                if 'J' in new:
                    works.append(new)
                else:
                    possible.append([new, card[1], ''])
        possible = eval_type(possible, mapping={'A': 'm', 'K': 'l', 'Q': 'k', 'J': 'j', 'T': 'i', '9': 'h', '8': 'g', '7': 'f', '6': 'e', '5': 'd', '4': 'c', '3': 'b', '2': 'a'})
        for jdx, pos in enumerate(possible):
            pos[2] = pos[2][0]
            possible[jdx] = pos
        possible = sorted(possible, key=itemgetter(2))
        cards[idx][2] = possible[-1][2] + cards[idx][2][1:]
        cards[idx].append(possible[-1][0])
    return cards


def main():
    """
    Main function
    """

    # process args
    infile = get_args()

    # read data
    cards = read_data_struct(infile)

    # part 1
    cards = eval_type(cards, mapping={'A': 'm', 'K': 'l', 'Q': 'k', 'J': 'j', 'T': 'i', '9': 'h', '8': 'g', '7': 'f', '6': 'e', '5': 'd', '4': 'c', '3': 'b', '2': 'a'})
    cards = sort_cards(cards)
    sums = 0
    for idx, card in enumerate(cards):
        sums += (idx + 1) * card[1]
    print(f"Part 1 solution: {sums}")

    # part 2
    cards = convert_joker(cards)
    cards = sort_cards(cards)
    sums = 0
    for idx, card in enumerate(cards):
        sums += (idx + 1) * card[1]
    print(f"Part 2 solution: {sums}")


if __name__ == '__main__':
    main()

# EOF
