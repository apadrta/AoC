#!/usr/bin/env python
# -*- coding:utf-8 -*-
"""
Advent of code 2022 - Day 22
"""

import argparse
import numpy as np


def get_args():
    """
    Cmd line argument parsing (preprocessing)
    """
    # Assign description to the help doc
    parser = argparse.ArgumentParser(
        description='Advent of code 2022: Day 22')

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


def parse_input(lines):
    """
    Preprocess input
    """
    # read map
    width = 0
    for line in lines[:-2]:
        if len(line) > width:
            width = len(line)
    data = np.zeros((len(lines) - 2, width), dtype=int)
    for idx, line in enumerate(lines[:-2]):
        for jdx, char in enumerate(line):
            if char == '.':
                data[(idx, jdx)] = 1
            elif char == '#':
                data[(idx, jdx)] = 8
    # read path
    path = [int(x) for x in lines[-1].replace('L', ' -1 ').replace('R', ' -2 ').split(' ')]
    for idx, item in enumerate(path):
        if item == -1:
            path[idx] = 'L'
        elif item == -2:
            path[idx] = 'R'

    return data, path


facing = [
    (0, 1),
    (1, 0),
    (0, -1),
    (-1, 0)
]


def print_map(mapdata, filename):
    """
    print map data
    """
    chars = {
        0: ' ',
        1: '.',
        2: '>',
        3: 'v',
        4: '<',
        5: '^',
        8: '#',
    }
    with open(filename, "w") as fhnd:
        for idx in range(0, mapdata.shape[0]):
            for jdx in range(0, mapdata.shape[1]):
                if mapdata[(idx, jdx)] in chars:
                    fhnd.write(chars[mapdata[(idx, jdx)]])
                else:
                    fhnd.write(mapdata[(idx, jdx)])
            fhnd.write('\n')


def solve_part1(mapdata, path):
    """
    go througp map
    """
    # get starting tile
    pos = [0, 0]
    for idx in range(0, mapdata.shape[1]):
        if mapdata[(0, idx)] == 1:
            pos[1] = idx
            break
    # follow path
    orientation = 0
    mapdata[tuple(pos)] = 2 + orientation
    idx = 0
    for inst in path:
        # turn
        if inst == 'R':
            orientation = (orientation + 1) % 4
            mapdata[tuple(pos)] = 2 + orientation
            continue
        if inst == 'L':
            orientation = (orientation - 1) % 4
            mapdata[tuple(pos)] = 2 + orientation
            continue
        # move
        for _ in range(0, inst):
            next_pos = [(pos[0] + facing[orientation][0]) % mapdata.shape[0], (pos[1] + facing[orientation][1]) % mapdata.shape[1]]
            while mapdata[tuple(next_pos)] == 0:
                next_pos = [(next_pos[0] + facing[orientation][0]) % mapdata.shape[0], (next_pos[1] + facing[orientation][1]) % mapdata.shape[1]]
            if mapdata[tuple(next_pos)] == 8:
                break
            pos = next_pos
            mapdata[tuple(pos)] = 2 + orientation
        idx += 1
    return 1000 * (pos[0] + 1) + 4 * (pos[1] + 1) + orientation


