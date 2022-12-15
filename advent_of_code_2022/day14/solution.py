#!/usr/bin/env python
# -*- coding:utf-8 -*-
"""
Advent of code 2022 - Day 14
"""

import argparse
import numpy as np


def get_args():
    """
    Cmd line argument parsing (preprocessing)
    """
    # Assign description to the help doc
    parser = argparse.ArgumentParser(
        description='Advent of code 2022: Day 14')

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


def create_blocks(lines):
    """
    compare two packets
    """
    blocks = []
    xmin = None
    xmax = None
    ymax = None
    ymin = None
    for line in lines:
        points = line.split(' -> ')
        last = None
        for point in points:
            x, y = [int(var) for var in point.split(',')]
            if last:
                blocks.append((last, (x, y)))
            last = (x, y)

            if not xmin:
                xmin = x
            else:
                if x < xmin:
                    xmin = x
            if not ymin:
                ymin = y
            else:
                if y < ymin:
                    ymin = y
            if not xmax:
                xmax = x
            else:
                if x > xmax:
                    xmax = x
            if not ymax:
                ymax = y
            else:
                if y > ymax:
                    ymax = y
    return blocks, (xmin, xmax), (ymin, ymax)


def simulate_sand(blocks, xdef, ydef):
    """
    simulate sand
    """
    # initialize grid
    xsize = xdef[1] + 2
    ysize = ydef[1] + 2
    arr = np.zeros((ysize, xsize), dtype=int)
    arr[0, 500] = 9
    # add blocks
    for block in blocks:
        yblock = abs(block[1][1] - block[0][1])
        xblock = abs(block[1][0] - block[0][0])
        npblock = np.ones((yblock + 1, xblock + 1), dtype=int)
        x_pos = min(block[0][0], block[1][0])
        y_pos = min(block[0][1], block[1][1])
        arr[y_pos:y_pos+yblock+1, x_pos:x_pos+xblock+1] = npblock
    # simulate sand
    sandn = 0
    while True:
        pos = [0, 500]
        while True:
            if arr[(pos[0] + 1, pos[1])] == 0:
                pos[0] += 1
            elif arr[(pos[0] + 1, pos[1] - 1)] == 0:
                pos[0] += 1
                pos[1] -= 1
            elif arr[(pos[0] + 1, pos[1] + 1)] == 0:
                pos[0] += 1
                pos[1] += 1
            else:
                arr[(pos[0], pos[1])] = 2
                break
            if pos[0] == ysize-1:
                return sandn
        sandn += 1


def simulate_sand2(blocks, xdef, ydef):
    """
    simulate sand with floor
    """
    # initialize grid
    xsize = xdef[1] + 2 * ydef[1]
    ysize = ydef[1] + 3
    arr = np.zeros((ysize, xsize), dtype=int)
    arr[0, 500] = 9
    # add floor
    arr[ysize-1, :] = np.ones((1, xsize), dtype=int)
    # add blocks
    for block in blocks:
        yblock = abs(block[1][1] - block[0][1])
        xblock = abs(block[1][0] - block[0][0])
        npblock = np.ones((yblock + 1, xblock + 1), dtype=int)
        x_pos = min(block[0][0], block[1][0])
        y_pos = min(block[0][1], block[1][1])
        arr[y_pos:y_pos+yblock+1, x_pos:x_pos+xblock+1] = npblock
    # simulate sand
    sandn = 0
    while True:
        pos = [0, 500]
        while True:
            if arr[(pos[0] + 1, pos[1])] == 0:
                pos[0] += 1
            elif arr[(pos[0] + 1, pos[1] - 1)] == 0:
                pos[0] += 1
                pos[1] -= 1
            elif arr[(pos[0] + 1, pos[1] + 1)] == 0:
                pos[0] += 1
                pos[1] += 1
            else:
                arr[(pos[0], pos[1])] = 2
                if arr[(0, 500)] == 2:
                    return sandn + 1
                break
        sandn += 1


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
    blocks, xsize, ysize = create_blocks(lines)
    res = simulate_sand(blocks, xsize, ysize)
    print(f"Part 1 solution: {res}")

    # part 2
    res = simulate_sand2(blocks, xsize, ysize)
    print(f"Part 2 solution: {res}")


if __name__ == '__main__':
    main()

# EOF
