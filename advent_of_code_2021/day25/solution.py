#!/usr/bin/env python
# -*- coding:utf-8 -*-
"""
Advent of code 2021 - Day 25
"""

import argparse
from copy import deepcopy
import numpy as np


def get_args():
    """
    Cmd line argument parsing (preprocessing)
    """
    # Assign description to the help doc
    parser = argparse.ArgumentParser(
        description='Advent of code 2021: Day 25')

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
    lines = [x.strip() for x in data]

    # process data
    max_i = len(lines)
    max_j = len(lines[0])
    sea = np.zeros((max_i, max_j), dtype=int)
    for index_i, line in enumerate(lines):
        for index_j, char in enumerate(line):
            if char == '>':
                sea[(index_i, index_j)] = 1
            if char == 'v':
                sea[(index_i, index_j)] = 2

    # first part
    move = True
    i = 0
    while move:
        # move east/right
        new_sea = deepcopy(sea)
        move = False
        for index_i, line in enumerate(lines):
            for index_j, char in enumerate(line):
                if sea[(index_i, index_j)] == 1 and sea[(index_i, (index_j + 1) % max_j)] == 0:
                    new_sea[(index_i, (index_j + 1) % max_j)] = 1
                    new_sea[(index_i, index_j)] = 0
                    move = True
        sea = new_sea
        # move south/down
        new_sea = deepcopy(sea)
        for index_j, char in enumerate(line):
            for index_i, line in enumerate(lines):
                if sea[(index_i, index_j)] == 2 and sea[((index_i + 1) % max_i, index_j)] == 0:
                    new_sea[((index_i + 1) % max_i, index_j)] = 2
                    new_sea[(index_i, index_j)] = 0
                    move = True
        sea = new_sea
        i += 1
        print(".", end='', flush=True)
    print(f"\nPart 1 solution: {i}")


if __name__ == '__main__':
    main()


# EOF
