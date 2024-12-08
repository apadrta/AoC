#!/usr/bin/env python
# -*- coding:utf-8 -*-
"""
Advent of code 2024 - Day 8
"""

import argparse


def get_args():
    """
    Cmd line argument parsing (preprocessing)
    """
    # Assign description to the help doc
    parser = argparse.ArgumentParser(
        description='Advent of code 2024: Day 8')

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
    # create basic rules and list of updates
    antenas = {}
    for idx, row in enumerate(data):
        for jdx, col in enumerate(row):
            if col == ".":
                continue
            if col not in antenas:
                antenas[col] = []
            antenas[col].append([idx, jdx])
    return {"size": [len(data), len(data[0])], 'antenas': antenas}


def get_pairs(data):
    """
    get all possible pairs from data (unordered)
    """
    pairs = []
    idx = 0
    while idx < len(data):
        jdx = idx + 1
        while jdx < len(data):
            pairs.append([data[idx], data[jdx]])
            jdx += 1
        idx += 1
    return pairs


def get_antinodes(data):
    """
    Get antinodes list
    """
    antinodes = []
    for antdata in data["antenas"].values():
        pairs = get_pairs(antdata)
        for pair in pairs:
            diff = [pair[0][0] - pair[1][0], pair[0][1] - pair[1][1]]
            for run in [0, 1]:
                if run == 0:
                    antinode = [pair[0][0] + diff[0], pair[0][1] + diff[1]]
                else:
                    antinode = [pair[1][0] - diff[0], pair[1][1] - diff[1]]
                if antinode[0] < 0 or antinode[0] >= data["size"][0]:
                    continue
                if antinode[1] < 0 or antinode[1] >= data["size"][1]:
                    continue
                if antinode in antinodes:
                    continue
                antinodes.append(antinode)
    return antinodes


def get_antinodes_rep(data):
    """
    Get antinodes list (repeat)
    """
    antinodes = []
    for antdata in data["antenas"].values():
        for antenna in antdata:
            if antenna in antinodes:
                continue
            antinodes.append(antenna)
        pairs = get_pairs(antdata)
        for pair in pairs:
            diff = [pair[0][0] - pair[1][0], pair[0][1] - pair[1][1]]
            for run in [0, 1]:
                last = []
                while True:
                    if run == 0:
                        if not last:
                            antinode = [pair[0][0] + diff[0], pair[0][1] + diff[1]]
                        else:
                            antinode = [last[0] + diff[0], last[1] + diff[1]]
                    else:
                        if not last:
                            antinode = [pair[1][0] - diff[0], pair[1][1] - diff[1]]
                        else:
                            antinode = [last[0] - diff[0], last[1] - diff[1]]
                    last = antinode
                    if antinode[0] < 0 or antinode[0] >= data["size"][0]:
                        break
                    if antinode[1] < 0 or antinode[1] >= data["size"][1]:
                        break
                    if antinode in antinodes:
                        continue
                    antinodes.append(antinode)
    return antinodes


def main():
    """
    Main function
    """

    # process args
    infile = get_args()

    # read data
    data = read_data(infile)

    # part 1
    antinodes = get_antinodes(data)
    sums = len(antinodes)
    print(f"Part 1 solution: {sums}")

    # part 2
    antinodes = get_antinodes_rep(data)
    sums = len(antinodes)
    print(f"Part 2 solution: {sums}")


if __name__ == '__main__':
    main()

# EOF
