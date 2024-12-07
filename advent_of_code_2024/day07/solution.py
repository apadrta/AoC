#!/usr/bin/env python
# -*- coding:utf-8 -*-
"""
Advent of code 2024 - Day 7
"""

import argparse


def get_args():
    """
    Cmd line argument parsing (preprocessing)
    """
    # Assign description to the help doc
    parser = argparse.ArgumentParser(
        description='Advent of code 2024: Day 7')

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
    results = []
    terms = []
    for item in data:
        [res, nums] = item.split(': ')
        results.append(int(res))
        terms.append([int(x) for x in nums.split(' ')])
    return results, terms


def check_equation(res, terms, operators):
    """
    Read and prepare data
    """
    states = [[terms[0], terms[1:]]]
    while states:
        act = states.pop()
        for operator in operators:
            # evaluate state
            if len(act[1]) == 0:
                if act[0] == res:
                    return True
                continue
            # process first term in queue
            val = act[0]
            if operator == "*":
                val = val * act[1][0]
            elif operator == "+":
                val = val + act[1][0]
            elif operator == "||":
                val = int(str(val) + str(act[1][0]))
            states.append([val, act[1][1:]])
    return False


def main():
    """
    Main function
    """

    # process args
    infile = get_args()

    # read data
    results, terms = read_data(infile)

    # part 1
    sums = 0
    for idx, result in enumerate(results):
        if check_equation(result, terms[idx], ["*", "+"]):
            sums += result
    print(f"Part 1 solution: {sums}")

    # part 2
    sums = 0
    for idx, result in enumerate(results):
        if check_equation(result, terms[idx], ["*", "+", "||"]):
            sums += result
    print(f"\nPart 2 solution: {sums}")


if __name__ == '__main__':
    main()

# EOF
