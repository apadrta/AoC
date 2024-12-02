#!/usr/bin/env python
# -*- coding:utf-8 -*-
"""
Advent of code 2024 - Day 2
"""

import argparse


def get_args():
    """
    Cmd line argument parsing (preprocessing)
    """
    # Assign description to the help doc
    parser = argparse.ArgumentParser(
        description='Advent of code 2024: Day 2')

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
    # createle array of reports
    reports = []
    for item in data:
        reports.append([int(x) for x in item.strip().split(' ')])
    return reports


def is_safe(report):
    """
    Check if report is safe
    """
    direction = report[1] - report[0]
    idx = 1
    while idx < len(report):
        diff = report[idx] - report[idx - 1]
        # check abs difference from 1 to 3
        if abs(diff) < 1 or abs(diff) > 3:
            return False
        # check direction
        if direction < 0 < diff:
            return False
        if direction > 0 > diff:
            return False
        idx += 1
    return True


def main():
    """
    Main function
    """

    # process args
    infile = get_args()

    # read data
    reports = read_data(infile)

    # part 1
    sums = 0
    for report in reports:
        if is_safe(report):
            sums += 1
    print(f"Part 1 solution: {sums}")

    # part 2
    sums = 0
    for report in reports:
        if is_safe(report):
            sums += 1
        else:
            idx = 0
            while idx < len(report):
                if is_safe(report[:idx]+report[idx+1:]):
                    sums += 1
                    break
                idx += 1
    print(f"Part 2 solution: {sums}")


if __name__ == '__main__':
    main()

# EOF
