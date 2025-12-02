#!/usr/bin/env python
# -*- coding:utf-8 -*-
"""
Advent of code 2025 - Day 2
"""

import argparse


def get_args():
    """
    Cmd line argument parsing (preprocessing)
    """
    # Assign description to the help doc
    parser = argparse.ArgumentParser(
        description='Advent of code 2025: Day 1')

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
    with open(filename, "r", encoding='utf8') as fileh:
        data = fileh.readlines()
    data = data[0].strip().split(',')
    ranges = []
    for item in data:
        ranges.append([int(x) for x in item.split('-')] + item.split('-'))
    return ranges


def proces_range(limits):
    """
    process one range and returns list of invalid IDs in it
    """
    # identify length of a half
    halvlen = 0
    res = []
    if len(limits[2]) == len(limits[3]) and len(limits[2]) % 2 == 0:
        halvlen = len(limits[2]) // 2
    elif len(limits[2]) % 2 == 0 and len(limits[3]) % 2 == 1:
        halvlen = len(limits[2]) // 2
    elif len(limits[2]) % 2 == 1 and len(limits[3]) % 2 == 0:
        halvlen = len(limits[3]) // 2
    elif len(limits[2]) == len(limits[3]) and len(limits[2]) % 2 == 1:
        return res
    else:
        print(f'  Unrecognized state {limits}')
        return res

    # check values
    rngfrom = 10**(halvlen-1)
    rngto = 10**(halvlen)
    for idx in range(rngfrom, rngto):
        val = idx + idx * rngto
        if limits[0] <= val <= limits[1]:
            res.append(val)
    return res


def proces_range_reps(limits, reps):
    """
    process one range and returns list of invalid IDs in it
    """
    res = []
    if max(len(limits[2]), len(limits[3])) < reps:
        # too short
        return res
    if len(limits[2]) % reps != 0 and len(limits[3]) % reps != 0:
        # indivisible to reps parts
        return res

    # identify length of a part
    partlen = 0
    if len(limits[2]) == len(limits[3]) and len(limits[2]) % reps == 0:
        partlen = len(limits[2]) // reps
    elif len(limits[2]) % reps == 0 and len(limits[3]) % reps != 0:
        partlen = len(limits[2]) // reps
    elif len(limits[2]) % reps != 0 and len(limits[3]) % reps == 0:
        partlen = len(limits[3]) // reps
    elif len(limits[2]) == len(limits[3]) and len(limits[2]) % reps != 0:
        return res
    else:
        print(f'  Unrecognized state {limits}')
        return res

    # check values
    rngfrom = 10**(partlen-1)
    rngto = 10**(partlen)
    for idx in range(rngfrom, rngto):
        val = idx
        for _ in range(1, reps):
            val = val * rngto + idx
        if limits[0] <= val <= limits[1]:
            res.append(val)
    return res


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
    for item in data:
        vals = proces_range(item)
        for val in vals:
            sums += val
    print(f'Solution part1: {sums}')

    # part 2
    allvals = []
    for size in [2, 3, 5, 7]:
        for item in data:
            vals = proces_range_reps(item, size)
            for val in vals:
                if val not in allvals:
                    allvals.append(val)
    sums = 0
    for val in allvals:
        sums += val
    print(f"Part 2 solution: {sums}")


if __name__ == '__main__':
    main()

# EOF
