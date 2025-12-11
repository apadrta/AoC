#!/usr/bin/env python
# -*- coding:utf-8 -*-
"""
Advent of Code solution
"""

import argparse
from copy import deepcopy


def get_args():
    """
    Cmd line argument parsing (preprocessing)
    """
    # Assign description to the help doc
    parser = argparse.ArgumentParser(
        description='Advent of code 2025 day 11')

    # Add arguments
    parser.add_argument(
        '-i',
        '--infile',
        type=str,
        help='Input filename',
        required=True)

    # Array for all arguments passed to script
    args = parser.parse_args()

    # Return arg variables
    return args.infile


def read_data(filename):
    """
    read input data
    """
    data = []
    with open(filename, "r", encoding="utf8") as fhnd:
        data = fhnd.readlines()
    data = [x.strip() for x in data]

    nodes = []
    edges = {}

    for item in data:
        src, dst = item.split(': ')
        dst = dst.split(' ')
        nodes.append(src)
        edges[src] = dst

    return nodes, edges


def sort_nodes(nodes, edges):
    """
    topological sort
    """
    # init
    degrees = {}
    for node in nodes:
        degrees[node] = 0
    for dsts in edges.values():
        for dst in dsts:
            degrees[dst] += 1
    # sort
    remaining = deepcopy(nodes)
    process = []
    for item, value in degrees.items():
        if value == 0:
            process.append(item)
            remaining.remove(item)
    snodes = []

    while process:
        # get first item with zero prerequsities
        item = process.pop(0)
        snodes.append(item)
        # lower prerequisties in its destinations
        for dst in edges[item]:
            degrees[dst] -= 1
        # add zero prerequisited items to processing
        dels = []
        for node in remaining:
            if degrees[node] == 0:
                process.append(node)
                dels.append(node)
        for item in dels:
            remaining.remove(item)

    return snodes


def get_paths_number(nodes, edges, start_node, end_node):
    """
    counts number of different paths from start to end
    """
    if end_node not in nodes:
        nodes.append(end_node)
    if end_node not in edges:
        edges[end_node] = []
    nodes = sort_nodes(nodes, edges)
    dist = {}
    for node in nodes:
        dist[node] = 0
    dist[start_node] = 1

    for node in nodes:
        for dst in edges[node]:
            dist[dst] += dist[node]

    return dist[end_node]


def main():
    """
    main
    """

    filename = get_args()
    nodes, edges = read_data(filename)
    # part 1
    sums = get_paths_number(nodes, edges, 'you', 'out')
    print(f"Solution part 1: {sums}")

    # part 2
    svr_dac = get_paths_number(nodes, edges, 'svr', 'dac')
    svr_fft = get_paths_number(nodes, edges, 'svr', 'fft')
    dac_fft = get_paths_number(nodes, edges, 'dac', 'fft')
    fft_dac = get_paths_number(nodes, edges, 'fft', 'dac')
    dac_out = get_paths_number(nodes, edges, 'dac', 'out')
    fft_out = get_paths_number(nodes, edges, 'fft', 'out')
    sums = svr_dac * dac_fft * fft_out
    sums += svr_fft * fft_dac * dac_out
    print(f"Solution part2: {sums}")


if __name__ == '__main__':
    main()

# EOF
