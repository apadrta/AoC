#!/usr/bin/env python
# -*- coding:utf-8 -*-
"""
Advent of code 2021 - Day 13
"""

import argparse
from copy import deepcopy
from PIL import Image
import numpy as np


def get_args():
    """
    Cmd line argument parsing (preprocessing)
    """
    # Assign description to the help doc
    parser = argparse.ArgumentParser(
        description='Advent of code 2021: Day 13')

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


def fold_y(points, axis):
    """
    Fold points along y-axis
    """
    newpoints = set()
    for point in points:
        if point[1] < axis:
            newpoints.add(point)
        else:
            newpoints.add((point[0], axis - (point[1] - axis)))
    return newpoints


def fold_x(points, axis):
    """
    Fold points along x-axis
    """
    newpoints = set()
    for point in points:
        if point[0] < axis:
            newpoints.add(point)
        else:
            newpoints.add((axis - (point[0] - axis), point[1]))
    return newpoints


def points2image(points, filename):
    """
    Write points to picture
    """
    maxy = 0
    maxx = 0
    for point in points:
        if point[0] > maxx:
            maxx = point[0]
        if point[1] > maxy:
            maxy = point[0]
    arr = np.zeros((maxy + 1, maxx + 1), dtype='uint8')
    for point in points:
        arr[(point[1], point[0])] = 1
    img = Image.fromarray(arr.astype('uint8')*255)
    img.save(filename)


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

    points = set()
    folds = []
    for line in lines:
        if line and line[0].isdigit():
            points.add(tuple([int(x) for x in line.split(",")]))
        elif line and line[0] == 'f':
            [text, number] = line.split("=")
            folds.append((text[-1], int(number)))

    # part 1
    mypoints = deepcopy(points)
    if folds[0][0] == 'y':
        res = fold_y(mypoints, folds[0][1])
    else:
        res = fold_x(mypoints, folds[0][1])
    print(f"Part 1 solution: {len(res)}")

    # part 2
    mypoints = deepcopy(points)
    for fold in folds:
        if fold[0] == 'y':
            mypoints = fold_y(mypoints, fold[1])
        else:
            mypoints = fold_x(mypoints, fold[1])

    points2image(mypoints, "solution2.png")
    print("Part 2 solution: check piture 'solution2.png'")


if __name__ == '__main__':
    main()

# EOF
