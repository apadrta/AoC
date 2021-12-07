#!/usr/bin/env python
# -*- coding:utf-8 -*-
"""
Advent of code 2021 - Day 7
"""

import argparse


def get_args():
    """
    Cmd line argument parsing (preprocessing)
    """
    # Assign description to the help doc
    parser = argparse.ArgumentParser(
        description='Advent of code 2021: Day 7')

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

    nums = [int(x) for x in data[0].replace('\n', '').replace('\r', '').split(",")]

    # first part
    i = min(nums)
    minfuel = (max(nums) - min(nums)) * len(nums)
    while i < max(nums) + 1:
        fuel = 0
        for num in nums:
            fuel += abs(num-i)
        if fuel < minfuel:
            minfuel = fuel
            minpos = i
        i += 1
    print(f"Part 1 solution: {minfuel}")

    # second part
    consumption = [0]
    i = 1
    maxi = max(nums) - min(nums)
    while i <= maxi:
        consumption.append(consumption[-1] + i)
        i += 1

    i = min(nums)
    minfuel = consumption[(max(nums) - min(nums))] * len(nums)
    while i < max(nums) + 1:
        fuel = 0
        for num in nums:
            fuel += consumption[abs(num-i)]
        i += 1
        if fuel < minfuel:
            minfuel = fuel

    print(f"Part 2 solution: {minfuel}")


if __name__ == '__main__':
    main()

# EOF
