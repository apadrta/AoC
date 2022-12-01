#!/usr/bin/env python
# -*- coding:utf-8 -*-
"""
Advent of code 2022 - Day 1
"""

import argparse


def get_args():
    """
    Cmd line argument parsing (preprocessing)
    """
    # Assign description to the help doc
    parser = argparse.ArgumentParser(
        description='Advent of code 2022: Day 1')

    # Add arguments
    parser.add_argument(
        '-i',
        '--infile',
        type=str,
        help='Inputfilename',
        required=True)

    # Array for all arguments passed to script
    args = parser.parse_args()

    # Return arg variables
    return args.infile


def main():
    """
    Main function
    """

    # process args
    infile = get_args()

    # read data
    data = []
    with open(infile, "r") as fileh:
        data = fileh.readlines()

    elf_items = [[]]
    for item in data:
        item = item.replace('\n', '').replace('\r', '')
        if item:
            elf_items[-1].append(int(item))
        else:
            elf_items.append([])

    # find elf with most calories
    maxcal = 0
    for bag in elf_items:
        cal = 0
        for item in bag:
            cal += item
        if cal > maxcal:
            maxcal = cal

    print("Part 1 solution: {}".format(maxcal))

    # find three elves with top calories
    elfcal = []
    for bag in elf_items:
        cal = 0
        for item in bag:
            cal += item
        elfcal.append(cal)
    elfcal.sort()
    threesnack = elfcal[-1] + elfcal[-2] + elfcal[-3]

    print("Part 2 solution: {}".format(threesnack))


if __name__ == '__main__':
    main()

# EOF
