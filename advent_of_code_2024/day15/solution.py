#!/usr/bin/env python
# -*- coding:utf-8 -*-
"""
Advent of code 2024 - Day 15
"""

import argparse


vector = {
    0: [-1, 0],
    1: [1, 0],
    2: [0, -1],
    3: [0, 1],
}


def get_args():
    """
    Cmd line argument parsing (preprocessing)
    """
    # Assign description to the help doc
    parser = argparse.ArgumentParser(
        description='Advent of code 2024: Day 15')

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
    # parse data
    mapdata = {"pos": [0, 0], "crates": [], "walls": []}
    instructions = []
    for idx, line in enumerate(data):
        if not line:
            continue
        if line[0] == "#":
            for jdx, item in enumerate(line):
                if item == "#":
                    mapdata["walls"].append([idx, jdx])
                elif item == "O":
                    mapdata["crates"].append([idx, jdx])
                elif item == "@":
                    mapdata["pos"] = [idx, jdx]
        else:
            for item in line:
                if item == "^":
                    instructions.append(0)
                elif item == "v":
                    instructions.append(1)
                elif item == "<":
                    instructions.append(2)
                elif item == ">":
                    instructions.append(3)
    return mapdata, instructions


def moveit(mapdata, moves):
    """
    Move robot according to instruction in map
    """
    train = [mapdata["pos"]]
    idx = 0
    traindirection = moves[idx]
    while idx < len(moves):
        move = moves[idx]
        # check direction change (keep just robot position)
        if move != traindirection:
            for item in train[1:]:
                mapdata["crates"].append(item)
            train = [train[0]]
            traindirection = move
        # check tile in front of first part of train
        new = [train[-1][0] + vector[move][0], train[-1][1] + vector[move][1]]
        if new in mapdata["walls"]:
            # no move posssible
            idx += 1
            continue
        if new in mapdata["crates"]:
            # add new crate to the train (no move)
            mapdata["crates"].remove(new)
            train.append(new)
            continue
        # move
        for jdx, item in enumerate(train):
            train[jdx] = [item[0] + vector[move][0], item[1] + vector[move][1]]
        idx += 1
    for item in train[1:]:
        mapdata["crates"].append(item)
    mapdata["pos"] = train[0]
    return mapdata


def moveitmoveit(mapdata, moves):
    """
    Move robot according to instruction in map
    """
    train = [[mapdata["pos"]]]
    idx = 0
    traindirection = moves[idx]
    while idx < len(moves):
        move = moves[idx]
        # check direction change (keep just robot position)
        if move != traindirection:
            for level in train[1:]:
                for item in level:
                    mapdata["crates"].append(item)
            train = [train[0]]
            traindirection = move
        # check tiles in front of first level of train
        news = []
        for kdx, level in enumerate(train):
            for item in level:
                if kdx == 0:
                    # robot only
                    news.append([item[0] + vector[move][0], item[1] + vector[move][1]])
                else:
                    # crates
                    if traindirection in [0, 1]:
                        # up/down
                        news.append([item[0] + vector[move][0], item[1] + vector[move][1]])
                        news.append([item[0] + vector[move][0], item[1] + vector[move][1] + 1])
                    elif traindirection == 2:
                        # left
                        news.append([item[0] + vector[move][0], item[1] + vector[move][1]])
                    else:
                        # right
                        news.append([item[0] + vector[move][0], item[1] + vector[move][1] + 1])
        hitwall = False
        for new in news:
            if new in mapdata["walls"]:
                hitwall = True
                break
        if hitwall:
            # no move posssible
            idx += 1
            continue
        new_crates = []
        for new in news:
            if new in mapdata["crates"]:
                new_crates.append(new)
                mapdata["crates"].remove(new)
                continue
            if [new[0], new[1] - 1] in mapdata["crates"]:
                new_crates.append([new[0], new[1] - 1])
                mapdata["crates"].remove([new[0], new[1] - 1])
        if new_crates:
            # add new crate to the train (no move)
            train.append(new_crates)
            continue
        # move
        new_train = []
        for level in train:
            new_level = []
            for item in level:
                new_level.append([item[0] + vector[move][0], item[1] + vector[move][1]])
            new_train.append(new_level)
        train = new_train
        idx += 1
    for level in train[1:]:
        for item in level:
            mapdata["crates"].append(item)
    mapdata["pos"] = train[0][0]
    return mapdata


def doublemap(mapdata):
    """
    Double map according to rules for 2nd part
    """
    # udpate robot position
    mapdata["pos"] = [mapdata["pos"][0], mapdata["pos"][1]*2]
    # update walls position
    walls = []
    for wall in mapdata["walls"]:
        walls.append([wall[0], wall[1] * 2])
        walls.append([wall[0], wall[1] * 2+1])
    mapdata["walls"] = walls
    # update crates position
    crates = []
    for crate in mapdata["crates"]:
        crates.append([crate[0], crate[1] * 2])
    mapdata["crates"] = crates
    return mapdata


def print_doublemap(mapdata):
    """
    Print map (debug)
    """
    size = [0, 0]
    for item in mapdata["walls"]:
        if item[0] > size[0]:
            size[0] = item[0]
        if item[1] > size[1]:
            size[1] = item[1]
    for i in range(0, size[0] + 1):
        print(f"{i:03d} ", end='')
        for j in range(0, size[1] + 1):
            if [i, j] == mapdata["pos"]:
                print("@", end='')
                continue
            if [i, j] in mapdata["walls"]:
                print("#", end='')
                continue
            if [i, j] in mapdata["crates"]:
                print("[]", end='')
                continue
            if [i, j - 1] in mapdata["crates"]:
                continue
            print(".", end='')
        print("")


def eval_crates(crates):
    """
    Evaluate crate
    """
    sums = 0
    for crate in crates:
        sums += 100 * crate[0] + crate[1]
    return sums


def main():
    """
    Main function
    """

    # process args
    infile = get_args()

    # read data
    mapdata, moves = read_data(infile)

    # part 1
    mapmoved = moveit(mapdata, moves)
    sums = eval_crates(mapmoved["crates"])
    print(f"Part 1 solution: {sums}")

    # part 2
    mapdata, moves = read_data(infile)
    mapdata = doublemap(mapdata)
    mapmoved = moveitmoveit(mapdata, moves)
    print_doublemap(mapdata)
    sums = eval_crates(mapmoved["crates"])
    print(f"Part 2 solution: {sums}")


if __name__ == '__main__':
    main()

# EOF
