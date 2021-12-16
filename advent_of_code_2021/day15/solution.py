#!/usr/bin/env python
# -*- coding:utf-8 -*-
"""
Advent of code 2021 - Day 15
"""

import argparse
import numpy as np
from dijkstar import Graph, find_path


def get_args():
    """
    Cmd line argument parsing (preprocessing)
    """
    # Assign description to the help doc
    parser = argparse.ArgumentParser(
        description='Advent of code 2021: Day 15')

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


def increase_danger(tile):
    """
    increase danger by one
    """
    size = np.size(tile, 0)
    for i in range(0, size):
        for j in range(0, size):
            tile[i, j] += 1
            if tile[i, j] > 9:
                tile[i, j] = 1
    return tile


def enlarge_floor(tile, repeat):
    """
    create larger floor (square)
    """
    size = np.size(tile, 0)
    newsize = size * repeat
    newmap = np.full((newsize, newsize), -1, dtype=int)
    for k in range(0, repeat * 2 - 1):
        if k < repeat:
            minrange = 0
            maxrange = k + 1
        else:
            minrange = k - repeat + 1
            maxrange = repeat
        for i in range(minrange, maxrange):
            pos = (i, k-i)
            newmap[pos[0]*size:(pos[0]+1)*size, pos[1]*size:(pos[1]+1)*size] = tile
        tile = increase_danger(tile)
    return newmap


def get_danger(floor):
    """
    Get cumulative danger optimal
    """
    size = np.size(floor, 0)
    graph = Graph()
    for i in range(0, size):
        for j in range(0, size):
            if j < size - 1:
                graph.add_edge((i*size)+j, (i*size)+(j+1), floor[(i, j+1)])
                graph.add_edge((i*size)+(j+1), (i*size)+j, floor[(i, j)])
            if i < size - 1:
                graph.add_edge((i*size)+j, (i+1)*size+j, floor[(i+1, j)])
                graph.add_edge((i+1)*size+j, (i*size)+j, floor[(i, j)])
    return find_path(graph, 0, size*size-1)


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
    lines = [x.strip() for x in data]

    # first part
    danger = np.zeros((len(lines), len(lines[0])), dtype=int)
    i = 0
    for line in lines:
        j = 0
        for char in line:
            danger[(i, j)] = int(char)
            j += 1
        i += 1

    # part 1
    res = get_danger(danger)
    print(f"Part 1 solution: {res.total_cost}")

    # part 2
    newdanger = enlarge_floor(danger, 5)
    res = get_danger(newdanger)
    print(f"Part 2 solution: {res.total_cost}")


if __name__ == '__main__':
    main()

# EOF
