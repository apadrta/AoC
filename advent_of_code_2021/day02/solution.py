#!/usr/bin/env python
# -*- coding:utf-8 -*-
"""
Advent of code 2021 - Day 2
"""

import argparse

#==============================================================================


def get_args():
    """
    Cmd line argument parsing (preprocessing)
    """
    # Assign description to the help doc
    parser = argparse.ArgumentParser(
        description='Advent of code 2021: Day 2')

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


#==============================================================================


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
    orders = []
    for item in data:
        [order, value] = item.split(" ", 1)
        orders.append([order, int(value.replace('\n', '').replace('\r', ''))])

    depth = 0
    horizontal = 0
    for order in orders:
        if order[0] == 'forward':
            horizontal += order[1]
        if order[0] == 'up':
            depth -= order[1]
        if order[0] == 'down':
            depth += order[1]
    
    print("Part 1 solution: {}".format(depth * horizontal))

    depth = 0
    horizontal = 0
    aim = 0
    for order in orders:
        if order[0] == 'forward':
            horizontal += order[1]
            depth += aim * order[1]
        if order[0] == 'up':
            aim -= order[1]
        if order[0] == 'down':
            aim += order[1]

    print("Part 2 solution: {}".format(depth * horizontal))
 
#==============================================================================

if __name__ == '__main__':
    main()

# EOF
