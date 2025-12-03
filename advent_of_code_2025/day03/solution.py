#!/usr/bin/env python
# -*- coding:utf-8 -*-
"""
Advent of Code solution
"""

import argparse


def get_args():
    """
    Cmd line argument parsing (preprocessing)
    """
    # Assign description to the help doc
    parser = argparse.ArgumentParser(
        description='Advent of code 2025 day 3')

    # Add arguments
    parser.add_argument(
        '-i',
        '--infile',
        type=str,
        help='Input filename',
        required=True)

    # Array for all arguments passed to script
    args = parser.parse_args()

    # Return arg variables
    return args.infile


def read_data(filename):
    """
    read input data
    """
    data = []
    with open(filename, "r", encoding="utf8") as fhnd:
        data = fhnd.readlines()
    data = [x.strip() for x in data]

    banks = []
    for item in data:
        banks.append([int(x) for x in item])

    return banks


def get_max(bank, maxs):
    """
    get maxs maximal numbers from left in given bank
    """
    nums = []
    first = 0
    last = len(bank) - maxs
    for _ in range(0, maxs):
        max_value = max(bank[first:last + 1])
        max_index = bank[first:last + 1].index(max_value)
        first = first + max_index + 1
        last = last + 1
        nums.append(max_value)

    jolts = 0
    for num in nums:
        jolts = jolts * 10 + num

    return jolts


def main():
    """
    main
    """

    filename = get_args()
    data = read_data(filename)

    # part 1
    sums = 0
    for item in data:
        sums += get_max(item, 2)

    print(f"Solution part 1: {sums}")

    # part 2
    sums = 0
    for item in data:
        sums += get_max(item, 12)

    print(f"Solution part 2: {sums}")


if __name__ == '__main__':
    main()

# EOF
