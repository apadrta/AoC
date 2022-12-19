#!/usr/bin/env python
# -*- coding:utf-8 -*-
"""
Advent of code 2022 - Day 19
"""

import argparse
from copy import deepcopy
# import numpy as np


def get_args():
    """
    Cmd line argument parsing (preprocessing)
    """
    # Assign description to the help doc
    parser = argparse.ArgumentParser(
        description='Advent of code 2022: Day 19')

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


def parse_input(lines):
    """
    Preprocess input
    """
    data = {}
    for idx, line in enumerate(lines):
        data[idx+1] = [int(x) for x in line.split(' ') if x.isdigit()]
    return data


maxbuilds_cumulative = {
    0: 0,
    1: 1,
    2: 4,
    3: 10,
    4: 20,
    5: 35,
    6: 56,
    7: 84,
    8: 120,
    9: 165,
    10: 220,
    11: 286,
    12: 364,
    13: 455,
    14: 560,
    15: 680,
    16: 816,
    17: 969,
    18: 1140,
    19: 1330,
    20: 1540,
    21: 1771,
    22: 2024,
    23: 2300,
    24: 2600,
    25: 2925,
    26: 3276,
    27: 3654,
    28: 4060,
    29: 4495,
    30: 4960,
    31: 5456,
    32: 5984
}


def eval_blueprint(blueprint, minutes):
    """
    evaluate blueprint efectivity for given time
    """
    # blue print definition
    # 0 ore per ore fact
    # 1 ore per clay fact
    # 2 ore per obsidian fact
    # 3 clay per obsidian fact
    # 4 ore per geode robot
    # 5 obsidian per geode robot
    factoryres = [
        [blueprint[0], 0, 0, 0],
        [blueprint[1], 0, 0, 0],
        [blueprint[2], blueprint[3], 0, 0],
        [blueprint[4], 0, blueprint[5], 0]
    ]  # ore, clay, obsidian, geode
    maxconsumption = [0, 0, 0, 0]
    for idx in range(0, 4):
        for jdx in range(0, 4):
            if factoryres[jdx][idx] > maxconsumption[idx]:
                maxconsumption[idx] = factoryres[jdx][idx]
    # simulate
    init_state1 = {'time': 0, 'store': [0, 0, 0, 0], 'facts': [1, 0, 0, 0], 'target': 0}
    init_state2 = {'time': 0, 'store': [0, 0, 0, 0], 'facts': [1, 0, 0, 0], 'target': 1}

    toprocess = [init_state1, init_state2]
    step = 0
    maxmined = 0
    discarded = 0
    first_geo = [0] * (minutes+1)
    while toprocess:
        step += 1
        proc = toprocess.pop()
        if step % 50000 == 0:
            print('.', end='', flush=True)
        # discard states worse than already reached
        if proc['store'][3] + maxbuilds_cumulative[minutes-proc["time"]] + proc['facts'][3] * (minutes-proc["time"]) < maxmined:
            # even if geod opening factory is builded each turn, result will not be better
            discarded += 1
            continue
        # if  proc['facts'][0] > maxconsumption[0] and proc['facts'][1] > maxconsumption[1] and proc['facts'][2] > maxconsumption[2]:
        if proc['facts'][0] > maxconsumption[0]:
            discarded += 1
            continue
        if proc['store'][3] + 2 < first_geo[proc['time']]:
            discarded += 1
            continue
        # check end of simulation
        if proc['time'] == minutes:
            if proc['store'][3] > maxmined:
                maxmined = proc['store'][3]
            continue
        # check if target factory building is possible
        build_possible = True
        for idx in range(0, 4):
            if proc['store'][idx] < factoryres[proc['target']][idx]:
                build_possible = False
                break
        # mine resources
        proc['time'] += 1
        for idx in range(0, 4):
            proc['store'][idx] += proc['facts'][idx]
        if proc['store'][3] > first_geo[proc['time']]:
            first_geo[proc['time']] = proc['store'][3]

        # if not enough resources, continue gathering
        if not build_possible:
            toprocess.append(proc)
            continue
        # build target factory
        proc['facts'][proc['target']] += 1
        for idx in range(0, 4):
            proc['store'][idx] -= factoryres[proc['target']][idx]
        # decide what to build next time
        for idx in range(0, 4):
            if idx == 2 and proc['facts'][1] == 0:
                break
            if idx == 3 and proc['facts'][2] == 0:
                break
            newproc = deepcopy(proc)
            newproc['target'] = idx
            toprocess.append(newproc)
    return maxmined


def solve_part1(blueprints, minutes):
    """
    evaluate blueprint
    """
    sums = 0
    for blue_id, blueprint in blueprints.items():
        sums += blue_id * eval_blueprint(blueprint, minutes)
    return sums


def solve_part2(blueprints, minutes):
    """
    run first three blueprints
    """
    res = 1
    for blue_id, blueprint in blueprints.items():
        if blue_id > 3:
            continue
        val = eval_blueprint(blueprint, minutes)
        res *= val
    return res


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
    lines = [x.strip() for x in data]

    # preprocess data
    data = parse_input(lines)

    # part 1
    res = solve_part1(data, 24)
    print(f"\nPart 1 solution: {res}")

    # part 2
    res = solve_part2(data, 32)
    print(f"\nPart 2 solution: {res}")


if __name__ == '__main__':
    main()

# EOF