def create_teleport_matrix(data):
    """
    Create transformation matrix
    """
    # implemented only for example + specific input
    # todo: make generic in the the future
    if data.shape[1] == 16:
        matrix = {
            (0, 5, 12): (1, 8, 14),
            (1, 12, 10): (3, 7, 1),
            (3, 3, 6): (0, 2, 8)
        }
        return matrix

    cranges = [
        [3, [-1, 50], [-1, 99], 0, [150, 0], [199, 0]],    # 01 -> 11
        [3, [-1, 100], [-1, 149], 3, [199, 0], [199, 49]],  # 02 -> 12
        [2, [0, 49], [49, 49], 0, [149, 0], [100, 0]],     # 03 -> 10
        [2, [50, 49], [99, 49], 1, [100, 0], [100, 49]],    # 04 -> 09
        [0, [0, 150], [49, 150], 2, [149, 99], [100, 99]],    # 05 -> 08
        [1, [50, 100], [50, 149], 2, [50, 99], [99, 99]],  # 06 -> 07
        [0, [50, 100], [99, 100], 3, [49, 100], [49, 149]],   # 07 -> 06
        [0, [100, 100], [149, 100], 2, [49, 149], [0, 149]],  # 08 -> 05
        [3, [99, 0], [99, 49], 0, [50, 50], [99, 50]],     # 09 -> 04
        [2, [100, -1], [149, -1], 0, [49, 50], [0, 50]],   # 10 -> 03
        [2, [150, -1], [199, -1], 1, [0, 50], [0, 99]],    # 11 -> 01
        [1, [200, 0], [200, 49], 1, [0, 100], [0, 149]],   # 12 -> 02
        [0, [150, 50], [199, 50], 3, [149, 50], [149, 99]],  # 13 -> 14
        [1, [150, 50], [150, 99], 2, [150, 49], [199, 49]]  # 14 -> 13
    ]
    # 01 ^ -1,50, -1,99) => 11 >
    # 02 ^ -1,100 -1,149 => 12 ^
    # 03 < 0,49 49,49 => 10 >
    # 04 < 50,49, 99,49 => 09 v
    # 05 > 0,150 49,150 => 08 <
    # 06 v 50,100 50,149 => 07 <
    # 07 > 50,100, 99,100 => 06 ^
    # 08 > 100,100 149,100 => 05 <
    # 09 ^ 99,0 99,49 => 04 >
    # 10 < 100,-1 149,-1 => 3 >
    # 11 < 150,-1 199,-1 => 1 v
    # 12 v 200,0 200,49 => v
    # 13 > 150,50 199,50 => 14 ^
    # 14 v 150,50 150,99 => 13 <
    matrix = {}
    for crange in cranges:
        for idx in range(0, 50):
            # evaluate source
            if crange[1][0] == crange[2][0]:
                mid = (crange[0], crange[1][0], crange[1][1]+idx)
            else:
                mid = (crange[0], crange[1][0]+idx, crange[1][1])
            # evaluate target
            tgt_diff = +idx
            if crange[4][0] > crange[5][0] or crange[4][1] > crange[5][1]:
                tgt_diff = -idx
            if crange[4][0] == crange[5][0]:
                # follow row
                matrix[mid] = (crange[3], crange[4][0], crange[4][1] + tgt_diff)
            else:
                # follow column
                matrix[mid] = (crange[3], crange[4][0] + tgt_diff, crange[4][1])
    return matrix


def solve_part2(mapdata, path):
    """
    go around cube
    """
    matrix = create_teleport_matrix(mapdata)
    # get starting tile
    pos = [0, 0]
    for idx in range(0, mapdata.shape[1]):
        if mapdata[(0, idx)] == 1:
            pos[1] = idx
            break
    # follow path
    orientation = 0
#    pos = [199, 49]
#    path = ['R', 100]
    mapdata[tuple(pos)] = 2 + orientation
    for inst in path:
        # turn
        if inst == 'R':
            orientation = (orientation + 1) % 4
            mapdata[tuple(pos)] = 2 + orientation
            continue
        if inst == 'L':
            orientation = (orientation - 1) % 4
            mapdata[tuple(pos)] = 2 + orientation
            continue
        # move
        for _ in range(0, inst):
            next_pos = [pos[0] + facing[orientation][0], pos[1] + facing[orientation][1]]
            next_orientation = orientation
            tel_id = (orientation, next_pos[0], next_pos[1])
            if tel_id in matrix:
                mod_pos = matrix[tel_id]
                next_orientation = mod_pos[0]
                next_pos = [mod_pos[1], mod_pos[2]]
            if mapdata[tuple(next_pos)] == 8:
                # hit wall
                break
            pos = next_pos
            orientation = next_orientation
            mapdata[tuple(pos)] = 2 + orientation
    print_map(mapdata, 'out.txt')
    return 1000 * (pos[0] + 1) + 4 * (pos[1] + 1) + orientation


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
    lines = [x.replace('\n', '').replace('\r', '') for x in data]

    # part 1
    data, path = parse_input(lines)
    res = solve_part1(data, path)
    print(f"Part 1 solution: {res}")

    # part 2
    data, path = parse_input(lines)
    res = solve_part2(data, path)
    print(f"Part 2 solution: {res}")


if __name__ == '__main__':
    main()

# EOF
