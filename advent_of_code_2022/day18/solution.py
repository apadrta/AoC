#!/usr/bin/env python
# -*- coding:utf-8 -*-
"""
Advent of code 2022 - Day 18
"""

import argparse
import numpy as np


def get_args():
    """
    Cmd line argument parsing (preprocessing)
    """
    # Assign description to the help doc
    parser = argparse.ArgumentParser(
        description='Advent of code 2022: Day 18')

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


def parse_input(lines):
    """
    Preprocess input
    """
    data = []
    for line in lines:
        data.append([int(x) for x in line.split(',')])
    return data


def solve_part1(data):
    """
    count surface
    """
    sums = len(data) * 6
    idx = 1
    while idx < len(data):
        jdx = 0
        if idx % 100 == 0:
            print('.', end='', flush=True)
        while jdx < idx:
            dist = 0
            for kdx in range(0, 3):
                dist += abs(data[idx][kdx] - data[jdx][kdx])
            if dist == 1:
                sums -= 2
            jdx += 1
        idx += 1

    return sums


diffs = [
    [0, 0, 1],
    [0, 0, -1],
    [0, 1, 0],
    [0, -1, 0],
    [1, 0, 0],
    [-1, 0, 0],
]


def solve_part2(data):
    """
    count surface
    """
    # prepare 3D array
    ranges = [
        [data[0][0], data[0][0]],
        [data[0][1], data[0][1]],
        [data[0][2], data[0][2]]
    ]
    for point in data[1:]:
        for kdx in range(0, 3):
            if point[kdx] < ranges[kdx][0]:
                ranges[kdx][0] = point[kdx]
            if point[kdx] > ranges[kdx][1]:
                ranges[kdx][1] = point[kdx]
    droplet = np.zeros((ranges[0][1] - ranges[0][0] + 3, ranges[1][1] - ranges[1][0] + 3, ranges[2][1] - ranges[2][0] + 3), dtype=int)
    for point in data:
        droplet[(point[0] - ranges[0][0] + 1, point[1] - ranges[1][0] + 1, point[2] - ranges[2][0] + 1)] = 1

    # color all cubes reachable from (0,0,0)
    droplet[(0, 0, 0)] = 8
    process = [[0, 0, 0]]
    step = 0
    size = np.shape(droplet)
    while process:
        procpoint = process.pop(0)
        for diff in diffs:
            newpoint = (diff[0] + procpoint[0], diff[1] + procpoint[1], diff[2] + procpoint[2])
            isok = True
            for kdx in range(0, 3):
                if newpoint[kdx] < 0 or newpoint[kdx] > size[kdx] - 1:
                    isok = False
                    break
            if isok and droplet[newpoint] == 0:
                droplet[newpoint] = 8
                process.append(newpoint)
        step += 1
        if step % 1000 == 0:
            print('.', end='', flush=True)
    # count values
    sums = 0
    other = 0
    pocket = 0
    for procpoint in data:
        for diff in diffs:
            newpoint = (diff[0] + procpoint[0] - ranges[0][0] + 1, diff[1] + procpoint[1] - ranges[1][0] + 1, diff[2] + procpoint[2] - ranges[2][0] + 1)
            if droplet[newpoint] == 8:
                sums += 1
            if droplet[newpoint] == 1:
                other += 1
            if droplet[newpoint] == 0:
                pocket += 1
    return sums


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

    # preprocess data
    data = parse_input(lines)

    # part 1
    res = solve_part1(data)
    print(f"\nPart 1 solution: {res}")

    # part 2
    res = solve_part2(data)
    print(f"\nPart 2 solution: {res}")


if __name__ == '__main__':
    main()

# EOF
