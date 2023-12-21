#!/usr/bin/env python
# -*- coding:utf-8 -*-
"""
Advent of code 2023 - Day 21
"""

import argparse
import math
from copy import deepcopy
import numpy as np


def get_args():
    """
    Cmd line argument parsing (preprocessing)
    """
    # Assign description to the help doc
    parser = argparse.ArgumentParser(
        description='Advent of code 2023: Day 21'
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

    width = len(data[0])
    height = len(data)
    pos = [0, 0]
    arr = np.full((height, width), -1, dtype=int)
    for idx, line in enumerate(data):
        for jdx, char in enumerate(line):
            if char == '#':
                arr[(idx, jdx)] = -9
            elif char == 'S':
                pos = [idx, jdx]
    return arr, pos


def count_positions(data, start, steps):
    """
    count possible positions in given steps
    """
    width = len(data[0])
    height = len(data)
    even_hist = [start]
    odd_hist = []
    buff = [start]
    kdx = 0
    while kdx < steps:
        kdx += 1
        new_buff = []
        if kdx % 2 == 0:
            hist = even_hist
        else:
            hist = odd_hist
        new_pos = []
        for pos in buff:
            if pos[0] > 0 and data[tuple([pos[0] - 1, pos[1]])] == -1:
                new_pos.append([pos[0] - 1, pos[1]])
            if pos[0] < height - 1 and data[tuple([pos[0] + 1, pos[1]])] == -1:
                new_pos.append([pos[0] + 1, pos[1]])
            if pos[1] > 0 and data[tuple([pos[0], pos[1] - 1])] == -1:
                new_pos.append([pos[0], pos[1] - 1])
            if pos[1] < width - 1 and data[tuple([pos[0], pos[1] + 1])] == -1:
                new_pos.append([pos[0], pos[1] + 1])
        for pos in new_pos:
            if pos not in hist:
                hist.append(pos)
                new_buff.append(pos)
        buff = new_buff
    if steps % 2 == 0:
        return len(even_hist)
    return len(odd_hist)


def get_dist_matrix(data, start):
    """
    create distance matrix from starting point
    """
    dists = deepcopy(data)
    width = len(data[0])
    height = len(data)

    buff = [start]
    dists[tuple(start)] = 0
    while buff:
        new_buff = []
        for pos in buff:
            new_pos = [pos[0] - 1, pos[1]]
            if pos[0] > 0 and dists[tuple(new_pos)] == -1:
                new_buff.append(new_pos)
                dists[tuple(new_pos)] = dists[tuple(pos)] + 1
            new_pos = [pos[0] + 1, pos[1]]
            if pos[0] < height - 1 and dists[tuple(new_pos)] == -1:
                new_buff.append(new_pos)
                dists[tuple(new_pos)] = dists[tuple(pos)] + 1
            new_pos = [pos[0], pos[1] - 1]
            if pos[1] > 0 and dists[tuple(new_pos)] == -1:
                new_buff.append(new_pos)
                dists[tuple(new_pos)] = dists[tuple(pos)] + 1
            new_pos = [pos[0], pos[1] + 1]
            if pos[1] < width - 1 and dists[tuple(new_pos)] == -1:
                new_buff.append(new_pos)
                dists[tuple(new_pos)] = dists[tuple(pos)] + 1
        buff = new_buff
    return dists


def get_points(data, steps):
    """
    count number of end positions in dist matrix for given number of steps
    """
    width = len(data[0])
    height = len(data)
    res = 0
    for idx in range(0, height):
        for jdx in range(0, width):
            if data[(idx, jdx)] < 0 or data[(idx, jdx)] > steps:
                continue
            if steps % 2 == 0 and (data[(idx, jdx)]) % 2 == 0:
                res += 1
            elif steps % 2 == 1 and (data[(idx, jdx)]) % 2 == 1:
                res += 1
    return res


def count_infinity(data, start, steps):
    """
    count possible positions in give steps
    """
    # prepare distance matrixes
    width = len(data[0])
    height = len(data)
    halfheight = (height - 1) // 2
    pois = {
       'start': start,
       'left': [(height - 1)//2, 0],
       'right': [(height - 1)//2, width - 1],
       'top': [0, (width - 1)//2],
       'bottom': [height - 1, (width - 1)//2],
       'topleft': [0, 0],
       'topright': [0, width - 1],
       'bottomleft': [height - 1, 0],
       'bottomright': [height - 1, width - 1],
    }
    matrixes = {}
    for name, poi in pois.items():
        matrixes[name] = get_dist_matrix(data, poi)

    # precount useful numbers
    upsize = (steps - (height - 1) // 2) // height
    halfheight = (height - 1) // 2
    topindex = (upsize-1) * height + halfheight + 1
    slopeindex1 = steps - halfheight + 1
    slopeindex2 = steps - height - halfheight + 1
    quadrant_even = math.floor((upsize-2)/2) * (math.floor((upsize-2)/2) + 1)
    quadrant_odd = math.ceil((upsize-2)/2) * math.ceil((upsize-2)/2) - 1

    # count possible garden plots
    sums = 0

    # start point
    res = get_points(matrixes['start'], steps)
    print(f'-> start += {res} (1x)')
    sums += res
    # end points (not full maps)
    res = get_points(matrixes['bottom'], steps - topindex)
    print(f'-> bottom += {res} (1x)')
    sums += res
    res = get_points(matrixes['top'], steps - topindex)
    print(f'-> top += {res} (1x)')
    sums += res
    res = get_points(matrixes['left'], steps - topindex)
    print(f'-> left += {res} (1x)')
    sums += res
    res = get_points(matrixes['right'], steps - topindex)
    print(f'-> right += {res} (1x)')
    sums += res
    # count slopes (not full maps)
    res = get_points(matrixes['bottomleft'], steps - slopeindex1)
    print(f'-> bottomleft type x += {res} ({upsize}x)')
    sums += res * upsize
    res = get_points(matrixes['bottomleft'], steps - slopeindex2)
    print(f'-> bottomleft type y += {res} ({upsize - 1}x)')
    sums += res * (upsize - 1)
    res = get_points(matrixes['bottomright'], steps - slopeindex1)
    print(f'-> bottomright type x += {res} ({upsize}x)')
    sums += res * upsize
    res = get_points(matrixes['bottomright'], steps - slopeindex2)
    print(f'-> bottomright type y += {res} ({upsize - 1}x)')
    sums += res * (upsize - 1)
    res = get_points(matrixes['topleft'], steps - slopeindex1)
    print(f'-> topleft type x += {res} ({upsize}x)')
    sums += res * upsize
    res = get_points(matrixes['topleft'], steps - slopeindex2)
    print(f'-> topleft type y += {res} ({upsize - 1}x)')
    sums += res * (upsize - 1)
    res = get_points(matrixes['topright'], steps - slopeindex1)
    print(f'-> topright type x += {res} ({upsize}x)')
    sums += res * upsize
    res = get_points(matrixes['topright'], steps - slopeindex2)
    print(f'-> topright type y += {res} ({upsize - 1}x)')
    sums += res * (upsize - 1)
    # count full straight
    res = get_points(matrixes['bottom'], steps)
    print(f'-> full bottom (even) += {res} ({math.ceil(upsize/2)}x)')
    sums += res * math.ceil(upsize/2)
    res = get_points(matrixes['bottom'], steps - 1)
    print(f'-> full bottom (odd) += {res} ({math.floor(upsize/2)}x)')
    sums += res * math.floor(upsize/2)
    res = get_points(matrixes['top'], steps)
    print(f'-> full top (even) += {res} ({math.ceil(upsize/2)}x)')
    sums += res * math.ceil(upsize/2)
    res = get_points(matrixes['top'], steps - 1)
    print(f'-> full top (odd) += {res} ({math.floor(upsize/2)}x)')
    sums += res * math.floor(upsize/2)
    res = get_points(matrixes['left'], steps)
    print(f'-> full left (even) += {res} ({math.ceil(upsize/2)}x)')
    sums += res * math.ceil(upsize/2)
    res = get_points(matrixes['right'], steps - 1)
    print(f'-> full left (odd) += {res} ({math.floor(upsize/2)}x)')
    sums += res * math.floor(upsize/2)
    res = get_points(matrixes['bottom'], steps)
    print(f'-> full right (even) += {res} ({math.ceil(upsize/2)}x)')
    sums += res * math.ceil(upsize/2)
    res = get_points(matrixes['bottom'], steps - 1)
    print(f'-> full right (odd) += {res} ({math.floor(upsize/2)}x)')
    sums += res * math.floor(upsize/2)
    # count full quadrants
    res = get_points(matrixes['bottomleft'], steps - 1)
    print(f'-> full bottomleft (even) += {res} ({quadrant_even}x)')
    sums += res * quadrant_even
    res = get_points(matrixes['bottomleft'], steps)
    print(f'-> full bottomleft (odd) += {res} ({quadrant_odd}x)')
    sums += res * quadrant_odd
    res = get_points(matrixes['bottomright'], steps - 1)
    print(f'-> full bottomright (even) += {res} ({quadrant_even}x)')
    sums += res * quadrant_even
    res = get_points(matrixes['bottomright'], steps)
    print(f'-> full bottomright (odd) += {res} ({quadrant_odd}x)')
    sums += res * quadrant_odd
    res = get_points(matrixes['topleft'], steps - 1)
    print(f'-> full topleft (even) += {res} ({quadrant_even}x)')
    sums += res * quadrant_even
    res = get_points(matrixes['topleft'], steps)
    print(f'-> full topleft (odd) += {res} ({quadrant_odd}x)')
    sums += res * quadrant_odd
    res = get_points(matrixes['topright'], steps - 1)
    print(f'-> full topright (even) += {res} ({quadrant_even}x)')
    sums += res * quadrant_even
    res = get_points(matrixes['bottomleft'], steps)
    print(f'-> full bottomleft (odd) += {res} ({quadrant_odd}x)')
    sums += res * quadrant_odd

    return sums


def main():
    """
    Main function
    """

    # process args
    infile = get_args()

    # read data
    data, start = read_data_struct(infile)

    # part 1
    count = count_positions(data, start, 64)
    print(f"Part 1 solution : {count}")

    # part 2
    count = count_infinity(data, start, 26501365)
    print(f"Part 2 solution: {count}")


if __name__ == '__main__':
    main()

# EOF
