#!/usr/bin/env python
# -*- coding:utf-8 -*-
"""
Advent of code 2021 - Day 2
"""

import argparse
from submarine import ElfSubmarine


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


def main():
    """
    Main function
    """

    # process args
    infile = get_args()

    # create and run submarine
    submarine = ElfSubmarine()
    submarine.read_instructions(infile)
    submarine.navigate()
    print("Solution part 2: {}".format(submarine.get_state_hash()))


if __name__ == '__main__':
    main()

# EOF
