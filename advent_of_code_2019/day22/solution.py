#!/usr/bin/env python
# -*- coding:utf-8 -*-
"""
Advent of code 2019 Day 22
"""


import argparse


def get_args():
    """
    Cmd line argument parsing (preprocessing)
    """
    # Assign description to the help doc
    parser = argparse.ArgumentParser(
        description='Advent of code 2019 Day 22')

    # Add arguments
    parser.add_argument(
        '-i',
        '--infile',
        type=str,
        help='Inputfilename',
        required=True)
    parser.add_argument(
        '-d',
        '--decksize',
        type=int,
        help='Size of card deck',
        required=True)

    # Array for all arguments passed to script
    args = parser.parse_args()

    # Return arg variables
    return args.infile, args.decksize


class ElfCardDeck():
    """
    Elf card deck
    """

    def __init__(self):
        """
        Constructor
        """
        self.first = None
        self.last = None
        self.next_idx = None
        self.prev_idx = None
        self.data = None

    def create_deck(self, number):
        """
        Add cards into deck
        """
        idx = 0
        self.data = []
        self.next_idx = 1
        self.prev_idx = 2

        while idx < number:
            self.data.append([idx, idx + 1, idx - 1])
            idx += 1
        self.first = 0
        self.last = len(self.data) - 1
        self.data[self.first][self.prev_idx] = None
        self.data[self.last][self.next_idx] = None

    def print_deck(self):
        """
        Print deck
        """
        idx = self.first
        while idx is not None:
            print(f' {self.data[idx][0]}', end='')
            idx = self.data[idx][self.next_idx]
        print('\n', end='')

    def deal_into_new_stack(self):
        """
        Deal into new stack
        """
        tmp = self.last
        self.last = self.first
        self.first = tmp
        tmp = self.next_idx
        self.next_idx = self.prev_idx
        self.prev_idx = tmp

    def cut_cards(self, cutpos):
        """
        Cut N cards
        """
        # find cutting position
        if cutpos > 0:
            pos = self.first
            idx = 0
            while idx < cutpos:
                pos = self.data[pos][self.next_idx]
                idx += 1
            pre_pos = self.data[pos][self.prev_idx]
        else:
            pos = self.last
            idx = cutpos
            while idx < -1:
                pos = self.data[pos][self.prev_idx]
                idx += 1
            pre_pos = self.data[pos][self.prev_idx]
        # rearange pointers
        self.data[self.last][self.next_idx] = self.first
        self.data[self.first][self.prev_idx] = self.last
        self.data[pos][self.prev_idx] = None
        self.data[pre_pos][self.next_idx] = None
        self.first = pos
        self.last = pre_pos

    def deal_with_increment(self, inc):
        """
        Deal with increment
        """
        new_data = [None] * len(self.data)
        target = 0
        pos = self.first
        while pos is not None:
            new_data[target] = [self.data[pos][0], target + 1, target - 1]
            pos = self.data[pos][self.next_idx]
            target = (target + inc) % len(self.data)
        self.data = new_data
        self.next_idx = 1
        self.prev_idx = 2
        self.first = 0
        self.last = len(self.data) - 1
        self.data[self.first][self.prev_idx] = None
        self.data[self.last][self.next_idx] = None

    def get_position(self, number):
        """
        Find position of fiven card number
        """
        pos = self.first
        idx = 0
        while self.data[pos][0] != number:
            pos = self.data[pos][self.next_idx]
            idx += 1
            if pos is None:
                return None
        return idx


def parse_data(lines):
    """
    Main function
    """
    insts = []
    for line in lines:
        if 'stack' in line:
            insts.append(['stack'])
        if 'increment' in line:
            insts.append(['increment', int(line.split(' ')[-1])])
        if 'cut' in line:
            insts.append(['cut', int(line.split(' ')[-1])])
    return insts


def main():
    """
    Main function
    """

    # process args
    infile, decksize = get_args()

    # read data
    data = []
    with open(infile, "r") as fileh:
        data = fileh.readlines()
    lines = [x.replace('\n', '').replace('\r', '') for x in data]
    orders = parse_data(lines)
    # part one
    deck = ElfCardDeck()
    deck.create_deck(decksize)
    for order in orders:
        print(order)
        if order[0] == 'stack':
            deck.deal_into_new_stack()
        elif order[0] == 'cut':
            deck.cut_cards(order[1])
        elif order[0] == 'increment':
            deck.deal_with_increment(order[1])
    res = deck.get_position(2019)
    print(f"Solution of part 1: {res}")

    # part two
#    print(f"Solution of part 2: {res}")


if __name__ == '__main__':
    main()

# EOF
