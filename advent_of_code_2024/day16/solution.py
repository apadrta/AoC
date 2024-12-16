#!/usr/bin/env python
# -*- coding:utf-8 -*-
"""
Advent of code 2024 - Day 16
"""

import argparse
import numpy as np

vector = {
    0: [-1, 0],
    1: [0, 1],
    2: [1, 0],
    3: [0, -1]
}


def get_args():
    """
    Cmd line argument parsing (preprocessing)
    """
    # Assign description to the help doc
    parser = argparse.ArgumentParser(
        description='Advent of code 2024: Day 16')

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
    array = np.array([[ord(char) for char in line] for line in data])
    return array


def get_pois(mapdata):
    """
    Extract points of interest
    """
    pois = {"start": [], "end": [], "crossroads": []}
    idx = 0
    while idx < mapdata.shape[0]:
        jdx = 0
        while jdx < mapdata.shape[1]:
            if mapdata[idx][jdx] == 83:
                pois["start"].append((idx, jdx))
            elif mapdata[idx][jdx] == 69:
                pois["end"].append((idx, jdx))
            elif mapdata[idx][jdx] == 46:
                paths = 0
                for vect in vector.values():
                    if mapdata[idx + vect[0]][jdx + vect[1]] == 46:
                        paths += 1
                if paths > 2:
                    pois["crossroads"].append((idx, jdx))
            jdx += 1
        idx += 1
    return pois


def get_target(mapdata, nodes, source, direction):
    """
    Get first POI on defined direction from given source
    """
    cost = 1
    length = 1
    act = [source[0] + vector[direction][0], source[1] + vector[direction][1]]
    while tuple(act) not in nodes:
        # go straight
        straight = [act[0] + vector[direction][0], act[1] + vector[direction][1]]
        if mapdata[straight[0]][straight[1]] != 35:
            act = straight
            cost += 1
            length += 1
            continue
        # turn left
        turn = [act[0] + vector[(direction - 1) % 4][0], act[1] + vector[(direction - 1) % 4][1]]
        if mapdata[turn[0]][turn[1]] != 35:
            act = turn
            cost += 1001
            length += 1
            direction = (direction - 1) % 4
            continue
        # turn right
        turn = [act[0] + vector[(direction + 1) % 4][0], act[1] + vector[(direction + 1) % 4][1]]
        if mapdata[turn[0]][turn[1]] != 35:
            act = turn
            cost += 1001
            length += 1
            direction = (direction + 1) % 4
            continue
        # dead end
        return None, None, None, None
    return tuple(act), direction, cost, length


def get_connections(mapdata, pois):
    """
    Get connections between pairs of pois
    """
    paths = {}
    nodes = pois["start"] + pois["end"] + pois["crossroads"]

    for source in nodes:
        for direction, vect in vector.items():
            if mapdata[source[0] + vect[0]][source[1] + vect[1]] == 35:
                continue
            target, targetdirection, cost, length = get_target(mapdata, nodes, source, direction)
            if target:
                if source not in paths:
                    paths[source] = {}
                if target not in paths[source] or cost < paths[source][target][0]:
                    paths[source][target] = [cost, direction, targetdirection, length]
    return paths


def find_min_path(start, end, conns):
    """
    Find path from start to end with min cost
    """
    state = {
        "pos": start,
        "direction": 1,  # facing east
        "cost": 0
    }
    visited = {}
    visited[start] = 0
    states = [state]
    while states:
        act = states.pop(0)
        for target, data in conns[act["pos"]].items():
            new = {}
            new["pos"] = target
            new["cost"] = act["cost"] + data[0]
            if act["direction"] != data[1]:
                new["cost"] += 1000
            new["direction"] = data[2]
            if new["pos"] not in visited or new["cost"] < visited[new["pos"]]:
                visited[new["pos"]] = new["cost"]
                states.append(new)
    if end in visited:
        return visited[end]
    return None


def find_min_path_points(start, end, conns, cost):
    """
    Find path from start to end with given cost
    """
    # find shortest path
    state = {
        "pos": start,
        "direction": 1,  # facing east
        "cost": 0,
        "len": 0,
        "history": []
    }
    visited = {}
    visited[start] = 0
    states = [state]
    finals = []
    while states:
        act = states.pop(0)
        for target, data in conns[act["pos"]].items():
            new = {}
            new["history"] = act["history"] + [act["pos"]]
            new["pos"] = target
            new["len"] = act["len"] + data[3]
            new["cost"] = act["cost"] + data[0]
            if act["direction"] != data[1]:
                new["cost"] += 1000
            new["direction"] = data[2]
            if new["pos"] == end and new["cost"] == cost:
                finals.append(new)
                continue
            if new["pos"] in act["history"]:
                continue
            if new["pos"] not in visited or new["cost"] - 1000 <= visited[new["pos"]]:
                visited[new["pos"]] = new["cost"]
                states.append(new)
    # count observatories
    parts = []
    ends = []
    length = 0
    for fin in finals:
        hist = fin["history"] + [fin["pos"]]
        idx = 1
        while idx < len(hist):
            src = hist[idx-1]
            dst = hist[idx]
            idx += 1
            val = conns[src][dst][3]
            if (src, dst) in parts:
                continue
            if dst in ends:
                parts.append((src, dst))
                length += val - 1
            else:
                parts.append((src, dst))
                ends.append(dst)
                length += val
    return length + 1


def main():
    """
    Main function
    """

    # process args
    infile = get_args()

    # read data
    mapdata = read_data(infile)
    pois = get_pois(mapdata)
    conns = get_connections(mapdata, pois)

    # part 1
    sums = find_min_path(pois["start"][0], pois["end"][0], conns)
    print(f"Part 1 solution: {sums}")

    # part 2
    sums2 = find_min_path_points(pois["start"][0], pois["end"][0], conns, sums)
    print(f"Part 2 solution: {sums2}")


if __name__ == '__main__':
    main()

# EOF
