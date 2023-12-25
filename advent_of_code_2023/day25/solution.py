#!/usr/bin/env python
# -*- coding:utf-8 -*-
"""
Advent of code 2023 - Day 25
"""

import argparse
import numpy as np
import scipy.sparse


def get_args():
    """
    Cmd line argument parsing (preprocessing)
    """
    # Assign description to the help doc
    parser = argparse.ArgumentParser(
        description='Advent of code 2023: Day 25'
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

    nodes = {}
    for line in data:
        left, right = line.split(': ')
        local_nodes = right.split(' ') + [left]
        for local_node in local_nodes:
            nodes[local_node] = 0
    for idx, value in enumerate(nodes.keys()):
        nodes[value] = idx

    arr = np.zeros((len(nodes), len(nodes)), dtype=int)
    for line in data:
        left, rights = line.split(': ')
        for right in rights.split(' '):
            arr[(nodes[left], nodes[right])] = 1
            arr[(nodes[right], nodes[left])] = 1

    return arr


def div_components(data):
    """
    divide to two groups
    """
    graph = scipy.sparse.csr_matrix(data)
    source = 0
    for idx in range(1, len(data)):
        flow = scipy.sparse.csgraph.maximum_flow(graph, source, idx)
        max_flow = scipy.sparse.csgraph.maximum_flow(graph, source, idx).flow_value
        if max_flow == 3:
            break

    source_nodes = scipy.sparse.csgraph.depth_first_order(graph - flow.flow, source)[0]
    return len(source_nodes) * (len(data) - len(source_nodes))


def main():
    """
    Main function
    """

    # process args
    infile = get_args()

    # read data
    data = read_data_struct(infile)

    # part 1
#    count = components_multiply(data, nodes)
    count = div_components(data)
    print(f"Part 1 solution : {count}")

    # part 2
#    count = find2(data)
#    print(f"Part 2 solution: {count}")


if __name__ == '__main__':
    main()

# EOF
