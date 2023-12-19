#!/usr/bin/env python
# -*- coding:utf-8 -*-
"""
Advent of code 2023 - Day 19
"""

import argparse
import re
from copy import deepcopy


def get_args():
    """
    Cmd line argument parsing (preprocessing)
    """
    # Assign description to the help doc
    parser = argparse.ArgumentParser(
        description='Advent of code 2023: Day 19'
        )

    # Add arguments
    parser.add_argument(
        '-i',
        '--infile',
        type=str,
        help='Inputfilename',
        required=True
        )

    # Array for all arguments passed to script
    args = parser.parse_args()

    # Return arg variables
    return args.infile


def read_data_struct(filename):
    """
    Read data from file and convert it to data structure
    """
    data = []
    with open(filename, "r", encoding="utf-8") as fileh:
        data = fileh.readlines()
    data = [x.strip() for x in data]

    rules = {}
    parts = []

    for line in data:
        if not line:
            continue
        if line[0] == '{':
            # parts
            items = line[1:-1].split(',')
            part = {}
            for item in items:
                details = item.split('=')
                part[details[0]] = int(details[1])
            parts.append(part)
        else:
            # rules
            name, details = line.split('{')
            items = details[:-1].split(',')
            rule = []
            for item in items:
                details = item.split(':')
                if len(details) == 1:
                    rule.append([True, details[0]])
                    continue
                maths = re.split('>|<', details[0])
                sign = '<'
                if '>' in details[0]:
                    sign = '>'
                rule.append([[maths[0], sign, int(maths[1])], details[1]])
            rules[name] = rule
    return rules, parts


def eval_part(rules, part):
    """
    Evaluate part accorring to rules
    """
    flow = 'in'
    while True:
        for rule in rules[flow]:
            if rule[0] is True:
                flow = rule[1]
                break
            if rule[0][0] in part:
                if rule[0][1] == '>':
                    if part[rule[0][0]] > rule[0][2]:
                        flow = rule[1]
                        break
                else:
                    if part[rule[0][0]] < rule[0][2]:
                        flow = rule[1]
                        break
        if flow == 'R':
            return 0
        if flow == 'A':
            vals = 0
            for value in part.values():
                vals += value
            return vals
    return 0


def count_possible(rules):
    """
    count possible combinations
    """
    possible = {'x': [1, 4000], 'm': [1, 4000], 'a': [1, 4000], 's': [1, 4000]}
    flow = 'in'
    buff = [[flow, possible]]
    accepted = []
    while buff:
        work = buff.pop(0)
        for rule in rules[work[0]]:
            new_state = deepcopy(work)
            new_state[0] = rule[1]
            if rule[0] is not True and rule[0][0] in new_state[1]:
                if rule[0][1] == '<':
                    new_state[1][rule[0][0]][1] = min(new_state[1][rule[0][0]][1], rule[0][2] - 1)
                    work[1][rule[0][0]][0] = max(new_state[1][rule[0][0]][0], rule[0][2])
                else:
                    new_state[1][rule[0][0]][0] = max(new_state[1][rule[0][0]][0], rule[0][2] + 1)
                    work[1][rule[0][0]][1] = min(new_state[1][rule[0][0]][1], rule[0][2])
            if new_state[0] == 'R':
                continue
            if new_state[0] == 'A':
                accepted.append(new_state[1])
                continue
            buff.append(new_state)
    sums = 0
    for acc in accepted:
        val = 1
        for item in acc.values():
            val *= item[1] - item[0] + 1
        sums += val
    return sums


def main():
    """
    Main function
    """

    # process args
    infile = get_args()

    # read data
    rules, parts = read_data_struct(infile)

    sums = 0
    for part in parts:
        sums += eval_part(rules, part)
    print(f"Part 1 solution: {sums}")

    # part 2
    count = count_possible(rules)
    print(f"Part 2 solution: {count}")


if __name__ == '__main__':
    main()

# EOF
