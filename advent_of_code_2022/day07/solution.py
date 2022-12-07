#!/usr/bin/env python
# -*- coding:utf-8 -*-
"""
Advent of code 2022 - Day 7
"""

import argparse


def get_args():
    """
    Cmd line argument parsing (preprocessing)
    """
    # Assign description to the help doc
    parser = argparse.ArgumentParser(
        description='Advent of code 2022: Day 7')

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


def parse_data(data):
    """
    Prepare data structure for further processing
    """
    struct = {}
    path = []
    for line in data:
        line = line.replace('\n', '').replace('\r', '')
        if line[:4] == '$ cd':
            dirname = line.split(' ')[-1]
            if dirname == '..':
                path = path[:-1]
            else:
                path += [dirname]
        elif line[0] != '$':
            size = line.split(' ')[0]
            if size[0:3] != 'dir':
                target_path = ''
                for item in path:
                    target_path += f'{item};'
                    if target_path not in struct:
                        struct[target_path] = 0
                    struct[target_path] += int(size)
    return struct


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

    # evaluate part 1
    dirs = parse_data(data)
    res = 0
    for value in dirs.values():
        if value <= 100000:
            res += value
    print("Part 1 solution: {}".format(res))

    # evaluate part 2
    needed_space = 30000000 - 70000000 + dirs['/;']
    minidx = 0
    values = list(dirs.values())
    for idx, value in enumerate(values):
        if value < needed_space:
            continue
        if values[idx] - needed_space < values[minidx] - needed_space:
            minidx = idx
    res = values[minidx]
    print("Part 2 solution: {}".format(res))


if __name__ == '__main__':
    main()

# EOF
