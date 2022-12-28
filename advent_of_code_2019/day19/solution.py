#!/usr/bin/env python
# -*- coding:utf-8 -*-
"""
Advent of code 2019 Day 19
"""


import argparse
import numpy as np
from elfcpu import ElfCPU


def get_args():
    """
    Cmd line argument parsing (preprocessing)
    """
    # Assign description to the help doc
    parser = argparse.ArgumentParser(
        description='Advent of code 2019 Day 19')

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


class ElfDroid():
    """
    Elf Droid for exploring tractor beam
    """

    def __init__(self):
        """
        Constructor
        """
        self.cpu = None

    def init_cpu(self, filename):
        """
        Initialize droid CPU
        """
        self.cpu = ElfCPU()
        self.cpu.read_code(filename)
        self.cpu.run()

    def explore(self, orders):
        """
        Manually explore floor
        """
        for order in orders:
            self.cpu.add_inputs(order)
            self.cpu.run()
            reply = self.cpu.get_output()
        return reply


def solution_part1(infile, size):
    """
    solution of part1
    """
    # initialize
    droid = ElfDroid()
    droid.init_cpu(infile)
    height = size
    width = size
    arr = np.zeros((height, width), dtype=int)
    # acquire raw data
    for idx in range(0, height):
        linefound = False
        for jdx in range(0, width):
            droid.init_cpu(infile)
            res = droid.explore([[jdx, idx]])
            arr[idx, jdx] = res[0]
            # optimalization for end line
            if res[0] == 1:
                linefound = True
            elif res[0] == 0 and linefound:
                break
        # optimalization for free rows
        if idx > 10 and not linefound:
            break
    return np.sum(arr), arr


def add_borders(arr, start, end, droidfile):
    """
    follow borders
    """
    # get init state
    y_pos = start
    x_left = 0
    x_right = 0
    beam = False
    jdx = 0
    while True:
        if arr[y_pos, jdx] == 1 and not beam:
            beam = True
            x_left = jdx
        elif arr[y_pos, jdx] == 0 and beam:
            beam = False
            x_right = jdx - 1
            break
        jdx += 1
    # initialize droid
    droid = ElfDroid()
    droid.init_cpu(droidfile)
    # follow beam contours
    pos = [[y_pos, x_left, x_right]]
    while y_pos < end:
        # move to next line
        y_pos += 1
        # move left x
        res = 0
        while res == 0:
            droid.init_cpu(droidfile)
            res = droid.explore([[x_left, y_pos]])[0]
            if res == 0:
                x_left += 1
        # move right x
        res = 1
        while res == 1:
            droid.init_cpu(droidfile)
            res = droid.explore([[x_right, y_pos]])[0]
            if res == 1:
                x_right += 1
            else:
                x_right -= 1
        # add to array
        pos.append([y_pos, x_left, x_right])
    # return list
    return pos


def find_square(pos, size):
    """
    find square in beams
    """
    for idx, item in enumerate(pos):
        if (item[2] - item[1] + 1) < size:
            continue
        if (idx + size) > len(pos):
            break
        if item[2] - pos[idx+size-1][1] + 1 == size:
            return item[0] + 10000 * pos[idx+size-1][1]
    return None


def main():
    """
    Main function
    """

    # process args
    infile = get_args()

    # part one
    res, arr = solution_part1(infile, 50)
    print(f"Solution of part 1: {res}")

    # part two
    pos = add_borders(arr, 20, 2000, infile)

    res = find_square(pos, 100)
    print(f"Solution of part 2: {res}")


if __name__ == '__main__':
    main()

# EOF
