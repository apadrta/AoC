#!/usr/bin/env python
# -*- coding:utf-8 -*-
"""
Advent of code 2022 - Day 25
"""

import argparse
# import numpy as np


def get_args():
    """
    Cmd line argument parsing (preprocessing)
    """
    # Assign description to the help doc
    parser = argparse.ArgumentParser(
        description='Advent of code 2022: Day 25')

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


def parse_input(lines):
    """
    Preprocess input
    """
    numbers = []
    for line in lines:
        numbers.append(line)
    return numbers


def snafu2dec(snafu):
    """
    convert snafu to decimal
    """
    num = 0
    base = 1
    for char in snafu[::-1]:
        char = int(char.replace('-', '-1').replace('=', '-2'))
        num += base * char
        base = base * 5
    return num


num2snafu = {
    0: '0',
    1: '1',
    2: '2',
    -1: '-',
    -2: '='
}


def sum_snafus(snafu_a, snafu_b):
    """
    returns sum of two snafus
    """
    # make both snafus long enoug
    length = max(len(snafu_a), len(snafu_b)) + 1
    num_a = [0] * (length - len(snafu_a))+[int(x.replace('-', '-1').replace('=', '-2')) for x in snafu_a]
    num_b = [0] * (length - len(snafu_b))+[int(x.replace('-', '-1').replace('=', '-2')) for x in snafu_b]
    res = ''
    over = 0
    for idx in range(length - 1, 0, -1):
        act = num_a[idx] + num_b[idx] + over
        over = 0
        if act == 3:
            act = -2
            over = 1
        elif act == 4:
            act = -1
            over = 1
        elif act == 5:
            act = 0
            over = 1
        elif act == -3:
            act = 2
            over = -1
        elif act == -4:
            act = 1
            over = -1
        elif act == -5:
            act = 0
            over = -1
        res = f'{num2snafu[act]}{res}'
    return res


def solve_part1(numbers):
    """
    sum up snafu numbers
    """
    sums = '0'
    for num in numbers:
        sums = sum_snafus(sums, num)
    return sums


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
    lines = [x.strip() for x in data]

    # preprocess data
    data = parse_input(lines)

    # part 1
    res = solve_part1(data)
    print(f"Part 1 solution: {res} (in dec: {snafu2dec(res)})")


if __name__ == '__main__':
    main()

# EOF
