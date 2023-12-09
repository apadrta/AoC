#!/usr/bin/env python
# -*- coding:utf-8 -*-
"""
Advent of code 2023 - Day 9
"""

import argparse


def get_args():
    """
    Cmd line argument parsing (preprocessing)
    """
    # Assign description to the help doc
    parser = argparse.ArgumentParser(
        description='Advent of code 2023: Day 9'
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
    reports = []
    for line in data:
        reports.append([int(x) for x in line.split(' ')])
    return reports


def oasis_predict(report):
    """
    Predict one step
    """
    # generate layes
    steps = [report]
    while True:
        new = []
        for idx, val in enumerate(steps[-1][:-1]):
            new.append(steps[-1][idx + 1] - val)
        steps.append(new)
        zeroes = True
        for val in new:
            if val != 0:
                zeroes = False
                break
        if zeroes:
            break
    # predict afterward
    after = 0
    for idx in range(len(steps) - 2, -1, -1):
        after = steps[idx][-1] + after
    # predict before
    before = 0
    for idx in range(len(steps) - 2, -1, -1):
        before = steps[idx][0] - before
    return after, before


def main():
    """
    Main function
    """

    # process args
    infile = get_args()

    # read data
    reports = read_data_struct(infile)
    # part 1 & part 2
    sums1 = 0
    sums2 = 0
    for report in reports:
        part1, part2 = oasis_predict(report)
        sums1 += part1
        sums2 += part2
    print(f"Part 1 solution: {sums1}")
    print(f"Part 2 solution: {sums2}")


if __name__ == '__main__':
    main()

# EOF
