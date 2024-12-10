#!/usr/bin/env python
# -*- coding:utf-8 -*-
"""
Advent of code 2024 - Day 10
"""

import argparse
import numpy as np


def get_args():
    """
    Cmd line argument parsing (preprocessing)
    """
    # Assign description to the help doc
    parser = argparse.ArgumentParser(
        description='Advent of code 2024: Day 10'
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

    width = len(data[0])
    height = len(data)
    zeroes = []
    arr = np.zeros((height, width), int)
    for idx, line in enumerate(data):
        for jdx, char in enumerate(line):
            val = int(char)
            arr[(idx, jdx)] = val
            if val == 0:
                zeroes.append((idx, jdx))
    return arr, zeroes


def count_trailheads(data, start, distinct=True):
    """
    Count number of destination of height 9 from given position of height 0.
    """
    neighbours = [(-1, 0), (1, 0), (0, -1), (0, 1)]
    actlist = [start]
    nextlist = []
    height = 0
    while actlist and height < 9:
        nextlist = []
        for act in actlist:
            for neighbour in neighbours:
                candidate = (act[0] + neighbour[0], act[1] + neighbour[1])
                if data.shape[0] - 1 < candidate[0] or candidate[0] < 0:
                    continue
                if data.shape[1] - 1 < candidate[1] or candidate[1] < 0:
                    continue
                if data[candidate] == height + 1:
                    if not distinct or (distinct and candidate not in nextlist):
                        nextlist.append(candidate)
        actlist = nextlist
        height += 1
    if height < 9:
        return 0
    return len(actlist)


def main():
    """
    Main function
    """

    # process args
    infile = get_args()

    # read data
    data, zeroes = read_data_struct(infile)

    # part 1
    sums = 0
    for zero in zeroes:
        sums += count_trailheads(data, zero, distinct=True)
    print(f"Part 1 solution: {sums}")

    # part 2
    sums = 0
    for zero in zeroes:
        sums += count_trailheads(data, zero, distinct=False)
    print(f"Part 2 solution: {sums}")


if __name__ == '__main__':
    main()

# EOF
