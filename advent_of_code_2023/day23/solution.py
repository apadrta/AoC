#!/usr/bin/env python
# -*- coding:utf-8 -*-
"""
Advent of code 2023 - Day 23
"""

import argparse
from copy import deepcopy


def get_args():
    """
    Cmd line argument parsing (preprocessing)
    """
    # Assign description to the help doc
    parser = argparse.ArgumentParser(
        description='Advent of code 2023: Day 23'
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

    return data


def get_dists(data):
    """
    compute distances in maze (
    """
    height = len(data)
    width = len(data[0])

    # get points of interests (all crosroads)
    pois = [[0, 1], [height - 1, width - 2]]
    for idx in range(1, height - 1):
        for jdx in range(1, width - 1):
            if data[idx][jdx] != '.':
                continue
            entrances = [data[idx - 1][jdx], data[idx + 1][jdx], data[idx][jdx - 1], data[idx][jdx + 1]]
            if entrances.count('.') + entrances.count('v') + entrances.count('^') + entrances.count('<') + entrances.count('>') > 2:
                pois.append([idx, jdx])

    # prepare possible trails
    trails = []
    for poi in pois:
        if data[poi[0]][poi[1] + 1] in '.>':
            trails.append([[poi[0], poi[1] + 1], 'L', poi])
        if data[poi[0]][poi[1] - 1] in '.<':
            trails.append([[poi[0], poi[1] - 1], 'R', poi])
        if poi[0] > 0 and data[poi[0] - 1][poi[1]] in '.^':
            trails.append([[poi[0] - 1, poi[1]], 'D', poi])
        if poi[0] < height - 2 and data[poi[0] + 1][poi[1]] in '.v':
            trails.append([[poi[0] + 1, poi[1]], 'U', poi])

    # compute path between pois
    paths = {}
    for trail in trails:
        pos = deepcopy(trail[0])
        fromdir = trail[1]
        length = 1
        while True:
            if fromdir != 'D' and data[pos[0] + 1][pos[1]] in '.v':
                pos[0] += 1
                fromdir = 'U'
            elif fromdir != 'U' and data[pos[0] - 1][pos[1]] in '.^':
                pos[0] -= 1
                fromdir = 'D'
            elif fromdir != 'R' and data[pos[0]][pos[1] + 1] in '.>':
                pos[1] += 1
                fromdir = 'L'
            elif fromdir != 'L' and data[pos[0]][pos[1] - 1] in '.<':
                pos[1] -= 1
                fromdir = 'R'
            else:
                break  # bad slope
            length += 1
            if pos in pois:
                if tuple(trail[2]) not in paths:
                    paths[tuple(trail[2])] = {}
                paths[tuple(trail[2])][tuple(pos)] = length
                break

    # find longest path
    buff = [[(0, 1), 0, [(0, 1)]]]
    visited = {(0, 1): 0}
    maxtrail = 0
    while buff:
        work = buff.pop()
        if work[0] == (height - 1, width - 2):
            if work[1] > maxtrail:
                maxtrail = work[1]
            continue
        for target, dist in paths[work[0]].items():
            if target in work[2]:
                continue
            if target in visited and visited[target] > work[1] + dist:
                continue
            buff.append([target, work[1] + dist, work[2] + [target]])
            visited[target] = work[1] + dist

    return maxtrail


def get_dists_both_ways(data):
    """
    compute distances ingoring slopes
    """
    height = len(data)
    width = len(data[0])

    # get points of interests (all crosroads)
    pois = [[0, 1], [height - 1, width - 2]]
    for idx in range(1, height - 1):
        for jdx in range(1, width - 1):
            if data[idx][jdx] != '.':
                continue
            entrances = [data[idx - 1][jdx], data[idx + 1][jdx], data[idx][jdx - 1], data[idx][jdx + 1]]
            if entrances.count('.') + entrances.count('v') + entrances.count('^') + entrances.count('<') + entrances.count('>') > 2:
                pois.append([idx, jdx])

    # prepare possible trails
    trails = []
    for poi in pois:
        if data[poi[0]][poi[1] + 1] != '#':
            trails.append([[poi[0], poi[1] + 1], 'L', poi])
        if data[poi[0]][poi[1] - 1] != '#':
            trails.append([[poi[0], poi[1] - 1], 'R', poi])
        if poi[0] > 0 and data[poi[0] - 1][poi[1]] != '#':
            trails.append([[poi[0] - 1, poi[1]], 'D', poi])
        if poi[0] < height - 2 and data[poi[0] + 1][poi[1]] != '#':
            trails.append([[poi[0] + 1, poi[1]], 'U', poi])

    # compute path between pois
    paths = {}
    for trail in trails:
        pos = deepcopy(trail[0])
        fromdir = trail[1]
        length = 1
        while True:
            if fromdir != 'D' and data[pos[0] + 1][pos[1]] != '#':
                pos[0] += 1
                fromdir = 'U'
            elif fromdir != 'U' and data[pos[0] - 1][pos[1]] != '#':
                pos[0] -= 1
                fromdir = 'D'
            elif fromdir != 'R' and data[pos[0]][pos[1] + 1] != '#':
                pos[1] += 1
                fromdir = 'L'
            elif fromdir != 'L' and data[pos[0]][pos[1] - 1] != '#':
                pos[1] -= 1
                fromdir = 'R'
            length += 1
            if pos in pois:
                if tuple(trail[2]) not in paths:
                    paths[tuple(trail[2])] = {}
                paths[tuple(trail[2])][tuple(pos)] = length
                break

    # find longest path
    buff = [[(0, 1), 0, [(0, 1)]]]
    visited = {(0, 1): 0}
    maxtrail = 0
    while buff:
        work = buff.pop()
        if work[0] == (height - 1, width - 2):
            if work[1] > maxtrail:
                maxtrail = work[1]
            continue
        for target, dist in paths[work[0]].items():
            if target in work[2]:
                continue
            visited[target] = work[1] + dist
            buff.append([target, work[1] + dist, work[2] + [target]])

    return maxtrail


def main():
    """
    Main function
    """

    # process args
    infile = get_args()

    # read data
    data = read_data_struct(infile)

    # part 1
    dists = get_dists(data)
    print(f"Part 1 solution : {dists}")

    # part 2
    dists = get_dists_both_ways(data)
    print(f"Part 2 solution : {dists}")


if __name__ == '__main__':
    main()

# EOF
