#!/usr/bin/env python
# -*- coding:utf-8 -*-
"""
Advent of code 2022 - Day 21
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
        description='Advent of code 2022: Day 21')

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
    monkeys = []
    for line in lines:
        mname, action = line.split(': ')
        if ' ' not in action:
            monkeys.append([mname, [int(action)]])
        else:
            monkeys.append([mname, action.split(' ')])
    return monkeys


def solve_part1(monkeys, root):
    """
    evaluate monkeys
    """
    known = {}
    process = []
    # extract known leaves
    for monkey in monkeys:
        if len(monkey[1]) == 1:
            known[monkey[0]] = monkey[1][0]
        else:
            process.append(monkey)
    # process other
    while True:
        change = False
        # check root
        if root in known:
            return known[root]
        # replace known
        for monkey in process:
            if monkey[1][0] in known:
                monkey[1][0] = known[monkey[1][0]]
            if monkey[1][2] in known:
                monkey[1][2] = known[monkey[1][2]]
        # evaluate possible
        unknown = []
        for monkey in process:
            if not isinstance(monkey[1][0], int) or not isinstance(monkey[1][2], int):
                unknown.append(monkey)
                continue
            change = True
            if monkey[1][1] == '-':
                known[monkey[0]] = monkey[1][0] - monkey[1][2]
            if monkey[1][1] == '/':
                known[monkey[0]] = monkey[1][0] // monkey[1][2]
            if monkey[1][1] == '*':
                known[monkey[0]] = monkey[1][0] * monkey[1][2]
            if monkey[1][1] == '+':
                known[monkey[0]] = monkey[1][0] + monkey[1][2]
        process = unknown
        if not change:
            return None
    return 0


def solve_part2(monkeys):
    """
    determine what to yell
    """
    # modify input data
    root = 0
    humn = 0
    for idx, monkey in enumerate(monkeys):
        if monkey[0] == 'root':
            root = idx
        if monkey[0] == 'humn':
            humn = idx
    monkeys[humn][0] = '????'
    # initialize searching data
    data = deepcopy(monkeys)
    left = solve_part1(data, monkeys[root][1][0])
    data = deepcopy(monkeys)
    right = solve_part1(data, monkeys[root][1][2])
    if left:
        mvalue = left
        mname = monkeys[root][1][2]
    else:
        mvalue = right
        mname = monkeys[root][1][0]
    while True:
        # find in which part is unknown value and tree result
        procmonkey = None
        for monkey in monkeys:
            if monkey[0] == mname:
                procmonkey = monkey
                break
        data = deepcopy(monkeys)
        left = solve_part1(data, procmonkey[1][0])
        data = deepcopy(monkeys)
        right = solve_part1(data, procmonkey[1][2])
        # get unknown value
        data = deepcopy(monkeys)
        if left:
            # unknown right value
            mname = procmonkey[1][2]
            if procmonkey[1][1] == '-':
                mvalue = left - mvalue
            if procmonkey[1][1] == '/':
                mvalue = left // mvalue
            if procmonkey[1][1] == '*':
                mvalue = mvalue // left
            if procmonkey[1][1] == '+':
                mvalue = mvalue - left
        else:
            # unknown left value
            mname = procmonkey[1][0]
            if procmonkey[1][1] == '-':
                mvalue = mvalue + right
            if procmonkey[1][1] == '/':
                mvalue = mvalue * right
            if procmonkey[1][1] == '*':
                mvalue = mvalue // right
            if procmonkey[1][1] == '+':
                mvalue = mvalue - right
        if mname == 'humn':
            return mvalue

    return 0


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
    data = parse_input(lines)
    res = solve_part1(data, 'root')
    print(f"Part 1 solution: {res}")

    # part 2
    data = parse_input(lines)
    res = solve_part2(data)
    print(f"Part 2 solution: {res}")


if __name__ == '__main__':
    main()

# EOF
