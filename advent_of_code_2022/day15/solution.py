#!/usr/bin/env python
# -*- coding:utf-8 -*-
"""
Advent of code 2022 - Day 15
"""

import argparse


def get_args():
    """
    Cmd line argument parsing (preprocessing)
    """
    # Assign description to the help doc
    parser = argparse.ArgumentParser(
        description='Advent of code 2022: Day 15')

    # Add arguments
    parser.add_argument(
        '-i',
        '--infile',
        type=str,
        help='Inputfilename',
        required=True)
    parser.add_argument(
        '-l',
        '--lineindex',
        type=int,
        help='Target line index',
        required=True)

    # Array for all arguments passed to script
    args = parser.parse_args()

    # Return arg variables
    return args.infile, args.lineindex


def parse_input(lines):
    """
    Preprocess input
    """
    data = []
    for line in lines:
        parts = line.split(' ')
        data.append([
            int(parts[2].replace('x=', '').replace(',', '')),
            int(parts[3].replace('y=', '').replace(':', '')),
            int(parts[8].replace('x=', '').replace(',', '')),
            int(parts[9].replace('y=', '').replace(':', ''))
        ])
    return data


def linecoverage(item, lineindex):
    """
    get limits for given line covered by signal
    """
    dist = abs(item[0] - item[2]) + abs(item[1] - item[3])
    var = dist - abs(item[1] - lineindex)
    if var < 0:
        return None
    return item[0] - var, item[0] + var


def concat_intervals(int_a, int_b):
    """
    concat intervals
    """
    # no intersection
    if int_a[0] > int_b[1] + 1:
        return [int_a, int_b]
    if int_a[1] + 1 < int_b[0]:
        return [int_a, int_b]
    # some kind of intersection
    mini = min(int_a[0], int_a[1], int_b[0], int_b[1])
    maxi = max(int_a[0], int_a[1], int_b[0], int_b[1])
    return [(mini, maxi)]


def solve_part1(data, lineindex):
    """
    solve part one
    """
    # get limits
    limits = []
    for item in data:
        limit = linecoverage(item, lineindex)
        if limit:
            limits.append(limit)
    # compute intersections
    for _ in range(len(limits)):
        goals = [limits[0]]
        for value in limits[1:]:
            change = False
            for idx, goal in enumerate(goals):
                res = concat_intervals(goal, value)
                if len(res) == 1:
                    change = True
                    goals[idx] = res[0]
                    break
            if not change:
                goals.append(value)
        limits = goals
        goal = goals[0]
    # sum ranges
    sums = 0
    for goal in goals:
        sums += goal[1] - goal[0] + 1
    # substract detected beacons
    known_beacons = []
    for item in data:
        if item[3] == lineindex:
            for goal in goals:
                if goal[0] <= item[2] <= goal[1] and (item[2], item[3]) not in known_beacons:
                    sums -= 1
                    known_beacons.append((item[2], item[3]))
                    break
    return sums


def search4bacon(data, lineindex, maxlimit):
    """
    solve part one
    """
    # get limits
    limits = []
    for item in data:
        limit = linecoverage(item, lineindex)
        if limit:
            if limit[0] < 0:
                limit = (0, limit[1])
            if limit[1] > maxlimit:
                limit = (limit[0], maxlimit)
            limits.append(limit)
    # compute intersections
    for _ in range(len(limits)):
        goals = [limits[0]]
        for value in limits[1:]:
            change = False
            for idx, goal in enumerate(goals):
                res = concat_intervals(goal, value)
                if len(res) == 1:
                    change = True
                    goals[idx] = res[0]
                    break
            if not change:
                goals.append(value)
        limits = goals
        goal = goals[0]
    # sum ranges
    if len(goals) == 1:
        if goals[0][0] == 0 and goals[0][1] == maxlimit:
            return None
        if goals[0][0] > 0:
            return goals[0][0]
        if goals[0][1] < maxlimit:
            return goals[0][1]
    return min(goals[0][1] + 1, goals[1][1] + 1)


def solve_part2(data, limit):
    """
    solve second day
    """
    idx = 0
    while idx <= limit:
        res = search4bacon(data, idx, limit)
        if res:
            return res * 4000000 + idx
        idx += 1
        if idx % 25000 == 0:
            print('.', flush=True, end='')
        if idx > limit:
            break
    return 0


def main():
    """
    Main function
    """

    # process args
    infile, lineindex = get_args()

    # read data
    data = []
    with open(infile, "r") as fileh:
        data = fileh.readlines()
    lines = [x.strip() for x in data]

    # preprocess data
    data = parse_input(lines)

    # part 1
    res = solve_part1(data, lineindex)
    print(f"Part 1 solution: {res}")

    # part 2
    res = solve_part2(data, 2 * lineindex)
    print(f"\nPart 2 solution: {res}")


if __name__ == '__main__':
    main()

# EOF
