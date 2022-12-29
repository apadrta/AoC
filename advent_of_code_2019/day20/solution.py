#!/usr/bin/env python
# -*- coding:utf-8 -*-
"""
Advent of code 2019 - Day 20
"""

import argparse
from string import ascii_uppercase
import numpy as np


def get_args():
    """
    Cmd line argument parsing (preprocessing)
    """
    # Assign description to the help doc
    parser = argparse.ArgumentParser(
        description='Advent of code 2019: Day 20')

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


def parse_data(lines):
    """
    parse data
    """
    arr = np.zeros((len(lines), len(lines[0])), dtype=int)
    portals = []
    for idx, line in enumerate(lines):
        for jdx, point in enumerate(line):
            # walls
            if point == '#':
                arr[idx, jdx] = -8
            # coridors
            elif point == '.':
                arr[idx, jdx] = -1
            # detect vertical portals
            elif point in ascii_uppercase and idx < len(lines) - 1 and lines[idx+1][jdx] in ascii_uppercase:
                portal_name = f'{point}{lines[idx+1][jdx]}'
                portal_pos = None
                if idx > 0 and lines[idx-1][jdx] == '.':
                    portal_pos = (idx-1, jdx)
                elif idx < len(lines) - 1 and lines[idx+2][jdx] == '.':
                    portal_pos = (idx + 2, jdx)
                portals.append([portal_name, portal_pos])
            # detect horizontal portals
            elif point in ascii_uppercase and jdx < len(lines[0]) - 1 and lines[idx][jdx+1] in ascii_uppercase:
                portal_name = f'{point}{lines[idx][jdx+1]}'
                portal_pos = None
                if jdx > 0 and lines[idx][jdx-1] == '.':
                    portal_pos = (idx, jdx-1)
                elif jdx < len(lines[0]) - 1 and lines[idx][jdx+2] == '.':
                    portal_pos = (idx, jdx+2)
                portals.append([portal_name, portal_pos])

    # add portals to array
    for portal in portals:
        arr[portal[1]] = -2
    # process portals
    start = None
    end = None
    telepairs = {}
    for portal in portals:
        if portal[0] == 'AA':
            start = portal[1]
        elif portal[0] == 'ZZ':
            end = portal[1]
        elif portal[0] not in telepairs:
            telepairs[portal[0]] = [portal[1]]
        else:
            telepairs[portal[0]].append(portal[1])
    tunnels = {}
    for endpoints in telepairs.values():
        tunnels[endpoints[0]] = endpoints[1]
        tunnels[endpoints[1]] = endpoints[0]

    return arr, tunnels, start, end


moves = [
    [0, 1],
    [0, -1],
    [1, 0],
    [-1, 0]
]


def shortest_path(arr, portals, start, end):
    """
    find shortest path
    """
    arr[start] = 0
    process = [start]
    step = 0
    while process:
        step += 1
        state = process.pop(0)
        if step % 10 == 0:
            print('.', end='', flush=True)
        for idx in range(0, 4):
            new_pos = (state[0] + moves[idx][0], state[1] + moves[idx][1])
            # checking end
            if new_pos == end and (arr[new_pos] == -2 or arr[new_pos] > arr[state] + 1):
                arr[new_pos] = arr[state] + 1
                continue
            # checking direct move
            if arr[new_pos] == -1 or arr[new_pos] > arr[state] + 1:
                arr[new_pos] = arr[state] + 1
                process.append(new_pos)
            # checking portal move
            if arr[new_pos] == -2 and (arr[portals[new_pos]] == -2 or arr[portals[new_pos]] > arr[state] + 1):
                arr[portals[new_pos]] = arr[state] + 2
                process.append(portals[new_pos])
    return arr[end]


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
    arr, portals, start, end = parse_data(lines)
    res = shortest_path(arr, portals, start, end)
    print(f"\nPart 1 solution: {res}")


if __name__ == '__main__':
    main()

# EOF
