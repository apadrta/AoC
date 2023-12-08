#!/usr/bin/env python
# -*- coding:utf-8 -*-
"""
Advent of code 2023 - Day 8
"""

import argparse
from math import lcm


def get_args():
    """
    Cmd line argument parsing (preprocessing)
    """
    # Assign description to the help doc
    parser = argparse.ArgumentParser(
        description='Advent of code 2023: Day 8'
        )

    # Add arguments
    parser.add_argument(
        '-i',
        '--infile',
        type=str,
        help='Inputfilename',
        required=True
        )

    # Array for all arguments passed to script
    args = parser.parse_args()

    # Return arg variables
    return args.infile


def read_data_struct(filename):
    """
    Read data from file and convert it to data structure
    """
    data = []
    with open(filename, "r", encoding="utf-8") as fileh:
        data = fileh.readlines()
    data = [x.strip() for x in data]
    # prepare directions manual (0 left, 1 right)
    directions = [int(x) for x in data[0].replace('L', '0').replace('R', '1')]
    maps = {}
    for line in data[2:]:
        src, dst = line.split(' = ')
        maps[src] = dst[1:-1].split(', ')
    return directions, maps


def move_to_zzz(dirs, maps, src='AAA', dst='ZZZ'):
    """
    Move from src (default AAA) to dst (default ZZZ) node
    """
    pos = src
    inst = 0
    steps = 0
    while pos != dst:
        pos = maps[pos][dirs[inst]]
        steps += 1
        inst = (inst + 1) % len(dirs)
    return steps


def move_to_z(dirs, maps, src='AAA'):
    """
    Move from src node (default AAA) to any node ending by Z
    """
    pos = src
    inst = 0
    steps = 0
    while pos[2] != 'Z':
        pos = maps[pos][dirs[inst]]
        steps += 1
        inst = (inst + 1) % len(dirs)
    return steps


def move_to_zzzs(dirs, maps):
    """
    MOVE from .*A to (.*Z) in optimal way
    """
    pos = []
    for point in maps:
        if point[2] == 'A':
            pos.append(point)
    lens = []
    for point in pos:
        lens.append(move_to_z(dirs, maps, point))
    res = 1
    for num in lens:
        res = lcm(res, num)
    return res


def main():
    """
    Main function
    """

    # process args
    infile = get_args()

    # read data
    dirs, maps = read_data_struct(infile)

    # part 1
    sums = 0
    sums = move_to_zzz(dirs, maps)
    print(f"Part 1 solution: {sums}")

    # part 2
    sums = move_to_zzzs(dirs, maps)
    print(f"Part 2 solution: {sums}")


if __name__ == '__main__':
    main()

# EOF
