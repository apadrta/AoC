#!/usr/bin/env python
# -*- coding:utf-8 -*-
"""
Advent of code 2019 - Day 20
"""

import argparse
from string import ascii_uppercase
from copy import deepcopy
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
        if step % 100 == 0:
            print('.', end='', flush=True)
        for idx in range(0, 4):
            new_pos = (state[0] + moves[idx][0], state[1] + moves[idx][1])
            # checking end
            if new_pos == end and (arr[new_pos] == -2 or arr[new_pos] > arr[state] + 1):
                arr[new_pos] = arr[state] + 1
                return arr[end]
            # checking direct move
            if arr[new_pos] == -1 or arr[new_pos] > arr[state] + 1:
                arr[new_pos] = arr[state] + 1
                process.append(new_pos)
            # checking portal move
            if arr[new_pos] == -2 and (arr[portals[new_pos]] == -2 or arr[portals[new_pos]] > arr[state] + 1):
                arr[portals[new_pos]] = arr[state] + 2
                process.append(portals[new_pos])
    return arr[end]


def make_templates(arr, portals, start, end):
    """
    Prepare templates for 2nd part
    """
    points = []
    for key, value in portals.items():
        if key not in points:
            points.append(key)
        if value not in points:
            points.append(value)
    yhalf = arr.shape[0] // 2
    xhalf = arr.shape[1] // 2
    positions = {}   # +1 = inner link, -1 outer link
    for point in points:
        if arr[point[0] + 1, point[1]] == 0 and point[0] < yhalf:
            positions[point] = 1
        elif arr[point[0] - 1, point[1]] == 0 and point[0] > yhalf:
            positions[point] = 1
        elif arr[point[0], point[1] + 1] == 0 and point[1] < xhalf:
            positions[point] = 1
        elif arr[point[0], point[1] - 1] == 0 and point[1] > xhalf:
            positions[point] = 1
        else:
            positions[point] = -1
    # prepare template for outer layer
    # (blind outer portals)
    t_out = deepcopy(arr)
    for point in points:
        if positions[point] == -1:
            t_out[point] = -8
    # prepare template for inner layers
    # (blind start and end positions)
    t_in = deepcopy(arr)
    t_in[start] = -8
    t_in[end] = -8

    return t_out, t_in, positions


def shortest_path_multilayer(out_tmp, in_tmp, portals, outinpos, start, end):
    """
    find shortest path in multilayer maze
    """
    # initialize
    arrays = []
    arrays.append(deepcopy(out_tmp))
    arrays[0][start] = 0
    process = [{'pos': start, 'depth': 0}]
    step = 0
    # start processing
    while process:
        step += 1
        state = process.pop(0)
        if step % 10000 == 0:
            print('.', end='', flush=True)
        for idx in range(0, 4):
            new_pos = (state['pos'][0] + moves[idx][0], state['pos'][1] + moves[idx][1])
            # checking end
            if state['depth'] == 0 and new_pos == end and (arrays[state['depth']][new_pos] == -2 or arrays[state['depth']][new_pos] > arrays[state['depth']][state['pos']] + 1):
                arrays[state['depth']][new_pos] = arrays[state['depth']][state['pos']] + 1
                return arrays[0][end]
            # checking direct move
            if arrays[state['depth']][new_pos] == -1 or arrays[state['depth']][new_pos] > arrays[state['depth']][state['pos']] + 1:
                arrays[state['depth']][new_pos] = arrays[state['depth']][state['pos']] + 1
                process.append({'pos': new_pos, 'depth': state['depth']})
            # checking portal move
            if arrays[state['depth']][new_pos] == -2:
                new_depth = state['depth'] + outinpos[new_pos]
                if len(arrays) - 1 < new_depth:
                    arrays.append(deepcopy(in_tmp))
                if (arrays[new_depth][portals[new_pos]] == -2 or arrays[new_depth][portals[new_pos]] > arrays[state['depth']][state['pos']] + 1):
                    arrays[new_depth][portals[new_pos]] = arrays[state['depth']][state['pos']] + 2
                process.append({'pos': portals[new_pos], 'depth': new_depth})
    return arrays[0][end]


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

    # part 1
    arr, portals, start, end = parse_data(lines)
    res = shortest_path(arr, portals, start, end)
    print(f"\nPart 1 solution: {res}")

    # part 2
    arr, portals, start, end = parse_data(lines)
    template_out, template_inner, outinpos = make_templates(arr, portals, start, end)
    res = shortest_path_multilayer(template_out, template_inner, portals, outinpos, start, end)
    print(f"\nPart 2 solution: {res}")


if __name__ == '__main__':
    main()

# EOF
