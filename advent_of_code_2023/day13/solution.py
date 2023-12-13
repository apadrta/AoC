#!/usr/bin/env python
# -*- coding:utf-8 -*-
"""
Advent of code 2023 - Day 13
"""

import argparse


def get_args():
    """
    Cmd line argument parsing (preprocessing)
    """
    # Assign description to the help doc
    parser = argparse.ArgumentParser(
        description='Advent of code 2023: Day 13'
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

    # split to mirrors
    mirrors = []
    mirror = []
    for line in data:
        if not line:
            mirrors.append(mirror)
            mirror = []
            continue
        mirror.append(line)
    mirrors.append(mirror)

    # rotate mirrors
    r_mirrors = []
    for mirror in mirrors:
        r_mirror = [''] * len(mirror[0])
        for idx, _ in enumerate(mirror[0]):
            for line in mirror:
                r_mirror[idx] += line[idx]
        r_mirrors.append(r_mirror)

    return mirrors, r_mirrors


def find_flip(data):
    """
    find flip in data
    """
    # find two similar consecutive rows
    sims = []
    for idx, value in enumerate(data):
        if idx < len(data) - 1:
            if value == data[idx + 1]:
                sims.append(idx)
    # check possible mirroring
    for sim in sims:
        idx = sim - 1
        jdx = sim + 2
        isok = True
        while idx >= 0 and jdx < len(data):
            if data[idx] != data[jdx]:
                isok = False
                break
            idx -= 1
            jdx += 1
        if isok:
            return sim + 1
    return 0


def get_diff(one, two):
    """
    compute difference of two strings of the same length
    """
    diff = 0
    for idx, value in enumerate(one):
        if value != two[idx]:
            diff += 1
    return diff


def find_flip_fix(data):
    """
    find flip in data and fix exactly one error
    """
    sim = 0
    while sim < len(data):
        idx = sim
        jdx = sim + 1
        diff = 0
        while idx >= 0 and jdx < len(data):
            diff += get_diff(data[idx], data[jdx])
            idx -= 1
            jdx += 1
        if diff == 1:
            return sim + 1
        sim += 1
    return 0


def main():
    """
    Main function
    """

    # process args
    infile = get_args()

    # read data
    mirrors, r_mirrors = read_data_struct(infile)

    # part 1
    sums = 0
    for idx, mirror in enumerate(mirrors):
        sums += find_flip(mirror) * 100 + find_flip(r_mirrors[idx])
    print(f"Part 1 solution: {sums}")

    # part 2
    sums = 0
    for idx, mirror in enumerate(mirrors):
        sums += find_flip_fix(mirror) * 100 + find_flip_fix(r_mirrors[idx])
    print(f"Part 2 solution: {sums}")


if __name__ == '__main__':
    main()

# EOF
