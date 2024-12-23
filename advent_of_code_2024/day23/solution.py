#!/usr/bin/env python
# -*- coding:utf-8 -*-
"""
Advent of code 2024 - Day 23
"""

import argparse
from itertools import combinations
import numpy as np
import networkx as nx


def get_args():
    """
    Cmd line argument parsing (preprocessing)
    """
    # Assign description to the help doc
    parser = argparse.ArgumentParser(
        description='Advent of code 2024: Day 23')

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


def read_data(filename):
    """
    Read and prepare data
    """
    # read file
    data = []
    with open(filename, "r") as fileh:
        data = fileh.readlines()
    data = [x.replace('\r', '').replace('\n', '') for x in data]

    net = []
    for item in data:
        net.append(item.split('-'))
    return net


def eval_net(data):
    """
    make connection matrix
    """
    nodes = {}
    idx = 0
    for item in data:
        if item[0] not in nodes:
            nodes[item[0]] = idx
            idx += 1
        if item[1] not in nodes:
            nodes[item[1]] = idx
            idx += 1
    matrix = np.zeros((len(nodes), len(nodes)), dtype=int)

    for item in data:
        matrix[nodes[item[0]], nodes[item[1]]] = 1
        matrix[nodes[item[1]], nodes[item[0]]] = 1

    return nodes, matrix


def get_tripplets(nodes, matrix):
    """
    get list of tripplets
    """
    triplets = []
    for idx, jdx, kdx in combinations(nodes.values(), 3):
        if matrix[idx, jdx] and matrix[idx, kdx] and matrix[jdx, kdx]:
            triplets.append([idx, jdx, kdx])
    return triplets


def get_max_clique(matrix):
    """
    get largest clique
    """
    nxmatrix = nx.from_numpy_array(matrix)
    cliques = list(nx.find_cliques(nxmatrix))
    maxs = cliques[0]
    for clique in cliques:
        if len(clique) > len(maxs):
            maxs = clique
    return maxs


def main():
    """
    Main function
    """

    # process args
    infile = get_args()

    # read data
    data = read_data(infile)

    # part 1
    nodes, matrix = eval_net(data)
    tripplets = get_tripplets(nodes, matrix)
    target = []
    for key, value in nodes.items():
        if key[0] == 't':
            target.append(value)
    sums = 0
    for tripplet in tripplets:
        if set(target) & set(tripplet):
            sums += 1
    print(f"Part 1 solution: {sums}")

    # part 2
    sums = 0
    maxs = get_max_clique(matrix)
    revnodes = {}
    for key, value in nodes.items():
        revnodes[value] = key
    names = []
    for item in maxs:
        names.append(revnodes[item])
    print(f"Part 2 solution: {','.join(sorted(names))}")


if __name__ == '__main__':
    main()

# EOF
