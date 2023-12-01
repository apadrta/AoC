#!/usr/bin/env python
# -*- coding:utf-8 -*-
"""
Advent of code 2023 - Day 1
"""

import argparse


def get_args():
    """
    Cmd line argument parsing (preprocessing)
    """
    # Assign description to the help doc
    parser = argparse.ArgumentParser(
        description='Advent of code 2023: Day 1')

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


def get_number(item):
    """
    get number made from first and last digit
    """
    first = None
    for char in item:
        if char in '0123456789':
            first = char
            break
    last = None
    for char in item[::-1]:
        if char in '0123456789':
            last = char
            break
    if not first or not last:
        return 0
    return int(f"{first}{last}")


def get_number_part2(item):
    """
    get number made from first and last digit
    """
    conv = {'one': 1,
            'two': 2,
            'three': 3,
            'four': 4,
            'five': 5,
            'six': 6,
            'seven': 7,
            'eight': 8,
            'nine': 9,
            '0': 0,
            '1': 1,
            '2': 2,
            '3': 3,
            '4': 4,
            '5': 5,
            '6': 6,
            '7': 7,
            '8': 8,
            '9': 9}

    first = None
    first_pos = len(item) + 1
    for key, value in conv.items():
        pos = item.find(key)
        if first_pos > pos >= 0:
            first_pos = pos
            first = value

    last = None
    last_pos = -1
    for key, value in conv.items():
        pos = item.rfind(key)
        if pos >= 0 and pos > last_pos:
            last_pos = pos
            last = value
    if not first or not last:
        return 0

    return int(f"{first}{last}")


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

    # part 1
    sums = 0
    for item in data:
        sums += get_number(item)
    print("Part 1 solution: {}".format(sums))

    # part 2
    sums = 0
    for item in data:
        sums += get_number_part2(item)
    print("Part 2 solution: {}".format(sums))


if __name__ == '__main__':
    main()

# EOF
