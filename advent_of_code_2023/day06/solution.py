#!/usr/bin/env python
# -*- coding:utf-8 -*-
"""
Advent of code 2023 - Day 6
"""

import argparse


def get_args():
    """
    Cmd line argument parsing (preprocessing)
    """
    # Assign description to the help doc
    parser = argparse.ArgumentParser(
        description='Advent of code 2023: Day 6'
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

    lines = [x.split(':')[1] for x in data]
    times = " ".join(lines[0].split())
    times = [int(x) for x in times.split(' ')]
    dists = " ".join(lines[1].split())
    dists = [int(x) for x in dists.split(' ')]

    return times, dists


def eval_race(time, dist):
    """
    Evaluate race for part1
    """
    speed = 0
    while speed < time:
        res = speed * (time - speed)
        if res > dist:
            return time - 2 * (speed) + 1
        speed += 1
    return 0


def main():
    """
    Main function
    """

    # process args
    infile = get_args()

    # read data
    times, dists = read_data_struct(infile)

    # part 1
    muls = 1
    for idx, time in enumerate(times):
        muls *= eval_race(time, dists[idx])
    print(f"Part 1 solution: {muls}")

    # part 2
    times = int("".join([str(x) for x in times]))
    dists = int("".join([str(x) for x in dists]))
    muls = eval_race(times, dists)
    print(f"Part 2 solution: {muls}")


if __name__ == '__main__':
    main()

# EOF
