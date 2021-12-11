#!/usr/bin/env python
# -*- coding:utf-8 -*-
"""
Advent of code 2021 - Day 11
"""

import argparse
import numpy as np


def get_args():
    """
    Cmd line argument parsing (preprocessing)
    """
    # Assign description to the help doc
    parser = argparse.ArgumentParser(
        description='Advent of code 2021: Day 11')

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


border_diffs = [(-1, 0), (1, 0), (0, -1), (0, 1), (-1, -1), (-1, 1), (1, -1), (1, 1)]


def energy_round(energy):
    """
    Get list of lowpoints heights and list of ther coordinates
    """
    i = 0
    # step 1: increase all tiles by one
    while i < np.size(energy, 0):
        j = 0
        while j < np.size(energy, 1):
            energy[(i, j)] += 1
            j += 1
        i += 1
    # step 2: flashing
    flash_ah = 0
    flashed = []
    i = 0
    while i < np.size(energy, 0):
        j = 0
        while j < np.size(energy, 1):
            if (i, j) in flashed:
                # already flashed (must end with zero)
                energy[(i, j)] = 0
                j += 1
                continue
            if energy[(i, j)] > 9:
                # tile fleshs
                flash_ah += 1
                flashed.append((i, j))
                energy[(i, j)] = 0
                # increase energy in border tiles
                for diff in border_diffs:
                    if (i == 0 and diff[0] == -1) or (i == np.size(energy, 0) - 1 and diff[0] == 1):
                        continue
                    if (j == 0 and diff[1] == -1) or (j == np.size(energy, 1) - 1 and diff[1] == 1):
                        continue
                    energy[(i + diff[0], j + diff[1])] += 1
                # reset counters
                i = -1
                j = np.size(energy, 1)
            j += 1
        i += 1
    return energy, flash_ah


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
    energy = np.zeros((len(lines), len(lines[0])), dtype=int)
    i = 0
    for line in lines:
        j = 0
        for char in line:
            energy[(i, j)] = int(char)
            j += 1
        i += 1

    numsum = 0
    for i in range(0, 100):
        energy, flashes = energy_round(energy)
        # print(energy, flashes)
        numsum += flashes
    print(f"Part 1 solution: {numsum}")

    # second part
    energy = np.zeros((len(lines), len(lines[0])), dtype=int)
    i = 0
    for line in lines:
        j = 0
        for char in line:
            energy[(i, j)] = int(char)
            j += 1
        i += 1

    i = 0
    target_flashes = np.size(energy, 0) * np.size(energy, 1)
    while True:
        energy, flashes = energy_round(energy)
        if flashes >= target_flashes:
            break
        if i >= 1000:
            print("safe brake activated, uiii")
            break
        i += 1
    print(f"Part 2 solution: {i+1}")


if __name__ == '__main__':
    main()

# EOF
