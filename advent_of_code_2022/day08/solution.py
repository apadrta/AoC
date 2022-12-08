#!/usr/bin/env python
# -*- coding:utf-8 -*-
"""
Advent of code 2022 - Day 8
"""

import argparse
import numpy as np


def get_args():
    """
    Cmd line argument parsing (preprocessing)
    """
    # Assign description to the help doc
    parser = argparse.ArgumentParser(
        description='Advent of code 2022: Day 8')

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


def lines2array(lines):
    """
    Convert lines to array
    """
    xsize = len(lines[0])
    ysize = len(lines)

    arr = np.zeros((xsize, ysize), dtype=np.int8)
    for idx, line in enumerate(lines):
        items = [int(x) for x in line]
        arr[:, idx] = np.array(items)
    return np.transpose(arr)


def detect_visible(trees, visarr):
    """
    Detect visible trees from top side
    """
    # visibility from top
    ridx = 0
    while ridx < trees.shape[1]:
        cidx = 0
        last = -1
        while cidx < trees.shape[0]:
            if trees[(cidx, ridx)] > last:
                last = trees[(cidx, ridx)]
                visarr[(cidx, ridx)] = 1
            cidx += 1
        ridx += 1
    return visarr


def scentic_score(trees, score):
    """
    Compute scentic score down from point
    """
    ridx = 0
    while ridx < trees.shape[1]:
        cidx = 0
        while cidx < trees.shape[0]:
            pos = cidx + 1
            while pos < trees.shape[0]:
                pos += 1
                if trees[(cidx, ridx)] <= trees[(pos-1, ridx)]:
                    break
            score[(cidx, ridx)] *= pos - cidx - 1
            cidx += 1
        ridx += 1

    return score


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
    trees = lines2array(lines)

    # detect visibility
    visarr = np.zeros(trees.shape, dtype=np.int8)
    for _ in range(0, 4):
        visarr = detect_visible(trees, visarr)
        visarr = np.rot90(visarr)
        trees = np.rot90(trees)

    # count visible trees
    res = visarr.sum()
    print(f"Part 1 solution: {res}")

    # count scentic scores
    score = np.ones(trees.shape, dtype=np.int32)
    for _ in range(0, 4):
        score = scentic_score(trees, score)
        score = np.rot90(score)
        trees = np.rot90(trees)
    # detect maximal value
    res = score.max()
    print(f"Part 2 solution: {res}")


if __name__ == '__main__':
    main()

# EOF
