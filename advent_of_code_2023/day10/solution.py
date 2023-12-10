#!/usr/bin/env python
# -*- coding:utf-8 -*-
"""
Advent of code 2023 - Day 10
"""

import argparse
import numpy as np
from skimage.morphology import flood_fill


def get_args():
    """
    Cmd line argument parsing (preprocessing)
    """
    # Assign description to the help doc
    parser = argparse.ArgumentParser(
        description='Advent of code 2023: Day 10'
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
    maps = [x.strip() for x in data]

    for idx, line in enumerate(data):
        if 'S' in line:
            start = (idx, line.find('S'))  # line, column (y, x)
            break

    return maps, start


def find_connected(maps, start):
    """
    Find connected positions for given starting point
    """
    pipe = maps[start[0]][start[1]]
    positions = []
    # up
    if start[0] > 0 and pipe in 'S|LJ' and maps[start[0]-1][start[1]] in '|F7S':
        positions.append((start[0]-1, start[1]))
    # down
    if start[0] < len(maps) - 1 and pipe in 'S|F7' and maps[start[0]+1][start[1]] in '|LJS':
        positions.append((start[0]+1, start[1]))
    # left
    if start[1] > 0 and pipe in 'S-7J' and maps[start[0]][start[1]-1] in '-FLS':
        positions.append((start[0], start[1]-1))
    # right
    if start[1] < len(maps[0]) - 1 and pipe in 'S-FL' and maps[start[0]][start[1]+1] in '-7JS':
        positions.append((start[0], start[1]+1))
    return positions


def farthest_distance(maps, start):
    """
    Find farthest distance
    """
    data = np.full((len(maps), len(maps[0])), -1, dtype=int)
    data[(start)] = 0
    positions = [start]
    max_dist = 0
    while positions:
        new_positions = []
        for pos in positions:
            work_positions = find_connected(maps, pos)
            for work_pos in work_positions:
                if data[work_pos] == -1:
                    data[work_pos] = data[pos] + 1
                    if data[pos] + 1 > max_dist:
                        max_dist = data[pos] + 1
                    new_positions.append(work_pos)
        positions = new_positions
    return max_dist, data


def count_enclosed(maps, data):
    """
    Count inside tiles
    """
    dists = data.shape
    arr = np.full((dists[0] + 2, dists[1] + 2), -1, dtype=int)
    arr[1:-1, 1:-1] = data
    arr = flood_fill(arr, (0, 0), -9)
    sums = 0
    for idx in range(0, dists[0] + 2):
        for jdx in range(0, dists[1] + 2):
            if arr[(idx, jdx)] == -1:
                crossings = 0
                last_num = None
                last_turn = ''
                point = (idx, jdx)
                while point[1] != 0:
                    point = (point[0], point[1]-1)
                    if arr[point] >= 0:
                        if maps[point[0]-1][point[1]-1] == '-':
                            last_num = arr[point]
                            continue
                        if not last_num:
                            # new crossing
                            last_num = arr[point]
                            if maps[point[0]-1][point[1]-1] in 'LJ':
                                last_turn = 'up'
                            elif maps[point[0]-1][point[1]-1] in 'F7':
                                last_turn = 'down'
                            crossings += 1
                        elif abs(last_num - arr[point]) != 1:
                            # other tight crossing
                            last_num = arr[point]
                            if maps[point[0]-1][point[1]-1] in 'LJ':
                                last_turn = 'up'
                            elif maps[point[0]-1][point[1]-1] in 'F7':
                                last_turn = 'down'
                            crossings += 1
                        else:
                            # crossing continue
                            if last_turn == 'up' and maps[point[0]-1][point[1]-1] in 'LJ':
                                crossings -= 1
                            elif last_turn == 'down' and maps[point[0]-1][point[1]-1] in 'F7':
                                crossings -= 1
                    else:
                        last_num = None
                if int(crossings) % 2 == 1:
                    sums += 1
    return sums


def main():
    """
    Main function
    """

    # process args
    infile = get_args()

    # read data
    maps, start = read_data_struct(infile)

    # part 1
    dist, data = farthest_distance(maps, start)
    print(f"Part 1 solution: {dist}")

    # part 2
    count = count_enclosed(maps, data)
    print(f"Part 2 solution: {count}")


if __name__ == '__main__':
    main()

# EOF
