#!/usr/bin/env python
# -*- coding:utf-8 -*-
"""
Advent of code 2024 - Day 20
"""

import argparse
import numpy as np

vector = {
    0: [-1, 0],
    1: [0, 1],
    2: [1, 0],
    3: [0, -1]
}


def get_args():
    """
    Cmd line argument parsing (preprocessing)
    """
    # Assign description to the help doc
    parser = argparse.ArgumentParser(
        description='Advent of code 2024: Day 20'
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


def read_data(filename):
    """
    Read and prepare data
    """
    # read file
    data = []
    with open(filename, "r") as fileh:
        data = fileh.readlines()
    data = [x.replace('\r', '').replace('\n', '') for x in data]
    array = np.array([[ord(char) for char in line] for line in data])
    return array


def get_pois(mapdata):
    """
    Extract points of interest
    """
    pois = {"start": (0, 0), "end": (0, 0), "path": {}}
    idx = 0
    while idx < mapdata.shape[0]:
        jdx = 0
        end = False
        while jdx < mapdata.shape[1]:
            if mapdata[idx][jdx] == 83:
                pois["start"] = (idx, jdx)
                end = True
                break
            jdx += 1
        if end:
            break
        idx += 1
    pos = [pois["start"][0], pois["start"][1]]
    val = 0
    pois["path"][tuple(pos)] = val
    while mapdata[pos[0]][pos[1]] != 69:
        for vect in vector.values():
            newpos = (pos[0] + vect[0], pos[1] + vect[1])
            if newpos in pois["path"]:
                continue
            if mapdata[newpos[0]][newpos[1]] != 35:
                val += 1
                pos[0] = newpos[0]
                pos[1] = newpos[1]
                pois["path"][newpos] = val
                break
    pois["end"] = tuple(pos)
    return pois


def find_shortcuts(path):
    """
    Read and prepare data
    """
    scuts = {}
    for idx, ivalue in path.items():
        for jdx, jvalue in path.items():
            if (idx[0] == jdx[0] and abs(idx[1] - jdx[1]) == 2) or (idx[1] == jdx[1] and abs(idx[0] - jdx[0]) == 2):
                short = jvalue - ivalue - 2
                if short <= 0:
                    continue
                if short not in scuts:
                    scuts[short] = 0
                scuts[short] += 1
    return scuts


def find_shortcuts20(path):
    """
    Read and prepare data
    """
    scuts = {}
    for idx, ivalue in path.items():
        for jdx, jvalue in path.items():
            cityblock = abs(idx[0] - jdx[0]) + abs(idx[1] - jdx[1])
            if cityblock <= 20:
                short = jvalue - ivalue - cityblock
                if short <= 0:
                    continue
                if short not in scuts:
                    scuts[short] = 0
                scuts[short] += 1
    return scuts


def main():
    """
    Main function
    """

    # process args
    infile = get_args()

    # read data
    data = read_data(infile)

    # part 1
    pois = get_pois(data)
    shortcuts = find_shortcuts(pois["path"])
    sums = 0
    for key, value in shortcuts.items():
        if key >= 100:
            sums += value
    print(f"Part 1 solution: {sums}")

    # part 2
    sums = 0
    shortcuts = find_shortcuts20(pois["path"])
    for key, value in shortcuts.items():
        if key >= 100:
            sums += value
    print(f"Part 2 solution: {sums}")


if __name__ == '__main__':
    main()

# EOF
