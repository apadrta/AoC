#!/usr/bin/env python
# -*- coding:utf-8 -*-
"""
Advent of code 2022 - Day 12
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
        description='Advent of code 2022: Day 12')

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


def get_path(data, startnode, endnode):
    """
    Compute shortest path
    """
    sizei = np.size(data, 0)
    sizej = np.size(data, 1)
    graph = Graph()
    for i in range(0, sizei):
        for j in range(0, sizej):
            if j < sizej - 1:
                if data[(i, j+1)] - data[(i, j)] <= 1:
                    graph.add_edge((i*sizej)+j, (i*sizej)+(j+1), 1)
                if data[(i, j)] - data[(i, j+1)] <= 1:
                    graph.add_edge((i*sizej)+(j+1), (i*sizej)+j, 1)
            if i < sizei - 1:
                if data[(i+1, j)] - data[(i, j)] <= 1:
                    graph.add_edge((i*sizej)+j, (i+1)*sizej+j, 1)
                if data[(i, j)] - data[(i+1, j)] <= 1:
                    graph.add_edge((i+1)*sizej+j, (i*sizej)+j, 1)
    return find_path(graph, startnode, endnode).total_cost


def get_paths(data, a_nodes, end_node):
    """
    Compute shortest path from different nodes
    """
    path_lengths = []
    for a_node in a_nodes:
        try:
            path_lengths.append(get_path(data, a_node, end_node))
        finally:
            continue
    return min(path_lengths)


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

    # preprocessing
    climb = np.zeros((len(lines), len(lines[0])), dtype=int)
    start_node = 0
    end_node = 0
    a_nodes = []
    i = 0
    for line in lines:
        proc = line.replace('S', 'a').replace('E', 'z')
        proc = [ord(x) for x in proc]
        j = 0
        for val in proc:
            climb[(i, j)] = val - 97
            if line[j] == 'S':
                start_node = i * len(line) + j
            if line[j] == 'E':
                end_node = i * len(line) + j
            if val == 97:
                a_nodes.append(i * len(line) + j)
            j += 1
        i += 1

    # part 1
    res = get_path(climb, start_node, end_node)
    print(f"Part 1 solution: {res}")

    # part 2
    res = get_paths(climb, a_nodes, end_node)
    print(f"Part 2 solution: {res}")


if __name__ == '__main__':
    main()

# EOF
