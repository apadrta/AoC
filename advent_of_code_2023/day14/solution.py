#!/usr/bin/env python
# -*- coding:utf-8 -*-
"""
Advent of code 2023 - Day 14
"""

import argparse
from copy import deepcopy
import numpy as np


def get_args():
    """
    Cmd line argument parsing (preprocessing)
    """
    # Assign description to the help doc
    parser = argparse.ArgumentParser(
        description='Advent of code 2023: Day 14'
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

    width = len(data[0])
    height = len(data)
    arr = np.zeros((height, width), int)
    for idx, line in enumerate(data):
        for jdx, char in enumerate(line):
            if char == '#':
                arr[(idx, jdx)] = 2
            if char == 'O':
                arr[(idx, jdx)] = 1
    return arr


def tilt_north(data):
    """
    tilt data north
    """
    width = len(data[0])
    height = len(data)
    idx = 0
    load = 0
    while idx < width:
        stop = -1
        pos = 0
        while pos < height:
            if data[(pos, idx)] == 2:
                stop = pos
            elif data[(pos, idx)] == 1:
                stop += 1
                data[(pos, idx)] = 0
                data[(stop, idx)] = 1
                load += height - stop
            pos += 1
        idx += 1
    return data, load


def tilt_west(data):
    """
    tilt data west
    """
    width = len(data[0])
    height = len(data)
    pos = 0
    load = 0
    while pos < height:
        stop = -1
        idx = 0
        while idx < width:
            if data[(pos, idx)] == 2:
                stop = idx
            elif data[(pos, idx)] == 1:
                stop += 1
                data[(pos, idx)] = 0
                data[(pos, stop)] = 1
                load += height - pos
            idx += 1
        pos += 1
    return data, load


def tilt_south(data):
    """
    tilt data south
    """
    width = len(data[0])
    height = len(data)
    idx = 0
    load = 0
    while idx < width:
        stop = width
        pos = width - 1
        while pos >= 0:
            if data[(pos, idx)] == 2:
                stop = pos
            elif data[(pos, idx)] == 1:
                stop -= 1
                data[(pos, idx)] = 0
                data[(stop, idx)] = 1
                load += height - stop
            pos -= 1
        idx += 1
    return data, load


def tilt_east(data):
    """
    tilt data east
    """
    width = len(data[0])
    height = len(data)
    pos = 0
    load = 0
    while pos < height:
        stop = width
        idx = width - 1
        while idx >= 0:
            if data[(pos, idx)] == 2:
                stop = idx
            elif data[(pos, idx)] == 1:
                stop -= 1
                data[(pos, idx)] = 0
                data[(pos, stop)] = 1
                load += height - pos
            idx -= 1
        pos += 1
    return data, load


def tilts(data, nums):
    """
    tilt data north+west+south+east nums times
    """
    num = 0
    sums = 0
    states = [deepcopy(data)]
    loads = [0]
    while num < nums:
        print('.', end='', flush=True)
        data, sums = tilt_north(data)
        data, sums = tilt_west(data)
        data, sums = tilt_south(data)
        data, sums = tilt_east(data)
        loads.append(sums)
        frompos = -1
        for idx, item in enumerate(states):
            if np.array_equal(item, data):
                frompos = idx
                break
        if frompos == -1:
            states.append(deepcopy(data))
        else:
            print(f'\ncycle detected {frompos} - {num}')
            break
        num += 1
    num += 1
    sums = loads[(nums - frompos) % (num - frompos) + frompos]

    return sums


def main():
    """
    Main function
    """

    # process args
    infile = get_args()

    # read data
    data = read_data_struct(infile)

    # part 1
    data, sums = tilt_north(data)
    print(f"Part 1 solution: {sums}")

    # part 2
    sums = tilts(data, 1000000000)
    print(f"Part 2 solution: {sums}")


if __name__ == '__main__':
    main()

# EOF
