#!/usr/bin/env python
# -*- coding:utf-8 -*-
"""
Advent of code 2024 - Day 6
"""

import argparse


def get_args():
    """
    Cmd line argument parsing (preprocessing)
    """
    # Assign description to the help doc
    parser = argparse.ArgumentParser(
        description='Advent of code 2024: Day 6')

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
    # create basic rules and list of updates
    position = []
    obstacles = []
    for idx, row in enumerate(data):
        for jdx, col in enumerate(row):
            if col == "#":
                obstacles.append([idx, jdx])
            elif col == "^":
                position = [idx, jdx]
    return {"size": [len(data), len(data[0])], 'guard': position, 'obstacles': obstacles}


def path_to_out(data):
    """
    Count visited tiles on path to out
    """
    act = [data["guard"][0], data["guard"][1]]
    directions = [(-1, 0), (0, 1), (1, 0), (0, -1)]
    direction = 0
    visited = []
    loopcheck = []
    loop = False
    while True:
        # check out
        if act[0] < 0 or act[0] >= data["size"][0]:
            loop = False
            break
        if act[1] < 0 or act[1] >= data["size"][1]:
            loop = False
            break
        if [act, direction] in loopcheck:
            loop = True
            break
        loopcheck.append([act, direction])
        if act not in visited:
            visited.append(act)
        # get next tile
        nexttile = [act[0] + directions[direction][0], act[1] + directions[direction][1]]
        if nexttile in data["obstacles"]:
            # turn right
            direction = (direction + 1) % 4
        else:
            # move
            act = nexttile
    return visited, loop


def add_obstacle(data, visited):
    """
    Try to add obstacle
    """
    loops = 0
    for idx, newone in enumerate(visited):
        if newone == data["guard"]:
            continue
        print(f"{idx}.", end='', flush=True)
        [_, loop] = path_to_out({"size": data["size"], "guard": data["guard"], "obstacles": data["obstacles"] + [newone]})
        if loop:
            loops += 1
    return loops


def main():
    """
    Main function
    """

    # process args
    infile = get_args()

    # read data
    data = read_data(infile)

    # part 1
    [visited, _] = path_to_out(data)
    sums = len(visited)
    print(f"Part 1 solution: {sums}")

    # part 2
    sums = add_obstacle(data, visited)
    print(f"\nPart 2 solution: {sums}")


if __name__ == '__main__':
    main()

# EOF
