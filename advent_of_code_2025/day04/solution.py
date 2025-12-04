#!/usr/bin/env python
# -*- coding:utf-8 -*-
"""
Advent of Code solution
"""

import argparse
import numpy as np


def get_args():
    """
    Cmd line argument parsing (preprocessing)
    """
    # Assign description to the help doc
    parser = argparse.ArgumentParser(
        description='Advent of code 2025 day 4')

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

    width = len(data[0])+2
    height = len(data)+2
    papers = []
    arr = np.zeros((height, width), int)
    for idx, line in enumerate(data):
        for jdx, char in enumerate(line):
            val = 0
            if char == '@':
                val = 1
            arr[(idx + 1, jdx + 1)] = val
            if val == 1:
                papers.append((idx + 1, jdx + 1))
    return arr, papers


SURR = [
    (-1, -1),
    (-1, 0),
    (-1, 1),
    (0, -1),
    (0, 1),
    (1, -1),
    (1, 0),
    (1, 1),
]


def get_accesible(arr, papers):
    """
    get list of positions for accesible papers
    """

    accessible = []
    for item in papers:
        neighbours = 0
        for direction in SURR:
            neighbours += arr[tuple(np.array(item) + np.array(direction))]
        if neighbours < 4:
            accessible.append(item)
    return accessible


def main():
    """
    main
    """

    filename = get_args()
    arr, papers = read_data(filename)

    # part 1
    rolls = get_accesible(arr, papers)
    print(f"Solution part 1: {len(rolls)}")

    # part 2
    removed = len(rolls)
    while len(rolls) > 0:
        # remove rolls from array and the list
        for item in rolls:
            arr[item] = 0
            papers.remove(item)

        # find removable
        rolls = get_accesible(arr, papers)
        removed += len(rolls)
        print('.', end='', flush=True)

    print(f"\nSolution part 2: {removed}")


if __name__ == '__main__':
    main()

# EOF
