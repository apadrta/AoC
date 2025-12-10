#!/usr/bin/env python
# -*- coding:utf-8 -*-
"""
Advent of Code solution
"""

import argparse
from dijkstar import Graph, find_path
import z3


def get_args():
    """
    Cmd line argument parsing (preprocessing)
    """
    # Assign description to the help doc
    parser = argparse.ArgumentParser(
        description='Advent of code 2025 day 10')

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

    machines = []
    for item in data:
        parts = item.split(' ')
        machine = {}
        for part in parts:
            if part[0] == '[':
                part = part[1:-1].replace('.', '0').replace('#', '1')
                machine['len'] = len(part)
                machine['final'] = int(part, 2)
                machine['trans'] = []
                machine['wires'] = []
            elif part[0] == '(':
                tmp = ['0'] * machine['len']
                wires = [int(x) for x in part[1:-1].split(',')]
                machine['wires'].append(wires)
                for wire in wires:
                    tmp[wire] = '1'
                machine['trans'].append(int(''.join(tmp), 2))
            if part[0] == '{':
                machine['joltage'] = [int(x) for x in part[1:-1].split(',')]
        machines.append(machine)

    return machines


def dijkstra_part1(machine):
    """
    compute best path by dijkstra
    """
    size = 2**machine['len']
    graph = Graph()
    idx = 0
    while idx < size:
        for trans in machine['trans']:
            dst = idx ^ trans
            graph.add_edge(idx, dst, 1)
        idx += 1

    res = find_path(graph, 0, machine['final'])
    return res.total_cost


def get_matrix(machine):
    """
    prepare matrix for z3
    """
    matrix = []
    for idx in range(0, machine['len']):
        line = [0] * 13
        for jdx, value in enumerate(machine['wires']):
            if idx in value:
                line[jdx] = 1

        matrix.append(line)
    return matrix


def z3_part2(machine):
    """
    solve equation by z3
    """

    # prepare data
    matrix = get_matrix(machine)

    # define variables for evaluating
    x0 = z3.Int("x0")
    x1 = z3.Int("x1")
    x2 = z3.Int("x2")
    x3 = z3.Int("x3")
    x4 = z3.Int("x4")
    x5 = z3.Int("x5")
    x6 = z3.Int("x6")
    x7 = z3.Int("x7")
    x8 = z3.Int("x8")
    x9 = z3.Int("x9")
    x10 = z3.Int("x10")
    x11 = z3.Int("x11")
    x12 = z3.Int("x12")

    opt = z3.Optimize()

    # add equations
    for idx in range(0, machine['len']):
        opt.add(x0 * matrix[idx][0] + x1 * matrix[idx][1] + x2 * matrix[idx][2] + x3 * matrix[idx][3] + x4 * matrix[idx][4] + x5 * matrix[idx][5] + x6 * matrix[idx][6] + x7 * matrix[idx][7] + x8 * matrix[idx][8] + x9 * matrix[idx][9] + x10 * matrix[idx][10] + x11 * matrix[idx][11] + x12 * matrix[idx][12] == machine['joltage'][idx])

    # add non-negative constraints
    opt.add(x0 >= 0)
    opt.add(x1 >= 0)
    opt.add(x2 >= 0)
    opt.add(x3 >= 0)
    opt.add(x4 >= 0)
    opt.add(x5 >= 0)
    opt.add(x6 >= 0)
    opt.add(x7 >= 0)
    opt.add(x8 >= 0)
    opt.add(x9 >= 0)
    opt.add(x10 >= 0)
    opt.add(x11 >= 0)
    opt.add(x12 >= 0)

    # define kriterium
    opt.minimize(x0 + x1 + x2 + x3 + x4 + x5 + x6 + x7 + x8 + x9 + x10 + x11 + x12)

    # solve
    opt.check()
    model = opt.model()
    minval = model.evaluate(x0 + x1 + x2 + x3 + x4 + x5 + x6 + x7 + x8 + x9 + x10 + x11 + x12)

    return int(str(minval))


def main():
    """
    main
    """

    filename = get_args()
    data = read_data(filename)

    # part 1
    sums = 0
    for item in data:
        sums += dijkstra_part1(item)
    print(f"\nSolution part 1: {sums}")

    # part 2
    sums = 0
    for item in data:
        sums += z3_part2(item)

    print(f"Solution part 2: {sums}")


if __name__ == '__main__':
    main()

# EOF
