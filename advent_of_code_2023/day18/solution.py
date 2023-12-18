#!/usr/bin/env python
# -*- coding:utf-8 -*-
"""
Advent of code 2023 - Day 18
"""

import argparse
import numpy as np
from skimage.morphology import flood_fill


def get_args():
    """
    Cmd line argument parsing (preprocessing)
    """
    # Assign description to the help doc
    parser = argparse.ArgumentParser(
        description='Advent of code 2023: Day 18'
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

    instructions = []
    conv = {'0': 'R', '1': 'D', '2': 'L', '3': 'U'}
    for line in data:
        direction, length, color = line.split(' ')
        instructions.append([direction, int(length), int(color[2:-2], 16), conv[color[-2]]])

    return instructions


def shoelace(xvals, yvals):
    """
    Sholelace method
    """
    area = 0
    idx = 0
    while idx < len(xvals):
        area += xvals[idx] * yvals[(idx + 1) % len(xvals)] - yvals[idx] * xvals[(idx + 1) % len(xvals)]
        idx += 1
    return abs(area) / 2


def dig_pool_shoelace(insts, dirpos=0, lenpos=1):
    """
    Find farthest distance
    """
    # get vertices and number of points
    pos = [0, 0]
    yvals = [0]
    xvals = [0]
    pts = 0
    for inst in insts[:-1]:
        if inst[dirpos] == 'R':
            pos[1] += inst[lenpos]
        elif inst[dirpos] == 'L':
            pos[1] -= inst[lenpos]
        elif inst[dirpos] == 'D':
            pos[0] -= inst[lenpos]
        elif inst[dirpos] == 'U':
            pos[0] += inst[lenpos]
        xvals.append(pos[1])
        yvals.append(pos[0])
        pts += inst[lenpos]
    pts += insts[-1][lenpos]
    # count area
    return int(shoelace(xvals, yvals)) + 1 + pts // 2


def dig_pool(insts):
    """
    Find farthest distance
    """
    pos = [0, 0]
    points = []
    upleft = [0, 0]
    downright = [0, 0]
    for inst in insts:
        # movepos
        if inst[0] == 'R':
            for _ in range(0, inst[1]):
                pos[1] += 1
                points.append(tuple(pos))
        elif inst[0] == 'L':
            for _ in range(0, inst[1]):
                pos[1] -= 1
                points.append(tuple(pos))
        elif inst[0] == 'D':
            for _ in range(0, inst[1]):
                pos[0] += 1
                points.append(tuple(pos))
        elif inst[0] == 'U':
            for _ in range(0, inst[1]):
                pos[0] -= 1
                points.append(tuple(pos))
        # count limits
        if pos[0] < upleft[0]:
            upleft[0] = pos[0]
        if pos[0] > downright[0]:
            downright[0] = pos[0]
        if pos[1] < upleft[1]:
            upleft[1] = pos[1]
        if pos[1] > downright[1]:
            downright[1] = pos[1]
    # prepare array
    width = downright[1] - upleft[1]
    height = downright[0] - upleft[0]
    arr = np.full((height + 3, width + 3), -1, dtype=int)
    # place points
    for point in points:
        arr[(point[0] - upleft[0] + 1, point[1] - upleft[1] + 1)] = 0
    # count and return digged m3
    arr = flood_fill(arr, (0, 0), -9)

    return np.count_nonzero(arr == 0) + np.count_nonzero(arr == -1)


def main():
    """
    Main function
    """

    # process args
    infile = get_args()

    # read data
    data = read_data_struct(infile)

    # part 1
    count = dig_pool(data)
    print(f"Part 1 solution (naive): {count}")
    count = dig_pool_shoelace(data, 0, 1)
    print(f"Part 1 solution (shoelace): {count}")

    # part 2
    count = dig_pool_shoelace(data, 3, 2)
    print(f"Part 2 solution (shoelace): {count}")


if __name__ == '__main__':
    main()

# EOF
