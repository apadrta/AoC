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
        description='Advent of code 2025 day 1')

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

    codes = []
    for item in data:
        value = int(item[1:])
        if item[0] == 'L':
            value = value * -1
        codes.append(value)
    return codes


def main():
    """
    main
    """

    filename = get_args()
    data = read_data(filename)

    # part 2
    act = 50
    sums1 = 0
    sums2 = 0
    for item in data:
        # count whole spin (part 2)
        div = 100
        if item < 0:
            div = -100
        sums2 += item // div
        item = item % div
        # count moving over zero (part 2)
        if item > 0 and act + item > 99:
            sums2 += 1
        if act and item < 0 and act + item < 1:
            sums2 += 1
        # move and count if ends on zero (part 1)
        act = (act + item) % 100
        if not act:
            sums1 += 1

    print(f"Solution part1: {sums1}")
    print(f"Solution part2: {sums2}")


if __name__ == '__main__':
    main()

# EOF
