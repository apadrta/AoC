#!/usr/bin/env python
# -*- coding:utf-8 -*-
"""
Advent of code 2024 - Day 18
"""

import argparse
import numpy as np

vector = {
    0: [-1, 0],
    1: [0, 1],
    2: [1, 0],
    3: [0, -1]
}


def get_args():
    """
    Cmd line argument parsing (preprocessing)
    """
    # Assign description to the help doc
    parser = argparse.ArgumentParser(
        description='Advent of code 2024: Day 16')

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


def read_data(filename):
    """
    Read and prepare data
    """
    # read file
    data = []
    with open(filename, "r") as fileh:
        data = fileh.readlines()
    data = [x.replace('\r', '').replace('\n', '') for x in data]
    mems = []
    for item in data:
        mems.append([int(x) for x in item.split(',')])
    return mems


def shortest_path(memdata, numbytes):
    """
    Find shortest path from top left to bottom right
    """
    size = [0, 0]
    for item in memdata:
        if item[0] > size[0]:
            size[0] = item[0]
        if item[1] > size[1]:
            size[1] = item[1]

    # initialize
    memory = np.full((size[1] + 1, size[0] + 1), -1, dtype=int,)
    for item in memdata[0:numbytes]:
        memory[item[1], item[0]] = -2
    memory[0][0] = 0

    # count distance
    toprocess = [[0, 0]]
    while toprocess:
        act = toprocess.pop(0)
        for vect in vector.values():
            new = [act[0] + vect[0], act[1] + vect[1]]
            if new[0] < 0 or new[0] > size[0]:
                continue
            if new[1] < 0 or new[1] > size[1]:
                continue
            if memory[new[0], new[1]] == -1 or memory[new[0], new[1]] > memory[act[0], act[1]] + 1:
                memory[new[0], new[1]] = memory[act[0], act[1]] + 1
                toprocess.append(new)
    return memory[size[1]][size[0]]


def main():
    """
    Main function
    """

    # process args
    infile = get_args()

    # read data
    memdata = read_data(infile)
    first = 1024

    # part 1
    sums = shortest_path(memdata, first)
    print(f"Part 1 solution: {sums}")
    # part 2
    idx = 0
    while True:
        if idx % 100 == 0:
            print('.', end='', flush=True)
        sums = shortest_path(memdata, first + idx + 1)
        if sums < 0:
            break
        idx += 1
    print(f"\nPart 2 solution: {','.join([str(x) for x in memdata[first+idx]])}")


if __name__ == '__main__':
    main()

# EOF
