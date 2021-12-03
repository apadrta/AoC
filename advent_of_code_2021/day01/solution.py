#!/usr/bin/env python
# -*- coding:utf-8 -*-
"""
Advent of code 2021 - Day 1
"""

import argparse


def get_args():
    """
    Cmd line argument parsing (preprocessing)
    """
    # Assign description to the help doc
    parser = argparse.ArgumentParser(
        description='Advent of code 2021: Day 1')

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
    nums = [int(x.replace('\n', '').replace('\r', '')) for x in data]

    inc = 0
    last = nums[0]
    for num in nums[1:]:
        if num - last > 0:
            inc += 1
        last = num
    print("Part 1 solution: {}".format(inc))

    i = 0
    nums2 = []
    while i < len(nums) - 2:
        nums2.append(nums[i] + nums[i+1] + nums[i+2])
        i += 1

    inc = 0
    last = nums2[0]
    for num in nums2[1:]:
        if num - last > 0:
            inc += 1
        last = num
    print("Part 2 solution: {}".format(inc))


if __name__ == '__main__':
    main()

# EOF
