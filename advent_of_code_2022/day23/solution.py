#!/usr/bin/env python
# -*- coding:utf-8 -*-
"""
Advent of code 2022 - Day 23
"""

import argparse


def get_args():
    """
    Cmd line argument parsing (preprocessing)
    """
    # Assign description to the help doc
    parser = argparse.ArgumentParser(
        description='Advent of code 2022: Day 23')

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
    elves = []
    for idx, line in enumerate(lines):
        for jdx, char in enumerate(line):
            if char == '#':
                elves.append([idx, jdx])
    return elves


moves = [
    [(-1, 0), (-1, -1), (-1, +1)],  # north
    [(+1, 0), (+1, -1), (+1, +1)],  # south
    [(0, -1), (+1, -1), (-1, -1)],  # west
    [(0, +1), (+1, +1), (-1, +1)]   # east
]

around = [
    [-1, -1],
    [-1, 0],
    [-1, +1],
    [0, +1],
    [+1, -1],
    [+1, 0],
    [+1, +1],
    [0, -1]
]


def solve_part1(elves):
    """
    simulate elf movements
    """
    for elfround in range(0, 10):
        new_elves = []
        elf_propositions = {}
        proposed_tiles = {}
        # first half
        for elf in elves:
            alone = True
            for tile in around:
                if [elf[0] + tile[0], elf[1] + tile[1]] in elves:
                    alone = False
                    break
            if alone:
                new_elves.append(elf)
            else:
                proposed = None
                for kdx in range(0, 4):
                    move = moves[(kdx + elfround) % len(moves)]
                    free = True
                    for item in move:
                        if [elf[0] + item[0], elf[1] + item[1]] in elves:
                            free = False
                            break
                    if free:
                        proposed = [elf[0] + move[0][0], elf[1] + move[0][1]]
                        break
                if proposed:
                    elf_propositions[tuple(elf)] = proposed
                    if tuple(proposed) not in proposed_tiles:
                        proposed_tiles[tuple(proposed)] = 0
                    proposed_tiles[tuple(proposed)] += 1
                else:
                    new_elves.append(elf)
        # second half
        for elf, proposal in elf_propositions.items():
            if proposed_tiles[tuple(proposal)] == 1:
                new_elves.append(proposal)
            else:
                new_elves.append(list(elf))
        elves = new_elves
        print('.', end='', flush=True)
    # count result
    minrow = 0
    maxrow = 0
    mincol = 0
    maxcol = 0
    for elf in elves:
        if elf[0] < minrow:
            minrow = elf[0]
        if elf[0] > maxrow:
            maxrow = elf[0]
        if elf[1] < mincol:
            mincol = elf[1]
        if elf[1] > maxcol:
            maxcol = elf[1]
    return (maxrow - minrow + 1) * (maxcol - mincol + 1) - len(elves)


def solve_part2(elves):
    """
    simulate elfs movements
    """
    elfround = 0
    move = True
    while move:
        move = False
        new_elves = []
        elf_propositions = {}
        proposed_tiles = {}
        # first half
        for elf in elves:
            alone = True
            for tile in around:
                if [elf[0] + tile[0], elf[1] + tile[1]] in elves:
                    alone = False
                    break
            if alone:
                new_elves.append(elf)
            else:
                proposed = None
                for kdx in range(0, 4):
                    move = moves[(kdx + elfround) % len(moves)]
                    free = True
                    for item in move:
                        if [elf[0] + item[0], elf[1] + item[1]] in elves:
                            free = False
                            break
                    if free:
                        proposed = [elf[0] + move[0][0], elf[1] + move[0][1]]
                        break
                if proposed:
                    elf_propositions[tuple(elf)] = proposed
                    if tuple(proposed) not in proposed_tiles:
                        proposed_tiles[tuple(proposed)] = 0
                    proposed_tiles[tuple(proposed)] += 1
                else:
                    new_elves.append(elf)
        # second half
        for elf, proposal in elf_propositions.items():
            if proposed_tiles[tuple(proposal)] == 1:
                move = True
                new_elves.append(proposal)
            else:
                new_elves.append(list(elf))
        elves = new_elves
        elfround += 1
        print('.', end='', flush=True)
    return elfround


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
    res = solve_part1(data)
    print(f"\nPart 1 solution: {res}")

    # part 2
    data = parse_input(lines)
    res = solve_part2(data)
    print(f"\nPart 2 solution: {res}")


if __name__ == '__main__':
    main()

# EOF
