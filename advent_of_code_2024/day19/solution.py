#!/usr/bin/env python
# -*- coding:utf-8 -*-
"""
Advent of code 2024 - Day 19
"""

import argparse
from copy import deepcopy


def get_args():
    """
    Cmd line argument parsing (preprocessing)
    """
    # Assign description to the help doc
    parser = argparse.ArgumentParser(
        description='Advent of code 2024: Day 19'
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

    towels = data[0].split(', ')
    patterns = data[2:]

    return towels, patterns


def split_towels(pattern, towels, first_only):
    """
    return 1 if pattern can be made from given towels
    """
    states = [pattern]
    finals = 0
    cnt = 0
    while states:
        act = states.pop()
        cnt += 1
        if cnt % 10000 == 0:
            print(f"{len(act)}, {act}, {len(states)} ")
        if act == '':
            finals += 1
            if first_only:
                break
        for towel in towels:
            if act.startswith(towel):
                new = deepcopy(act)
                new = new[len(towel):]
                states.append(new)
    return finals


def search_dp2(pattern, towels):
    """
    searching all combinations using DP (just number o paths)
    """
    # initialize idxtable
    idxtable = []
    for _ in range(0, len(pattern) + 1):
        idxtable.append(0)
    idxtable[0] = 1
    # fill idxtable
    for idx in range(1, len(pattern) + 1):
        for towel in towels:
            if idx >= len(towel) and pattern[idx - len(towel):idx] == towel:
                idxtable[idx] += idxtable[idx - len(towel)]
    return idxtable[-1]


def main():
    """
    Main function
    """

    # process args
    infile = get_args()

    # read data
    towels, patterns = read_data_struct(infile)

    # part 1
    sums = 0
    for pattern in patterns:
        sums += split_towels(pattern, towels, True)
    print(f"Part 1 solution: {sums}")

    # part 2
    sums = 0
    for pattern in patterns:
        print('.', end='', flush=True)
        sums += search_dp2(pattern, towels)
    print(f"\nPart 2 solution: {sums}")


if __name__ == '__main__':
    main()

# EOF
