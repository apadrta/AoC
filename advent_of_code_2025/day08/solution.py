#!/usr/bin/env python
# -*- coding:utf-8 -*-
"""
Advent of Code solution
"""

import argparse


def get_args():
    """
    Cmd line argument parsing (preprocessing)
    """
    # Assign description to the help doc
    parser = argparse.ArgumentParser(
        description='Advent of code 2025 day 8')

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
    distances = []
    for item in data:
        newnode = [int(x) for x in item.split(',')]
        for idx, node in enumerate(nodes):
            dst = 0
            for jdx, value in enumerate(node):
                dst += (value - newnode[jdx]) * (value - newnode[jdx])
            distances.append([dst, len(nodes), idx])
        nodes.append(newnode)
    distances.sort(key=lambda x: x[0])
    return nodes, distances


def count_circuits(distances, maxcnt, nodes):
    """
    count circuits for part 1
    """
    circuits = {}
    assignment = {}
    one_circuit = 0
    for dist in distances[:maxcnt]:
        if dist[1] in assignment and dist[2] not in assignment:
            # one end (A) is in some circuit
            circuits[assignment[dist[1]]].append(dist[2])
            assignment[dist[2]] = assignment[dist[1]]
        elif dist[2] in assignment and dist[1] not in assignment:
            # one end (B) is in some circuit
            circuits[assignment[dist[2]]].append(dist[1])
            assignment[dist[1]] = assignment[dist[2]]
        elif dist[2] not in assignment and dist[1] not in assignment:
            # whole new circuit
            idx = len(circuits)
            circuits[idx] = [dist[1], dist[2]]
            assignment[dist[1]] = idx
            assignment[dist[2]] = idx
        elif assignment[dist[1]] == assignment[dist[2]]:
            # both ends are in the same circuits (nothing happens)
            continue
        else:
            # each end ends in different circuit - merge circuits
            src = max(assignment[dist[1]], assignment[dist[2]])
            dst = min(assignment[dist[1]], assignment[dist[2]])
            for item in circuits[src]:
                assignment[item] = dst
            circuits[dst] += circuits[src]
            circuits[src] = []
        if len(circuits[0]) == len(nodes):
            # count part 2 check
            one_circuit = nodes[dist[1]][0] * nodes[dist[2]][0]

    # count part 1 check
    lens = []
    for item in circuits.values():
        lens.append(len(item))
    lens.sort(reverse=True)
    sums = 1
    for value in lens[0:3]:
        sums *= value
    return sums, one_circuit


def main():
    """
    main
    """

    filename = get_args()
    nodes, distances = read_data(filename)

    # part 1
    sums, _ = count_circuits(distances, 1000, nodes)
    print(f"Solution part 1: {sums}")

    _, sums = count_circuits(distances, 1000000000, nodes)
    print(f"Solution part 2: {sums}")


if __name__ == '__main__':
    main()

# EOF
