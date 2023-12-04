#!/usr/bin/env python
# -*- coding:utf-8 -*-
"""
Advent of code 2023 - Day 3
"""

import argparse


def get_args():
    """
    Cmd line argument parsing (preprocessing)
    """
    # Assign description to the help doc
    parser = argparse.ArgumentParser(
        description='Advent of code 2023: Day 3'
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
    data = [x.replace('  ', ' ').strip() for x in data]
    cards = []
    for item in data:
        cardid, carddata = item.split(': ')
        cardid = cardid.split(' ')[-1]
        win, have = carddata.split(' | ')
        win = set(int(x.strip()) for x in win.split(' '))
        have = set(int(x.strip()) for x in have.split(' '))
        inter = len(win.intersection(have))
        cards.append({'win': win, 'have': have, 'number': 1, 'value': inter})
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
    sums = 0
    for card in cards:
        sums += int(2**(card['value'] - 1))
    print(f"Part 1 solution: {sums}")

    # part 2
    idx = 0
    while idx < len(cards):
        jdx = idx + 1
        while jdx < idx + cards[idx]['value'] + 1:
            cards[jdx]['number'] += cards[idx]['number']
            jdx += 1
            if jdx == len(cards):
                break
        idx += 1
    sums = 0
    for card in cards:
        sums += card['number']
    print(f"Part 2 solution: {sums}")


if __name__ == '__main__':
    main()

# EOF
