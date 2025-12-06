#!/usr/bin/env python
# -*- coding:utf-8 -*-
"""
Advent of Code solution
"""

import argparse
import re


def get_args():
    """
    Cmd line argument parsing (preprocessing)
    """
    # Assign description to the help doc
    parser = argparse.ArgumentParser(
        description='Advent of code 2025 day 6')

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

    data = [re.sub(r"\s+", " ", x).split(' ') for x in data]

    for idx, item in enumerate(data[:-1]):
        data[idx] = [int(x) for x in item]

    return data


def cephalopod_math(data):
    """
    compute math homework part 1
    """
    maxs = len(data[0])
    sums = 0
    for idx in range(0, maxs):
        part = data[0][idx]
        if data[-1][idx] == '+':
            for item in data[1:-1]:
                part += item[idx]
        else:
            for item in data[1:-1]:
                part *= item[idx]
        sums += part
    return sums


def part2(filename):
    """
    process data for parr 2
    """
    data = []
    with open(filename, "r", encoding="utf8") as fhnd:
        data = fhnd.readlines()

    starts = []
    operators = []
    for idx, value in enumerate(data[-1]):
        if value in ['+', '*']:
            starts.append(idx)
            operators.append(value)
    starts.append(len(data[0]))
    all_sum = 0
    for idx, start in enumerate(starts[:-1]):
        size = starts[idx+1] - start - 1
        nums = [''] * size
        for item in data[0:-1]:
            for jdx in range(0, size):
                if item[start + jdx] != ' ':
                    nums[jdx] += item[start + jdx]
        nums = [int(x) for x in nums]
        sums = nums[0]
        if operators[idx] == '+':
            for num in nums[1:]:
                sums += num
        else:
            for num in nums[1:]:
                sums *= num
        all_sum += sums
    return all_sum


def main():
    """
    main
    """

    filename = get_args()
    data = read_data(filename)
    # part 1
    sums = cephalopod_math(data)
    print(f"Solution part 1: {sums}")

    # part 2
    sums = part2(filename)
    print(f"Solution part 2: {sums}")


if __name__ == '__main__':
    main()

# EOF
