#!/usr/bin/env python
# -*- coding:utf-8 -*-
"""
Advent of code 2021 - Day 3
"""

import argparse


def get_args():
    """
    Cmd line argument parsing (preprocessing)
    """
    # Assign description to the help doc
    parser = argparse.ArgumentParser(
        description='Advent of code 2021: Day 3')

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


def make_counts(data):
    """
    Prepare statistical object
    """
    length = len(data[0])
    counts = []
    for pos in range(0, length):
        counts.append({'0': 0, '1': 0})
    # count data
    for num in data:
        for pos in range(0, length):
            counts[pos][num[pos]] += 1
    return counts


def keep_matching_only(data, crit):
    """
    Keep only data matching criterion
    """
    out = []
    for item in data:
        if item[:len(crit)] == crit:
            out.append(item)
    return out


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
    nums = [x.replace('\n', '').replace('\r', '') for x in data]

    # init counters
    counts = make_counts(nums)

    # evaluate data
    gamma = ''
    epsilon = ''
    for item in counts:
        if item['0'] > item['1']:
            gamma += '0'
            epsilon += '1'
        else:
            gamma += '1'
            epsilon += '0'
    print("Part 1 solution: {}".format(int(gamma, 2) * int(epsilon, 2)))

    # init
    o2s = []
    co2s = []
    for num in nums:
        o2s.append(num)
        co2s.append(num)

    # oxygen
    crit_pos = 0
    crit = ''
    while True:
        # create criterion
        counts = make_counts(o2s)
        if counts[crit_pos]['0'] > counts[crit_pos]['1']:
            crit += '0'
        else:
            crit += '1'
        # keep only matching data
        o2s = keep_matching_only(o2s, crit)
        crit_pos += 1
        if len(o2s) == 1:
            break

    # co2
    crit_pos = 0
    crit = ''
    while True:
        # create criterion
        counts = make_counts(co2s)
        if counts[crit_pos]['0'] <= counts[crit_pos]['1']:
            crit += '0'
        else:
            crit += '1'
        # keep only matching data
        co2s = keep_matching_only(co2s, crit)
        crit_pos += 1
        if len(co2s) == 1:
            break
    print("Part 2 solution: {}".format(int(o2s[0], 2) * int(co2s[0], 2)))


if __name__ == '__main__':
    main()

# EOF
