#!/usr/bin/env python
# -*- coding:utf-8 -*-
"""
Advent of code 2024 - Day 25
"""

import argparse


def get_args():
    """
    Cmd line argument parsing (preprocessing)
    """
    # Assign description to the help doc
    parser = argparse.ArgumentParser(
        description='Advent of code 2024: Day 25')

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


def read_data(filename):
    """
    Read and prepare data
    """
    # read file
    data = []
    with open(filename, "r") as fileh:
        data = fileh.readlines()
    data = [x.replace('\r', '').replace('\n', '') for x in data]

    parts = []
    part = []
    for item in data:
        if item:
            part.append(item)
        else:
            parts.append(part)
            part = []
    if part:
        parts.append(part)
    return parts


def eval_data(data):
    """
    Split data to keys and locks
    """
    keys = []
    locks = []
    for item in data:
        new = [0, 0, 0, 0, 0]
        if item[0] == '#####':
            for idx, row in enumerate(item):
                for jdx, char in enumerate(row):
                    if char == '#':
                        new[jdx] = idx
            locks.append(new)
        else:
            for idx, row in enumerate(item[::-1]):
                for jdx, char in enumerate(row):
                    if char == '#':
                        new[jdx] = idx
            keys.append(new)

    return keys, locks


def fit(key, lock):
    """
    Return true if key fits in lock
    """
    for idx, value in enumerate(key):
        if value + lock[idx] > 5:
            return False
    return True


def main():
    """
    Main function
    """

    # process args
    infile = get_args()

    # read data
    data = read_data(infile)

    # part 1
    keys, locks = eval_data(data)
    sums = 0
    for lock in locks:
        for key in keys:
            if fit(key, lock):
                sums += 1
    print(f"Part 1 solution: {sums}")


if __name__ == '__main__':
    main()

# EOF
