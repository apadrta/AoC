#!/usr/bin/env python
# -*- coding:utf-8 -*-
"""
Advent of code 2022 - Day 24
"""

import argparse
# import numpy as np


def get_args():
    """
    Cmd line argument parsing (preprocessing)
    """
    # Assign description to the help doc
    parser = argparse.ArgumentParser(
        description='Advent of code 2022: Day 24')

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
    blizzs_pos = []
    blizzs_dir = []
    for idx, line in enumerate(lines[1:-1]):
        for jdx, point in enumerate(line[1:-1]):
            direction = None
            if point == '>':
                direction = (0, 1)
            elif point == '<':
                direction = (0, -1)
            elif point == '^':
                direction = (-1, 0)
            elif point == 'v':
                direction = (1, 0)
            if direction:
                blizzs_pos.append([idx, jdx])
                blizzs_dir.append(direction)
    return blizzs_pos, blizzs_dir, (len(lines)-2, len(lines[0])-2)


moves = [
    [0, 0],
    [1, 0],
    [-1, 0],
    [0, 1],
    [0, -1],
]


def solve_part1(bpos, bdir, size, start, end):
    """
    simulate blizzard dodging
    """
    step = 0
    elfs = [start]

    while True:
        step += 1
        # move blizzards
        for idx, _ in enumerate(bpos):
            bpos[idx][0] = (bpos[idx][0] + bdir[idx][0]) % size[0]
            bpos[idx][1] = (bpos[idx][1] + bdir[idx][1]) % size[1]
        # get possible moves
        new_elfs = []
        for elf in elfs:
            for move in moves:
                pmove = [elf[0] + move[0], elf[1] + move[1]]
                if pmove == end:
                    return step, bpos
                if pmove == start and pmove not in new_elfs:
                    new_elfs.append(pmove)
                elif pmove[0] < 0 or pmove[0] >= size[0] or pmove[1] < 0 or pmove[1] >= size[1]:
                    continue
                elif pmove not in bpos and pmove not in new_elfs:
                    new_elfs.append(pmove)
        elfs = new_elfs
        if step % 10 == 0:
            print('.', end='', flush=True)
    return 0


def solve_part2(bpos, bdir, size, prevres):
    """
    simulate blizzard dodging there, back and there again
    """
    sums = prevres
#    res, bpos = solve_part1(bpos, bdir, size, [-1, 0], [size[0], size[1] -1])
#    print(f'1st path = {res}')
#    sums += res
    res, bpos = solve_part1(bpos, bdir, size, [size[0], size[1] - 1], [-1, 0])
    sums += res
    res, bpos = solve_part1(bpos, bdir, size, [-1, 0], [size[0], size[1] - 1])
    sums += res
    return sums


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
    bpos, bdir, size = parse_input(lines)

    # part 1
    res, bpos = solve_part1(bpos, bdir, size, [-1, 0], [size[0], size[1] - 1])
    print(f"\nPart 1 solution: {res}")

    # part 2
#    bpos, bdir, size = parse_input(lines)
    res2 = solve_part2(bpos, bdir, size, res)
    print(f"\nPart 2 solution: {res2}")


if __name__ == '__main__':
    main()

# EOF
