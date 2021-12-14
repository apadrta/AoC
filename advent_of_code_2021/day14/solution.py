#!/usr/bin/env python
# -*- coding:utf-8 -*-
"""
Advent of code 2021 - Day 14
"""

import argparse


def get_args():
    """
    Cmd line argument parsing (preprocessing)
    """
    # Assign description to the help doc
    parser = argparse.ArgumentParser(
        description='Advent of code 2021: Day 14')

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


def polymerize(basic_formula, rules, steps):
    """
    Create submarine polymer (linked list)
    """
    formula = []
    i = 0
    for part in basic_formula:
        i += 1
        formula.append([part, i])
    formula[-1][1] = -1

    i = 0
    while i < steps:
        j = 0
        while formula[j][1] != -1:
            nextj = formula[j][1]
            for rule in rules:
                if rule[0][0] == formula[j][0] and rule[0][1] == formula[formula[j][1]][0]:
                    formula.append([rule[1], formula[j][1]])
                    formula[j][1] = len(formula) - 1
                    break
            j = nextj
        i += 1
    return formula


def polymerize_superoptimal(basic_formula, rules, steps):
    """
    Create submarine polymer (statistical data only)
    """
    formula = {}
    i = 0
    while i < len(basic_formula) - 1:
        if basic_formula[i:i+2] not in formula:
            formula[basic_formula[i:i+2]] = 0
        formula[basic_formula[i:i+2]] += 1
        i += 1

    i = 0
    while i < steps:
        i += 1
        news = {}
        for key, value in formula.items():
            for rule in rules:
                if rule[0] == key:
                    if key[0] + rule[1] not in news:
                        news[key[0] + rule[1]] = 0
                    if rule[1] + key[1] not in news:
                        news[rule[1] + key[1]] = 0
                    news[key[0] + rule[1]] += value
                    news[rule[1] + key[1]] += value
                    formula[key] = 0
                    break
        formula = news
    return formula


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

    basic_formula = lines[0]
    rules = []
    for line in lines[2:]:
        rules.append(line.split(" -> "))

    # part 1
    formula = polymerize(basic_formula, rules, 10)

    counts = {}
    j = 0
    while j != -1:
        if formula[j][0] not in counts:
            counts[formula[j][0]] = 0
        counts[formula[j][0]] += 1
        j = formula[j][1]
    print(f"Part 1 solution: {max(counts.values()) - min(counts.values())}")

    # part 2
    formula = polymerize_superoptimal(basic_formula, rules, 40)
    counts = {}
    for key, value in formula.items():
        for char in key:
            if char not in counts:
                counts[char] = 0
            counts[char] += value
    print(f"Part 2 solution: {(max(counts.values()) - min(counts.values()))//2 + 1}")


if __name__ == '__main__':
    main()

# EOF
