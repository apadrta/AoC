#!/usr/bin/env python
# -*- coding:utf-8 -*-
"""
Advent of code 2022 - Day 6
"""

import argparse


def get_args():
    """
    Cmd line argument parsing (preprocessing)
    """
    # Assign description to the help doc
    parser = argparse.ArgumentParser(
        description='Advent of code 2022: Day 6')

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


def find_pos(data, datalen):
    """
    Find position
    """
    buff = ''
    for idx, value in enumerate(data):

        if value not in buff:
            buff += value
        else:
            buff = buff[buff.find(value)+1:] + value
        if len(buff) == datalen:
            return idx + 1
    return -1


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

    # evaluate part 1
    res = find_pos(data[0], 4)
    print("Part 1 solution: {}".format(res))

    # evaluate part 2
    res = find_pos(data[0], 14)
    print("Part 2 solution: {}".format(res))


if __name__ == '__main__':
    main()

# EOF
