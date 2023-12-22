#!/usr/bin/env python
# -*- coding:utf-8 -*-
"""
Advent of code 2023 - Day 22
"""

import argparse
from operator import itemgetter


def get_args():
    """
    Cmd line argument parsing (preprocessing)
    """
    # Assign description to the help doc
    parser = argparse.ArgumentParser(
        description='Advent of code 2023: Day 22'
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

    # create bricks
    bricks = []
    for line in data:
        points = line.split('~')
        bricks.append([[int(x) for x in points[0].split(',')], [int(x) for x in points[1].split(',')]])
        bricks[-1].append(min(bricks[-1][0][2], bricks[-1][1][2]))

    # sort according to the height above the ground
    bricks = sorted(bricks, key=itemgetter(2))

    return bricks


def intersect_square(block_a, block_b):
    """
    find if two squares intersetcs
    """
    this = [
        [min(block_a[0][0], block_a[1][0]), min(block_a[0][1], block_a[1][1])],
        [max(block_a[0][0], block_a[1][0]), max(block_a[0][1], block_a[1][1])]
        ]
    other = [
        [min(block_b[0][0], block_b[1][0]), min(block_b[0][1], block_b[1][1])],
        [max(block_b[0][0], block_b[1][0]), max(block_b[0][1], block_b[1][1])]
        ]
    if other[1][0] < this[0][0] or other[0][0] > this[1][0] or other[1][1] < this[0][1] or other[0][1] > this[1][1]:
        return False
    return True


def fall_bricks(bricks):
    """
    compute brick falling
    """
    # initialize
    last_level = bricks[0][1][2] - bricks[0][0][2] + 1
    max_level = last_level
    store = {last_level: [0]}
    supports = []
    is_supported = []
    for idx in range(0, len(bricks)):
        supports.append([])
        is_supported.append([])

    # process brick falling + compute dependencies
    for idx, brick in enumerate(bricks[1:]):
        act_level = max_level + 1
        while act_level > 0:
            hit = 0
            if act_level not in store:
                store[act_level] = []
            for item in store[act_level]:
                if intersect_square([brick[0][0:2], brick[1][0:2]], [bricks[item][0][0:2], bricks[item][1][0:2]]):
                    hit += 1
                    supports[item].append(idx+1)
                    is_supported[idx+1].append(item)
            if hit > 0:
                break
            act_level -= 1
        last_level = act_level + (brick[1][2] - brick[0][2] + 1)
        if last_level not in store:
            store[last_level] = []
        store[last_level].append(idx + 1)
        if last_level > max_level:
            max_level = last_level

    # evaluate destructables
    sums = 0
    for idx in range(len(bricks)):
        destructable = 1
        for support in is_supported:
            if len(support) == 1 and idx in support:
                destructable = 0
                break
        sums += destructable

    return sums, supports, is_supported


def chain_reactions(supports, is_supported):
    """
    compute chain reactions
    """
    sums = 0
    for idx in range(len(supports)):
        out = []
        destruct = [idx]
        while destruct:
            work = destruct.pop()
            out.append(work)
            for candidate in supports[work]:
                stable = False
                for support in is_supported[candidate]:
                    if support not in out:
                        stable = True
                        break
                if not stable:
                    if candidate not in destruct:
                        destruct.append(candidate)
        sums += len(out) - 1
    return sums


def main():
    """
    Main function
    """

    # process args
    infile = get_args()

    # read data
    data = read_data_struct(infile)

    # part 1
    count, supports, is_supported = fall_bricks(data)
    print(f"Part 1 solution : {count}")

    # part 2
    count = chain_reactions(supports, is_supported)
    print(f"Part 2 solution: {count}")


if __name__ == '__main__':
    main()

# EOF
