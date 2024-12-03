#!/usr/bin/env python
# -*- coding:utf-8 -*-
"""
Advent of code 2024 - Day 3
"""

import argparse
import re


def get_args():
    """
    Cmd line argument parsing (preprocessing)
    """
    # Assign description to the help doc
    parser = argparse.ArgumentParser(
        description='Advent of code 2024: Day 3')

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
    return "".join(data)


def main():
    """
    Main function
    """

    # process args
    infile = get_args()

    # read data
    data = read_data(infile)

    # part 1
    sums = 0
    pattern = r"mul\([\d]+,[\d]+\)"
    matches = re.findall(pattern, data)
    for match in matches:
        nums = [int(x) for x in match.replace('mul(', '').replace(')', '').split(',')]
        sums += nums[0] * nums[1]
    print(f"Part 1 solution: {sums}")

    # part 2
    sums = 0
    pattern = r"mul\([\d]+,[\d]+\)|do\(\)|don't\(\)"
    matches = re.findall(pattern, data)
    enabled = True
    for match in matches:
        if match == 'do()':
            enabled = True
            continue
        if match == "don't()":
            enabled = False
            continue
        if enabled:
            nums = [int(x) for x in match.replace('mul(', '').replace(')', '').split(',')]
            sums += nums[0] * nums[1]
    print(f"Part 2 solution: {sums}")


if __name__ == '__main__':
    main()

# EOF
