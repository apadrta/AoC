#!/usr/bin/env python
# -*- coding:utf-8 -*-
"""
Advent of code 2024 - Day 1
"""

import argparse


def get_args():
    """
    Cmd line argument parsing (preprocessing)
    """
    # Assign description to the help doc
    parser = argparse.ArgumentParser(
        description='Advent of code 2024: Day 1')

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
    # createle left and right columns
    left = []
    right = []
    for item in data:
        first, second = item.strip().split('   ')
        left.append(int(first))
        right.append(int(second))
    left = sorted(left)
    right = sorted(right)
    return left, right


def count_distance(left, right):
    """
    Count distance between two columns
    """
    sums = 0
    for idx, value in enumerate(left):
        sums += abs(value - right[idx])
    return sums


def count_occurence_weight(left, right):
    """
    Count occurence weight
    """
    occurence = {}
    for item in right:
        if item not in occurence:
            occurence[item] = 0
        occurence[item] += 1
    sums = 0
    for item in left:
        if item in occurence:
            sums += item * occurence[item]
    return sums


def main():
    """
    Main function
    """

    # process args
    infile = get_args()

    # read data
    left, right = read_data(infile)

    # part 1
    print("Part 1 solution: {}".format(count_distance(left, right)))

    # part 2
    print("Part 2 solution: {}".format(count_occurence_weight(left, right)))


if __name__ == '__main__':
    main()

# EOF
