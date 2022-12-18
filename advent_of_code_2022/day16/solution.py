#!/usr/bin/env python
# -*- coding:utf-8 -*-
"""
Advent of code 2022 - Day 16
"""

import argparse
from copy import deepcopy
import numpy as np
from dijkstar import Graph, find_path


def get_args():
    """
    Cmd line argument parsing (preprocessing)
    """
    # Assign description to the help doc
    parser = argparse.ArgumentParser(
        description='Advent of code 2022: Day 16')

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


def solve_part1(arr, valves_i, rates_i, start, maxtime):
    """
    find maximal possible flow with one man
    """
    # initialize
    maxrate = 0
    closed_valves = []
    for key, value in rates_i.items():
        if value > 0:
            closed_valves.append(key)
        maxrate += value

    init_state = [valves_i[start], 0, 0, 0, closed_valves]
    # 0 position
    # 1 time elapsed
    # 2 summ of released pressure
    # 3 pressure_change per minute
    # 4 list of still closed valves)

    toprocess = [init_state]
    step = 0
    finalmax = 0
    while toprocess:
        # process state
        pstate = toprocess.pop(0)
        # transition to new state - wait when all wents are opened
        if pstate[3] == maxrate:
            newstate = deepcopy(pstate)
            newstate[2] += newstate[3] * (maxtime - newstate[1])
            newstate[1] = maxtime
            # newstates.append(newstate)
            if newstate[2] > finalmax:
                finalmax = newstate[2]
        # transition to new state - try to move through tunnel(s) + open valve
        for target in pstate[4]:
            # create new state
            if pstate[1] + arr[(pstate[0], target)] + 1 >= maxtime:
                addflow = pstate[3]*(maxtime-pstate[1])
                released = pstate[2] + addflow
                if released > finalmax:
                    finalmax = released
                continue
            newstate = deepcopy(pstate)
            newstate[0] = target                  # change position (move)
            newstate[1] += arr[(pstate[0], target)] + 1  # inc time (move+open)
            newstate[2] += newstate[3] * (arr[(pstate[0], target)] + 1)  # release pressure
            newstate[3] += rates_i[newstate[0]]   # increase total flow by current valve flow
            newstate[4].remove(newstate[0])       # open valve (remove from closed)
            # add new state
            toprocess.append(newstate)

        step += 1
        if step % 1000 == 0:
            print('.', end='', flush=True)
    return finalmax


