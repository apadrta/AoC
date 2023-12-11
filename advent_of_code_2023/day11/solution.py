#!/usr/bin/env python
# -*- coding:utf-8 -*-
"""
Advent of code 2023 - Day 11
"""

import argparse


def get_args():
    """
    Cmd line argument parsing (preprocessing)
    """
    # Assign description to the help doc
    parser = argparse.ArgumentParser(
        description='Advent of code 2023: Day 11'
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

    # detect galaxies
    gals = []
    for idx, line in enumerate(data):
        for jdx, char in enumerate(line):
            if char == '#':
                gals.append([idx, jdx])

    # detect empties
    erows = list(range(0, len(data)))
    ecols = list(range(0, len(data[0])))
    for gal in gals:
        if gal[0] in erows:
            erows.remove(gal[0])
        if gal[1] in ecols:
            ecols.remove(gal[1])

    return gals, erows, ecols


def count_dists(gals, erows, ecols, size=1):
    """
    Count distances
    """
    # create pairs
    pairs = []
    idx = 0
    while idx < len(gals) - 1:
        jdx = idx + 1
        while jdx < len(gals):
            pairs.append([idx, jdx])
            jdx += 1
        idx += 1
    # count distances
    sums = 0
    for pair in pairs:
        # row dist
        mins = min(gals[pair[0]][0], gals[pair[1]][0])
        maxs = max(gals[pair[0]][0], gals[pair[1]][0])
        dist = maxs - mins
        for erow in erows:
            if mins < erow < maxs:
                dist += size
        # cols dist
        mins = min(gals[pair[0]][1], gals[pair[1]][1])
        maxs = max(gals[pair[0]][1], gals[pair[1]][1])
        dist += maxs - mins
        for ecol in ecols:
            if mins < ecol < maxs:
                dist += size
        sums += dist
    return sums


def main():
    """
    Main function
    """

    # process args
    infile = get_args()

    # read data
    gals, erows, ecols = read_data_struct(infile)

    # part 1
    sums = count_dists(gals, erows, ecols, 1)
    print(f"Part 1 solution: {sums}")

    # part 2
    sums = count_dists(gals, erows, ecols, 999999)
    print(f"Part 2 solution: {sums}")


if __name__ == '__main__':
    main()

# EOF
