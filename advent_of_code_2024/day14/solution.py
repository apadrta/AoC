#!/usr/bin/env python
# -*- coding:utf-8 -*-
"""
Advent of code 2024 - Day 14
"""

import argparse


def get_args():
    """
    Cmd line argument parsing (preprocessing)
    """
    # Assign description to the help doc
    parser = argparse.ArgumentParser(
        description='Advent of code 2024: Day 14'
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
    robots = []
    size = [0, 0]
    for item in data:
        pos, vel = item.split(' ')
        pos = [int(x) for x in pos[2:].split(',')]
        vel = [int(x) for x in vel[2:].split(',')]
        robots.append({"p": pos, "v": vel})
        if pos[0] > size[0]:
            size[0] = pos[0]
        if pos[1] > size[1]:
            size[1] = pos[1]
    size = [size[0] + 1, size[1] + 1]
    return robots, size


def eval_robots(data, size, seconds):
    """
    Evaluate robots positions
    """
    robots = []
    for item in data:
        robot = [0, 0]
        for idx in [0, 1]:
            robot[idx] = (item['p'][idx] + seconds * item['v'][idx]) % size[idx]
        robots.append(robot)
    return robots


def eval_quadrant(data, size):
    """
    Evaluate safety factor
    """
    quadrants = [0, 0, 0, 0]
    for item in data:
        if item[0] < size[0]//2 and item[1] < size[1]//2:
            quadrants[0] += 1
        if item[0] < size[0]//2 and item[1] > size[1]//2:
            quadrants[1] += 1
        if item[0] > size[0]//2 and item[1] < size[1]//2:
            quadrants[2] += 1
        if item[0] > size[0]//2 and item[1] > size[1]//2:
            quadrants[3] += 1
    mul = 1
    for item in quadrants:
        mul = mul * item
    return mul


def is_overlapping(data):
    """
    Check if some robots are overlapping
    """
    idx = 0
    while idx < len(data):
        jdx = idx + 1
        while jdx < len(data):
            if data[idx] == data[jdx]:
                return True
            jdx += 1
        idx += 1
    return False


def main():
    """
    Main function
    """

    # process args
    infile = get_args()

    # read data
    data, size = read_data_struct(infile)

    # part 1
    data100 = eval_robots(data, size, 100)
    sums = eval_quadrant(data100, size)
    print(f"Part 1 solution: {sums}")

    # part 2
    idx = 1
    while True:
        if idx % 100 == 0:
            print(".", end='', flush=True)
        robodata = eval_robots(data, size, idx)
        res = is_overlapping(robodata)
#        print(idx, res)
        if not res:
            break
        idx += 1
    print(f"\nPart 2 solution: {idx}")


if __name__ == '__main__':
    main()

# EOF
