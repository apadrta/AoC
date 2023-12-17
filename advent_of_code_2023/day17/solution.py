#!/usr/bin/env python
# -*- coding:utf-8 -*-
"""
Advent of code 2023 - Day 17
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
        description='Advent of code 2023: Day 17'
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
    arr = np.zeros((height, width), int)
    for idx, line in enumerate(data):
        for jdx, char in enumerate(line):
            arr[(idx, jdx)] = int(char)
    return arr


def find_crucible_path(data):
    """
    Find path with minimal heat loss
    """
    # create graph
    graph = Graph()
    height = len(data)
    width = len(data[0])
    size = width * height

    # join start and finish states
    graph.add_edge(0, size, 0)
    graph.add_edge(size - 1, 2 * size - 1, 0)

    # generate edges
    for idx in range(0, height):
        for jdx in range(0, width):
            # 0 ... size -1 = horizontal movement allowed
            val = 0
            for kdx in range(0, 3):
                target = jdx + kdx + 1
                if target > width - 1:
                    break
                val += data[idx, target]
                graph.add_edge(idx * width + jdx, idx * width + (target + size), val)
            val = 0
            for kdx in range(0, 3):
                target = jdx - kdx - 1
                if target < 0:
                    break
                val += data[idx, target]
                graph.add_edge(idx * width + jdx, idx * width + (target + size), val)
            # size .. 2 * size - 1 = vertical movement allowed
            val = 0
            for kdx in range(0, 3):
                target = idx + kdx + 1
                if target > height - 1:
                    break
                val += data[target, jdx]
                graph.add_edge(idx * width + jdx + size, target * width + jdx, val)
            val = 0
            for kdx in range(0, 3):
                target = idx - kdx - 1
                if target < 0:
                    break
                val += data[target, jdx]
                graph.add_edge(idx * width + jdx + size, target * width + jdx, val)

    # use Dijkstra algorithm
    startnode = 0
    endnode = 2 * size - 1
    res = find_path(graph, startnode, endnode)
    print(res.costs)

    return res.total_cost


def find_ultra_crucible_path(data):
    """
    Find path with minimal heat loss
    """
    # create graph
    graph = Graph()
    height = len(data)
    width = len(data[0])
    size = width * height

    # join start and finish states
    graph.add_edge(0, size, 0)
    graph.add_edge(size - 1, 2 * size - 1, 0)

    # generate edges
    for idx in range(0, height):
        for jdx in range(0, width):
            # 0 ... size -1 = horizontal movement allowed
            val = 0
            for kdx in range(0, 10):
                target = jdx + kdx + 1
                if target > width - 1:
                    break
                val += data[idx, target]
                if kdx < 3:
                    continue
                graph.add_edge(idx * width + jdx, idx * width + (target + size), val)
            val = 0
            for kdx in range(0, 10):
                target = jdx - kdx - 1
                if target < 0:
                    break
                val += data[idx, target]
                if kdx < 3:
                    continue
                graph.add_edge(idx * width + jdx, idx * width + (target + size), val)
            # size .. 2 * size - 1 = vertical movement allowed
            val = 0
            for kdx in range(0, 10):
                target = idx + kdx + 1
                if target > height - 1:
                    break
                val += data[target, jdx]
                if kdx < 3:
                    continue
                graph.add_edge(idx * width + jdx + size, target * width + jdx, val)
            val = 0
            for kdx in range(0, 10):
                target = idx - kdx - 1
                if target < 0:
                    break
                val += data[target, jdx]
                if kdx < 3:
                    continue
                graph.add_edge(idx * width + jdx + size, target * width + jdx, val)

    # use Dijkstra algorithm
    startnode = 0
    endnode = 2 * size - 1
    res = find_path(graph, startnode, endnode)
    print(res.costs)

    return res.total_cost


def main():
    """
    Main function
    """

    # process args
    infile = get_args()

    # read data
    data = read_data_struct(infile)

    # part 1
    sums = find_crucible_path(data)
    print(f"Part 1 solution: {sums}")

    # part 2
    sums = find_ultra_crucible_path(data)
    print(f"Part 2 solution: {sums}")


if __name__ == '__main__':
    main()

# EOF
