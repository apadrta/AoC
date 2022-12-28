#!/usr/bin/env python
# -*- coding:utf-8 -*-
"""
Advent of code 2019 - Day 18
"""


import argparse
from copy import deepcopy
import numpy as np

def get_args():
    """
    Cmd line argument parsing (preprocessing)
    """
    # Assign description to the help doc
    parser = argparse.ArgumentParser(
        description='Advent of code 2019 - Day 18')

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


def print_floor(floor):
    """
    print floor in human readable form
    """
    for idx in range(np.size(floor, 0)):
        for jdx in range(np.size(floor, 1)):
            print(chr(floor[(idx, jdx)]), end='')
        print('\n', end='')


def find_poi(floor):
    """
    Find points of interest
    """
    entrance = []
    keys = {}
    doors = {}
    for i in range(np.size(floor, 0)):
        for j in range(np.size(floor, 1)):
            if floor[(i, j)] == ord('@'):
                entrance.append((i, j))
            elif chr(floor[(i, j)]).islower():
                keys[chr(floor[(i, j)])] = (i, j)
            elif chr(floor[(i, j)]).isupper():
                doors[chr(floor[(i, j)])] = (i, j)
    return entrance, keys, doors


border_diffs = [(-1, 0), (1, 0), (0, -1), (0, 1)]
entrance_diffs = [(-1, -1), (-1, 1), (1, -1), (1, 1)]


def find_dist_map(floor, poi):
    """
    Get distances from POI to other accesible POI
    """
    dist_map = {}
    for name, point in poi.items():
        # count distances
        distances = np.full((np.size(floor, 0), np.size(floor, 1)), -1, dtype=int)
        check = [point]
        distances[point] = 0
        while check:
            act = check.pop()
            for diff in border_diffs:
                if (act[0] == 0 and diff[0] == -1) or (act[0] == np.size(floor, 0) - 1 and diff[0] == 1):
                    # out of map
                    continue
                if (act[1] == 0 and diff[1] == -1) or (act[1] == np.size(floor, 1) - 1 and diff[1] == 1):
                    # out of map
                    continue
                check_pos = (act[0] + diff[0], act[1] + diff[1])
                if floor[check_pos] == 35:
                    # tile is wall
                    continue
                if distances[check_pos] == -1 or distances[check_pos] > distances[act] + 1:
                    # tile is not explored / can be accessed by shorter path
                    distances[check_pos] = distances[act] + 1
                    if floor[check_pos] == 46:
                        # tile is empty or orginal starting position or key -> explore surrounding tiles in next step
                        check.append(check_pos)
        # add info to distance map
        dist_map[name] = {}
        for target_name, target_point in poi.items():
            if distances[target_point] > 0:
                dist_map[name][target_name] = distances[target_point]
    return dist_map


def solution_part1(dist_map, nkeys):
    """
    solve part1
    """

    min_dest = None
    for key in dist_map:
        if key != '@':
            # process only starting position
            continue
        dests = [[[key], 0, []]]
        hist = {}
        step = 0
        prune = 0
        while dests:
            state = dests.pop()
            step += 1
            if step % 10000 == 0:
                print('.', end='', flush=True)
            for target, dist in dist_map[state[0][-1]].items():
                if target.isupper() and target.lower() not in state[0]:
                    # no key for processed door
                    continue
                # create new state
                newstate = deepcopy(state)
                newstate[0].append(target)
                newstate[1] += dist
                if target.islower() and target not in newstate[2]:
                    newstate[2].append(target)
                    newstate[2].sort()
                # prune inperspective - based on already known solution
                if min_dest and newstate[1] >= min_dest:
                    prune += 1
                    continue
                # prune inperspective - based on already seen progress
                if newstate[0][-1] in hist and tuple(newstate[2]) in hist[newstate[0][-1]] and hist[newstate[0][-1]][tuple(newstate[2])] <= newstate[1]:
                    prune += 1
                    continue
                # prune inperspective - based on same state scheduled
                delete = False
                for check in dests:
                    if check[0][-1] == newstate[0][-1] and check[2] == newstate[2] and check[1] <= newstate[1]:
                        delete = True
                if delete:
                    prune += 1
                    continue
                # add state to process
                dests.append(newstate)
                # evaluate end
                if len(newstate[2]) == nkeys:
                    if not min_dest or newstate[1] < min_dest:
                        min_dest = newstate[1]
                # update prunning structure
                if newstate[0][-1] not in hist:
                    hist[newstate[0][-1]] = {}
                if tuple(newstate[2]) not in hist[newstate[0][-1]]:
                    hist[newstate[0][-1]][tuple(newstate[2])] = newstate[1]
                elif hist[newstate[0][-1]][tuple(newstate[2])] > newstate[1]:
                    hist[newstate[0][-1]][tuple(newstate[2])] = newstate[1]
        break
    return min_dest


def mod_floor(floor, entrance):
    """
    modify floor according to 2nd part definition
    """
    entrances = {}
    floor[(entrance)] = ord('#')
    for diff in border_diffs:
        floor[(entrance[0] + diff[0], entrance[1] + diff[1])] = ord('#')
    for idx, diff in enumerate(entrance_diffs):
        floor[(entrance[0] + diff[0], entrance[1] + diff[1])] = 48 + idx
        entrances[str(idx)] = (entrance[0] + diff[0], entrance[1] + diff[1])
    return floor, entrances


def make_optimoves(state, dist_map):
    """
    make optimal moves (cannot be done better)
    """
    change = True
    while change:
        change = False
        for idx in range(0, 4):
            pos_targets = 0
            optkey = None
            optval = None
            for key, value in dist_map[state[idx]].items():
                if key not in state[6]:
                    pos_targets += 1
                    optkey = key
                    optval = value
            if pos_targets != 1:
                continue
            if optkey.islower() and optkey not in state[5]:
                state[6].append(state[idx])
                state[idx] = optkey
                state[4] += optval
                state[5].append(optkey)
                state[5].sort()
                change = True
    return state


