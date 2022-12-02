#!/usr/bin/env python
# -*- coding:utf-8 -*-
"""
Advent of code 2022 - Day 2
"""

import argparse


def get_args():
    """
    Cmd line argument parsing (preprocessing)
    """
    # Assign description to the help doc
    parser = argparse.ArgumentParser(
        description='Advent of code 2022: Day 2')

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

    # define variables
    win = [
        ['A', 'Y'],  # rock vs. paper
        ['B', 'Z'],  # paper vs. scissors
        ['C', 'X']   # scissors vs. rock
    ]
    tie = [
        ['A', 'X'],
        ['B', 'Y'],
        ['C', 'Z']
    ]
    strategy = {
        'X': {'A': 'Z', 'B': 'X', 'C': 'Y'},  # lose
        'Y': {'A': 'X', 'B': 'Y', 'C': 'Z'},  # draw
        'Z': {'A': 'Y', 'B': 'Z', 'C': 'X'}   # win
    }
    trans = {
        'X': -1,
        'Y': 0,
        'Z': 1
    }

    # evaluate games
    games = []
    for line in data:
        symbols = line.replace('\n', '').replace('\r', '').split(' ')
        # evaluate result
        res = -1  # lost
        if symbols in win:
            res = +1
        elif symbols in tie:
            res = 0
        # complete data
        games.append(
            symbols +
            [res] +
            [trans[symbols[1]]] +
            [strategy[symbols[1]][symbols[0]]]
        )

    # compute score - symbol + result
    score = {
        'X': 1,
        'Y': 2,
        'Z': 3,
        1: 6,
        0: 3,
        -1: 0,
    }
    total_score = 0
    for game in games:
        total_score += score[game[1]] + score[game[2]]

    print("Part 1 solution: {}".format(total_score))

    total_score = 0
    for game in games:
        total_score += score[game[3]] + score[game[4]]

    print("Part 2 solution: {}".format(total_score))


if __name__ == '__main__':
    main()

# EOF
