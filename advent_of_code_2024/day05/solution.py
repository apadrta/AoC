#!/usr/bin/env python
# -*- coding:utf-8 -*-
"""
Advent of code 2024 - Day 4
"""

import argparse


def get_args():
    """
    Cmd line argument parsing (preprocessing)
    """
    # Assign description to the help doc
    parser = argparse.ArgumentParser(
        description='Advent of code 2024: Day 5')

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
    rules = []
    updates = []
    for item in data:
        if "|" in item:
            rules.append([int(x) for x in item.split('|')])
        elif "," in item:
            updates.append([int(x) for x in item.split(',')])
    # create list of numbers of interest
    nois = []
    for rule in rules:
        if rule[0] not in nois:
            nois.append(rule[0])
        if rule[1] not in nois:
            nois.append(rule[1])
    # preprocess rules
    ruledict = {}
    for rule in rules:
        if rule[0] not in ruledict:
            ruledict[rule[0]] = []
        ruledict[rule[0]].append(rule[1])
    return ruledict, updates, nois


def is_correct(rules, nois, update):
    """
    Check is update follows th rules
    """
    # preprocess update
    pagepos = {}
    for idx, page in enumerate(update):
        pagepos[page] = idx
    # check rules
    for page in update:
        if page not in nois:
            # no rules is applied on this
            continue
        if page not in rules:
            # only one page of the rule exists (it is pointless to check)
            continue
        for follower in rules[page]:
            # check if all followers have higer position
            if follower not in pagepos:
                continue
            if pagepos[page] > pagepos[follower]:
                return False
    return True


def order_update(rules, update):
    """
    Order update according to the rules
    """
    ordered = []
    while update:
        restricted = []
        for rule, conds in rules.items():
            if rule in update:
                for cond in conds:
                    if cond in update:
                        restricted.append(cond)
        for page in update:
            if page not in restricted:
                ordered.append(page)
                update.remove(page)
    return ordered


def main():
    """
    Main function
    """

    # process args
    infile = get_args()

    # read data
    rules, updates, nois = read_data(infile)

    # part 1
    sums = 0
    for update in updates:
        if is_correct(rules, nois, update):
            sums += update[len(update) // 2]
    print(f"Part 1 solution: {sums}")

    # part 2
    sums = 0
    for update in updates:
        if not is_correct(rules, nois, update):
            ordered = order_update(rules, update)
            print(ordered)
            sums += ordered[len(ordered) // 2]
    print(f"Part 2 solution: {sums}")


if __name__ == '__main__':
    main()

# EOF
