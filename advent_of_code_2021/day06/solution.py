#!/usr/bin/env python
# -*- coding:utf-8 -*-
"""
Advent of code 2021 - Day 6
"""

import argparse


def get_args():
    """
    Cmd line argument parsing (preprocessing)
    """
    # Assign description to the help doc
    parser = argparse.ArgumentParser(
        description='Advent of code 2021: Day 4')

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

    # first part
    lfishes = [int(x) for x in data[0].replace('\n', '').replace('\r', '').split(",")]
    day = 0
    while day < 80:
        new = []
        i = 0
        while i < len(lfishes):
            if lfishes[i] > 0:
                lfishes[i] -= 1
            else:
                lfishes[i] = 6
                new.append(8)
            i += 1
        lfishes += new
        day += 1
    print(f"Part 1 solution: {len(lfishes)}")

    # second part
    lfishes = [int(x) for x in data[0].replace('\n', '').replace('\r', '').split(",")]
    fishdict = {}
    for i in range(0, 9):
        fishdict[i] = 0
    for fish in lfishes:
        fishdict[fish] += 1

    day = 0
    while day < 256:
        i = 0
        newdict = {}
        for i in range(0, 9):
            newdict[i] = 0
        for key, value in fishdict.items():
            if key > 0:
                newdict[key-1] += value
            else:
                newdict[6] += value
                newdict[8] += value
            i += 1
        fishdict = newdict
        day += 1

    sums = 0
    for value in fishdict.values():
        sums += value
    print(f"Part 2 solution: {sums}")


if __name__ == '__main__':
    main()

# EOF
