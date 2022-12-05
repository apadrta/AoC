#!/usr/bin/env python
# -*- coding:utf-8 -*-
"""
Advent of code 2022 - Day 5
"""

import argparse
import string

def get_args():
    """
    Cmd line argument parsing (preprocessing)
    """
    # Assign description to the help doc
    parser = argparse.ArgumentParser(
        description='Advent of code 2022: Day 5')

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


def process_data(data):
    """
    Process data
    """
    stacks = {}
    moves = []
    for line in data:
        line = line.replace('\n', '').replace('\r', '').replace('-', ',')
        if '[' in line:
            for idx, value in enumerate(line):
                if (idx+3) % 4 == 0 and value in string.ascii_uppercase:
                    if idx // 4 not in stacks:
                        stacks[idx // 4] = ''
                    stacks[idx // 4] += value  # top value = most left value
        elif 'move' in line:        
            moves.append([int(x) for x in line.replace('move ', '').replace('from ', '').replace('to ', '').split(' ')])
    return stacks, moves


def make_moves(stacks, moves):
    """
    Main function
    """
    for move in moves:
        for _ in range(0, move[0]):
            crate = stacks[move[1]-1][0]
            stacks[move[1]-1] = stacks[move[1]-1][1:]
            stacks[move[2]-1] = crate + stacks[move[2]-1]

    res = ''
    for idx in range(0, len(stacks)):
        res += stacks[idx][0]
    return res


def make_moves9001(stacks, moves):
    """
    Main function
    """
    for move in moves:
        crates = stacks[move[1]-1][:move[0]]
        stacks[move[1]-1] = stacks[move[1]-1][move[0]:]
        stacks[move[2]-1] = crates + stacks[move[2]-1]

    res = ''
    for idx in range(0, len(stacks)):
        res += stacks[idx][0]
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

    # evaluate part 1
    stacks, moves = process_data(data)
    res = make_moves(stacks, moves)
    print("Part 1 solution: {}".format(res))

    # evaluate part 2
    stacks, moves = process_data(data)
    res = make_moves9001(stacks, moves)
    print("Part 2 solution: {}".format(res))


if __name__ == '__main__':
    main()

# EOF
