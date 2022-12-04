#!/usr/bin/env python
# -*- coding:utf-8 -*-
"""
Advent of code 2022 - Day 4
"""

import argparse


def get_args():
    """
    Cmd line argument parsing (preprocessing)
    """
    # Assign description to the help doc
    parser = argparse.ArgumentParser(
        description='Advent of code 2022: Day 4')

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

    # prepare data
    tasks = []
    for line in data:
        line = line.replace('\n', '').replace('\r', '').replace('-', ',')
        tasks.append([int(x) for x in line.split(',')])

    # evaluate part 1
    oversum = 0
    for task in tasks:
        if task[0] >= task[2] and task[1] <= task[3]:
            oversum += 1
        elif task[0] <= task[2] and task[1] >= task[3]:
            oversum += 1
    print("Part 1 solution: {}".format(oversum))

    # evaluate part 2
    oversum = 0
    for task in tasks:
        if task[1] >= task[2] and task[0] <= task[3]:
            oversum += 1
    print("Part 2 solution: {}".format(oversum))


if __name__ == '__main__':
    main()

# EOF
