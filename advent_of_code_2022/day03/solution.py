#!/usr/bin/env python
# -*- coding:utf-8 -*-
"""
Advent of code 2022 - Day 3
"""

import argparse
import string


def get_args():
    """
    Cmd line argument parsing (preprocessing)
    """
    # Assign description to the help doc
    parser = argparse.ArgumentParser(
        description='Advent of code 2022: Day 3')

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


def item_priority(item):
    """
    Returns elf priority of elf item
    """
    if item in string.ascii_lowercase:
        return ord(item) - 96
    return ord(item) - 38


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
    rucksacks = []
    for line in data:
        line = line.replace('\n', '').replace('\r', '')
        comp1 = set(line[:int(len(line)/2)])
        comp2 = set(line[int(len(line)/2):])
        rucksacks.append([comp1, comp2, comp1.intersection(comp2)])

    priorsum = 0
    for rucksack in rucksacks:
        priorsum += item_priority(list(rucksack[2])[0])

    print("Part 1 solution: {}".format(priorsum))

    badgesum = 0
    idx = 0
    interset = set()
    for line in data:
        line = line.replace('\n', '').replace('\r', '')
        # compute intersection of sets
        if idx % 3 == 0:
            interset = set(line)
        else:
            interset = interset.intersection(set(line))
        # add badge value to sum
        if idx % 3 == 2:
            badgesum += item_priority(list(interset)[0])
        idx += 1

    print("Part 2 solution: {}".format(badgesum))


if __name__ == '__main__':
    main()

# EOF