def solution_part2(dist_map, entrances, nkeys):
    """
    solve part1
    """

    min_dest = None
    init_state = [
        entrances[0],
        entrances[1],
        entrances[2],
        entrances[3],
        0,
        [],
        []
    ]
    init_state = make_optimoves(init_state, dist_map)
    dests = [init_state]
    hist = {}
    step = 0
    prune = 0
    while dests:
        state = dests.pop(0)
        step += 1
        if step % 5000 == 0:
            print('.', end='', flush=True)
        # evaluate possible moves
        targeting = []
        for idx in range(0, len(entrances)):
            for target, dist in dist_map[state[idx]].items():
                if target.isupper() and target.lower() not in state[5]:
                    # no key for processed door
                    continue
                if target.islower() and target in state[6]:
                    # do not return to banned states
                    continue
                targeting.append([idx, state[idx], target, dist])
        # process new states for possible moves
        for target in targeting:
            # create new state
            newstate = deepcopy(state)
            newstate[target[0]] = target[2]
            newstate[4] += target[3]
            if target[2].islower() and target[2] not in newstate[5]:
                newstate[5].append(target[2])
                newstate[5].sort()
            # prune inperspective - based on already known solution
            if min_dest and newstate[4] >= min_dest:
                prune += 1
                continue
            # prune inperspective - based on already seen progress
            prunekey = tuple([newstate[0], newstate[1], newstate[2], newstate[3]])
            if prunekey in hist and tuple(newstate[5]) in hist[prunekey] and hist[prunekey][tuple(newstate[5])] <= newstate[4]:
                prune += 1
                continue
            # add state to process
            dests.append(newstate)
            # evaluate end
            if len(newstate[5]) == nkeys:
                if not min_dest or newstate[4] < min_dest:
                    min_dest = newstate[4]
            # update prunning structure
            prunekey = tuple([newstate[0], newstate[1], newstate[2], newstate[3]])
            if prunekey not in hist:
                hist[prunekey] = {}
            if tuple(newstate[5]) not in hist[prunekey]:
                hist[prunekey][tuple(newstate[5])] = newstate[4]
            elif hist[prunekey][tuple(newstate[5])] > newstate[4]:
                hist[prunekey][tuple(newstate[5])] = newstate[4]
    return min_dest


def remove_node(min_dest, node):
    """
    detect node from min-dest structure
    """
    del min_dest[node]
    for values in min_dest.values():
        if node in values:
            del values[node]
    return min_dest


def detect_trash_nodes(min_dest):
    """
    detect trash nodes
    """
    change = True
    while change:
        change = False
        # detect doors-leafs
        keys2del = []
        for key, value in min_dest.items():
            if key.isupper() and len(value) == 1:
                keys2del.append(key)
                change = True
        # remove doors-leafs
        for delkey in keys2del:
            min_dest = remove_node(min_dest, delkey)
        if change:
            continue
        # detect unnecesary two-links doors
        keys2del = []
        for key, value in min_dest.items():
            if key.isupper() and len(value) == 2:
                ends = list(value.keys())
                if ends[1] in min_dest[ends[0]] and min_dest[ends[0]][ends[1]] <= sum(value.values()):
                    keys2del.append(key)
                    change = True
        # remove unnecesary two-links doors
        for delkey in keys2del:
            min_dest = remove_node(min_dest, delkey)
        if change:
            continue
        # detect unnecesary three-links doors
        keys2del = []
        for key, value in min_dest.items():
            if key.isupper() and len(value) == 3:
                lens = list(value.values())
                ends = list(value.keys())
                delete = True
                for idx in range(0, 3):
                    end_a = ends[(idx + 1) % 3]
                    end_b = ends[(idx - 1) % 3]
                    len_a = lens[(idx + 1) % 3]
                    len_b = lens[(idx - 1) % 3]
                    if end_a not in min_dest[end_b] or min_dest[end_b][end_a] > len_a + len_b:
                        delete = False
                        break
                if delete:
                    keys2del.append(key)
                    change = True
        # remove unnecesary three-links doors
        for delkey in keys2del:
            min_dest = remove_node(min_dest, delkey)
        if change:
            continue

    return min_dest


def main():
    """
    Main function
    """

    # process args
    filename = get_args()

    # prepare data for further processing
    data = []
    with open(filename, "r") as fileh:
        data = fileh.readlines()
    lines = [x.strip() for x in data]

    # convert to numpy array
    floor = np.zeros((len(lines), len(lines[0])), dtype=int)
    i = 0
    for line in lines:
        j = 0
        for char in line:
            floor[(i, j)] = ord(char)
            j += 1
        i += 1

    # part 1
    entrances, keys_pos, doors_pos = find_poi(floor)
    poi = keys_pos | doors_pos | {'@': entrances[0]}
    dist_map = find_dist_map(floor, poi)
    dist_map = detect_trash_nodes(dist_map)
    res = solution_part1(dist_map, len(keys_pos))
    print(f"\nSolution of part 1: {res}")

    # part 2
    entrances, keys_pos, doors_pos = find_poi(floor)
    floor, entrances = mod_floor(floor, entrances[0])
    poi = keys_pos | doors_pos | entrances
    dist_map = find_dist_map(floor, poi)
    dist_map = detect_trash_nodes(dist_map)

    res = solution_part2(dist_map, list(entrances.keys()), len(keys_pos))
    print(f"\nSolution of part 2: {res}")


if __name__ == '__main__':
    main()

# EOF
