#!/usr/bin/env python
# -*- coding:utf-8 -*-
"""
Advent of code 2024 - Day 11
"""

import argparse


def get_args():
    """
    Cmd line argument parsing (preprocessing)
    """
    # Assign description to the help doc
    parser = argparse.ArgumentParser(
        description='Advent of code 2024: Day 11'
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
    nums = [int(x) for x in data[0].split(' ')]
    struct = {}
    for num in nums:
        if num not in struct:
            struct[num] = 0
        struct[num] = struct[num] + 1
    return struct


def blink_at_stones(data, blinks):
    """
    Count numner of stones after given number of blinks
    """
    idx = 0
    while idx < blinks:
        res = {}
        for key, value in data.items():
            if key == 0:
                if 1 not in res:
                    res[1] = 0
                res[1] += value
                continue
            strkey = str(key)
            if len(strkey) > 0 and len(strkey) % 2 == 0:
                midpoint = len(strkey) // 2
                first = int(strkey[:midpoint])
                second = int(strkey[midpoint:])
                if first not in res:
                    res[first] = 0
                res[first] += value
                if second not in res:
                    res[second] = 0
                res[second] += value
                continue
            newnum = key * 2024
            if newnum not in res:
                res[newnum] = 0
            res[newnum] += value
        data = res
        idx += 1
    return data


def main():
    """
    Main function
    """

    # process args
    infile = get_args()

    # read data
    data = read_data_struct(infile)

    # part 1
    res = blink_at_stones(data, 25)
    sums = 0
    for item in res.values():
        sums += item
    print(f"Part 1 solution: {sums}")

    # part 2
    res = blink_at_stones(data, 75)
    sums = 0
    for item in res.values():
        sums += item
    print(f"Part 2 solution: {sums}")


if __name__ == '__main__':
    main()

# EOF
