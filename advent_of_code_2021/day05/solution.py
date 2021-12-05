#!/usr/bin/env python
# -*- coding:utf-8 -*-
"""
Advent of code 2021 - Day 5
"""

import argparse


def get_args():
    """
    Cmd line argument parsing (preprocessing)
    """
    # Assign description to the help doc
    parser = argparse.ArgumentParser(
        description='Advent of code 2021: Day 4')

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


def get_steps(start, end):
    """
    Compute step orientation from start to end (deltax, deltay, number of steps)
    """
    difx = 0
    dify = 0
    steps = 0

    if start[0] != end[0]:
        difx = (end[0] - start[0]) // abs(end[0] - start[0])
        steps = abs(end[0] - start[0])
    if start[1] != end[1]:
        dify = (end[1] - start[1]) // abs(end[1] - start[1])
        steps = abs(end[1] - start[1])

    return [difx, dify, steps]


def get_danger(vents, diagonals=True):
    """
    Compute vent danger
    """
    danger = {}
    for vent in vents:
        [deltax, deltay, steps] = get_steps(vent[0], vent[1])
        if not diagonals and deltax != 0 and deltay != 0:
            # ignore diagonal
            continue
        posx = vent[0][0]
        posy = vent[0][1]
        step = 0
        while step <= steps:
            point = (posx, posy)
            if point in danger:
                danger[point] += 1
            else:
                danger[point] = 1
            posx += deltax
            posy += deltay
            step += 1
    return danger


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

    vents = []
    for item in data:
        points = item.replace('\n', '').replace('\r', '').split(" -> ")
        begin = tuple([int(x) for x in points[0].split(",")])
        end = tuple([int(x) for x in points[1].split(",")])
        vents.append([begin, end])

    # process data
    danger = get_danger(vents, False)
    print("Part 1 solution: {}".format(len(danger) - list(danger.values()).count(1)))

    danger = get_danger(vents, True)
    print("Part 2 solution: {}".format(len(danger) - list(danger.values()).count(1)))


if __name__ == '__main__':
    main()

# EOF
