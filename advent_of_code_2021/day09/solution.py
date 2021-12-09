#!/usr/bin/env python
# -*- coding:utf-8 -*-
"""
Advent of code 2021 - Day 9
"""

import argparse
import numpy as np


def get_args():
    """
    Cmd line argument parsing (preprocessing)
    """
    # Assign description to the help doc
    parser = argparse.ArgumentParser(
        description='Advent of code 2021: Day 9')

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


border_diffs = [(-1, 0), (1, 0), (0, -1), (0, 1)]


def get_lp(floor):
    """
    Get list of lowpoints heights and list of ther coordinates
    """
    lps = []
    lpsc = []
    i = 0
    while i < np.size(floor, 0):
        j = 0
        while j < np.size(floor, 1):
            islp = True
            for diff in border_diffs:
                if (i == 0 and diff[0] == -1) or (i == np.size(floor, 0) - 1 and diff[0] == 1):
                    continue
                if (j == 0 and diff[1] == -1) or (j == np.size(floor, 1) - 1 and diff[1] == 1):
                    continue
                if floor[(i + diff[0], j + diff[1])] <= floor[(i, j)]:
                    islp = False
                    break
            if islp:
                lps.append(floor[(i, j)])
                lpsc.append((i, j))
            j += 1
        i += 1
    return lps, lpsc


def get_basin(floor, lowpoint):
    """
    Get basin - list of tile coordinates for given lowpoint
    """
    basin = []
    checks = [lowpoint]
    while checks:
        check = checks.pop()
        # skip already processed tiles
        if check in basin:
            continue
        # add processed tile to basin
        basin.append(check)
        # check surrounding tiles if they are part of the basin
        for diff in border_diffs:
            # skip border "outs" checks
            if (check[0] == 0 and diff[0] == -1) or (check[0] == np.size(floor, 0) - 1 and diff[0] == 1):
                continue
            if (check[1] == 0 and diff[1] == -1) or (check[1] == np.size(floor, 1) - 1 and diff[1] == 1):
                continue
            # add tile is higher and not 9
            if floor[(check[0] + diff[0], check[1] + diff[1])] > floor[(check[0], check[1])] and floor[(check[0] + diff[0], check[1] + diff[1])] < 9:
                checks.append((check[0] + diff[0], check[1] + diff[1]))
    return basin


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

    # first part
    floor = np.zeros((len(lines), len(lines[0])), dtype=int)
    i = 0
    for line in lines:
        j = 0
        for char in line:
            floor[(i, j)] = int(char)
            j += 1
        i += 1
    lps, lpsc = get_lp(floor)

    numsum = 0
    for val in lps:
        numsum += val + 1
    print(f"Part 1 solution: {numsum}")

    # second part
    basins_len = []
    for coord in lpsc:
        basins_len.append(len(get_basin(floor, coord)))

    numsum = 1
    for i in range(0, 3):
        numsum *= max(basins_len)
        basins_len.remove(max(basins_len))
    print(f"Part 2 solution: {numsum}")


if __name__ == '__main__':
    main()

# EOF
