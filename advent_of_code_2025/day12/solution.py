#!/usr/bin/env python
# -*- coding:utf-8 -*-
"""
Advent of Code solution
"""

import argparse


def get_args():
    """
    Cmd line argument parsing (preprocessing)
    """
    # Assign description to the help doc
    parser = argparse.ArgumentParser(
        description='Advent of code 2025 day 12')

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

    shapes = []
    shape = []
    shape_line = -1
    spaces = []
    for item in data:
        if 'x' in item:
            size, nums = item.split(': ')
            space = {}
            space['size'] = [int(x) for x in size.split('x')]
            space['items'] = [int(x) for x in nums.split(' ')]
            spaces.append(space)
            continue
        if ':' in item:
            shape_line = 0
            shape = []
            continue
        if 3 > shape_line > -1:
            for idx, char in enumerate(item):
                if char == '#':
                    shape.append((shape_line, idx))
            shape_line += 1
            continue
        if not item and shape_line == 3:
            shapes.append(shape)
            shape_line = -1
            continue

    return spaces, shapes


def main():
    """
    main
    """

    filename = get_args()
    spaces, shapes = read_data(filename)

    # part 1
    areas = []
    for shape in shapes:
        areas.append(len(shape))

    cnt_ok = 0
    cnt_bad = 0
    cnt_unknown = 0
    for space in spaces:
        # will always fit (enough room even all tiles were full 3x3)
        if sum(space['items']) <= (space['size'][0] // 3) * (space['size'][1]//3):
            cnt_ok += 1
            continue
        # will never fit (parts of tiles together are bigger than space)
        sums = 0
        for idx, value in enumerate(space['items']):
            sums += value * areas[idx]
        if sums > (space['size'][0] * space['size'][1]):
            cnt_bad += 1
            continue
        # should be evaluated
        cnt_unknown += 1
    print(f'Data evaluation: ok = {cnt_ok}, bad = {cnt_bad}, unknown = {cnt_unknown}')
    print(f"Solution part 1: {cnt_ok}")


if __name__ == '__main__':
    main()

# EOF
