#!/usr/bin/env python
# -*- coding:utf-8 -*-
"""
Advent of Code solution
"""

import argparse


def get_args():
    """
    Cmd line argument parsing (preprocessing)
    """
    # Assign description to the help doc
    parser = argparse.ArgumentParser(
        description='Advent of code 2025 day 4')

    # Add arguments
    parser.add_argument(
        '-i',
        '--infile',
        type=str,
        help='Input filename',
        required=True)

    # Array for all arguments passed to script
    args = parser.parse_args()

    # Return arg variables
    return args.infile


def read_data(filename):
    """
    read input data
    """
    data = []
    with open(filename, "r", encoding="utf8") as fhnd:
        data = fhnd.readlines()
    data = [x.strip() for x in data]

    ranges = []
    nums = []
    first = 1
    for line in data:
        if not line:
            first = 0
            continue
        if first:
            ranges.append(tuple(int(x) for x in line.split('-')))
        else:
            nums.append(int(line))

    return ranges, nums


def process_ranges(rngs):
    """
    merge overlapping ranges
    """
    rngs = sorted(rngs)

    merged = [rngs[0]]
    for start, end in rngs[1:]:
        last_start, last_end = merged[-1]
        if start <= last_end:
            merged[-1] = (last_start, max(last_end, end))
        else:
            merged.append((start, end))

    return merged


def main():
    """
    main
    """

    filename = get_args()
    rngs, nums = read_data(filename)

    # part 1
    sums = 0
    for num in nums:
        for rng in rngs:
            if rng[0] <= num <= rng[1]:
                sums += 1
                break
    print(f"Solution part1: {sums}")

    # part 2
    rngs2 = process_ranges(rngs)
    sums = 0
    for item in rngs2:
        sums += item[1] - item[0] + 1
    print(f"Solution part2: {sums}")


if __name__ == '__main__':
    main()

# EOF