def solve_part2(arr, valves_i, rates_i, start, maxtime):
    """
    find maximal possible flow with one man and one elephant
    """
    # initialize
    # initialize
    maxrate = 0
    closed_valves = []
    for key, value in rates_i.items():
        if value > 0:
            closed_valves.append(key)
        maxrate += value
    init_state = [valves_i[start], 0, 0, 0, closed_valves, valves_i[start], 0, 0]
    # 0 man position / target position
    # 1 time elapsed
    # 2 summ of released pressure
    # 3 pressure_change per minute
    # 4 list of still closed valves
    # 5 elephant position / target position
    # 6 time to reach goal for man (0 means in goal)
    # 7 time to reach goal for elephant (0 means in goal)
    toprocess = [init_state]
    step = 0
    finalmax = 0
    currmax = 0
    minutemax = [0] * maxtime
    while toprocess:
        # process state
        pstate = toprocess.pop(0)
        if pstate[2] > currmax:
            currmax = pstate[2]

        # move man/elephant on their route
        movetime = min(pstate[6], pstate[7])
        if movetime > 0:
            # move towards targets
            pstate[6] -= movetime
            pstate[7] -= movetime
            # increase released pressure
            pstate[2] += pstate[3] * movetime
            # increase time
            pstate[1] += movetime
            # man open his valve
            if pstate[6] == 0 and pstate[0] in pstate[4]:
                pstate[3] += rates_i[pstate[0]]    # increase total flow by current valve flow
                pstate[4].remove(pstate[0])      # open valve (remove from closed)
            # elephant open his valve
            if pstate[7] == 0 and pstate[5] in pstate[4]:
                pstate[3] += rates_i[pstate[5]]    # increase total flow by current valve flow
                pstate[4].remove(pstate[5])      # open valve (remove from closed)

            # check end of processing - maxrate is reached
            if pstate[3] == maxrate:
                new_time = pstate[2] + pstate[3] * (maxtime - pstate[1])
                if new_time > finalmax:
                    finalmax = new_time
                continue
            # check end of processing - maxtimereached
            if pstate[1] >= maxtime:
                new_time = pstate[2] + pstate[3] * (maxtime - pstate[1])
                if new_time > finalmax:
                    finalmax = new_time
                continue
            # add to queue for next processin
            toprocess.append(pstate)
            if pstate[2] > minutemax[pstate[1]]:
                minutemax[pstate[1]] = pstate[2]
            continue

        # route man/elephant somewhere (move and open valve)
        for midx in pstate[4]:
            mtarget = midx
            mtime = arr[(pstate[0], mtarget)] + 1
            # if en route, route stays
            if pstate[6] > 0:
                mtarget = pstate[0]
                mtime = pstate[6]
            for eidx in pstate[4]:
                etarget = eidx
                etime = arr[(pstate[5], etarget)] + 1
                # if en route, route stays
                if pstate[7] > 0:
                    etarget = pstate[5]
                    etime = pstate[7]
                # elephant cannot choose valve already targeted by man
                if pstate[7] == 0 and etarget == mtarget:
                    continue
                newstate = deepcopy(pstate)
                # retouting man
                newstate[0] = mtarget
                newstate[6] = mtime
                # retouting elephant
                newstate[5] = etarget
                newstate[7] = etime
                # add new state
                add = True
                if newstate[1] > 0 and newstate[2] + rates_i[newstate[0]] + rates_i[newstate[5]] < minutemax[newstate[1] - 1]:
                    add = False
                if add:
                    toprocess.append(newstate)
                if newstate[2] > minutemax[newstate[1]]:
                    minutemax[newstate[1]] = newstate[2]
                # end inner cycle if inner is not changing
                if pstate[7] > 0:
                    break
            # do not repeat outer cycle if outer is not changing
            if pstate[6] > 0:
                break

        step += 1
        if step % 1000 == 0:
            print('.', end='', flush=True)
    return finalmax


def parse_input1(lines):
    """
    Preprocess input
    """
    # parse data
    valves = []
    valves_i = {}
    trans = {}
    rates = {}
    for idx, line in enumerate(lines):
        parts = line.split(' ', 9)
        valve = parts[1]
        valves_i[valve] = idx
        rate = parts[4].replace(';', '').split('=')[1]
        targets = parts[-1].split(', ')
        rates[idx] = int(rate)
        trans[valve] = []
        for target in targets:
            trans[valve].append(target)
        valves.append(valve)

    # compute direct paths
    graph = Graph()
    for source in valves:
        for target in trans[source]:
            graph.add_edge(valves_i[source], valves_i[target], 1)

    arr = np.zeros((len(valves), len(valves)), dtype=int)
    for idx, _ in enumerate(valves):
        for jdx, _ in enumerate(valves):
            arr[(idx, jdx)] = find_path(graph, idx, jdx).total_cost

    return arr, valves_i, rates


def parse_input2(lines):
    """
    Preprocess input
    """
    # parse data
    valves = []
    trans = {}
    rates = {}
    for idx, line in enumerate(lines):
        parts = line.split(' ', 9)
        valve = parts[1]
        rate = parts[4].replace(';', '').split('=')[1]
        targets = parts[-1].split(', ')
        rates[idx] = int(rate)
        trans[valve] = []
        for target in targets:
            trans[valve].append(target)
        valves.append(valve)
    return valves, rates, trans


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

    # part 1
    arr, valves_i, rates = parse_input1(lines)
    res = solve_part1(arr, valves_i, rates, 'AA', 30)
    print(f"\nPart 1 solution: {res}")

    # part 2
    res = solve_part2(arr, valves_i, rates, 'AA', 26)
    print(f"\nPart 2 solution: {res}")


if __name__ == '__main__':
    main()

# EOF
