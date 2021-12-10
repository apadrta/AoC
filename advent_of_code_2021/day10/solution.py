#!/usr/bin/env python
# -*- coding:utf-8 -*-
"""
Advent of code 2021 - Day 10
"""

import argparse
from statistics import median


def get_args():
    """
    Cmd line argument parsing (preprocessing)
    """
    # Assign description to the help doc
    parser = argparse.ArgumentParser(
        description='Advent of code 2021: Day 10')

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


open_chars = ['(', '{', '[', '<']
close_chars = {'(': ')', '{': '}', '[': ']', '<': '>'}
bad_value = {')': 3, ']': 57, '}': 1197, '>': 25137}
complete_value = {')': 1, ']': 2, '}': 3, '>': 4}


def find_corruption(string):
    """
    Find corrupted char in given string
    """
    opens = ''
    for char in string:
        if char in open_chars:
            opens += char
        else:
            if close_chars[opens[-1]] == char:
                opens = opens[:-1]
            else:
                return char
    return ''


def score_to_complete(string):
    """
    Complete line
    """
    opens = ''
    for char in string:
        if char in open_chars:
            opens += char
        else:
            opens = opens[:-1]
    app = ''
    while opens:
        app += close_chars[opens[-1]]
        opens = opens[:-1]
    score = 0
    for char in app:
        score = score * 5 + complete_value[char]
    return score


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

    # part 1
    numsum = 0
    for line in lines:
        corr = find_corruption(line)
        if corr:
            numsum += bad_value[corr]
    print(f"Part 1 solution: {numsum}")

    # part 2
    numsum = 0
    scores = []
    for line in lines:
        corr = find_corruption(line)
        if corr:
            continue
        scores.append(score_to_complete(line))
    print(f"Part 2 solution: {median(scores)}")


if __name__ == '__main__':
    main()

# EOF
