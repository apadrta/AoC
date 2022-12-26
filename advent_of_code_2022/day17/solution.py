#!/usr/bin/env python
# -*- coding:utf-8 -*-
"""
Advent of code 2022 - Day 17
"""

import argparse
import numpy as np


def get_args():
    """
    Cmd line argument parsing (preprocessing)
    """
    # Assign description to the help doc
    parser = argparse.ArgumentParser(
        description='Advent of code 2022: Day 17')

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
    # read data
    arr = [0] * len((lines[0]))
    for idx, value in enumerate(lines[0]):
        if value == '<':
            arr[idx] = -1
        else:
            arr[idx] = 1
    # add blocks definition
    blocks = []
    block = np.ones((1, 4), dtype=int)
    blocks.append(block)
    block = np.ones((3, 3), dtype=int)
    block[(0, 0)] = 0
    block[(2, 0)] = 0
    block[(0, 2)] = 0
    block[(2, 2)] = 0
    blocks.append(block)
    block = np.ones((3, 3), dtype=int)
    block[0:2, 0:2] = np.zeros((2, 2))
    blocks.append(block)
    block = np.ones((4, 1), dtype=int)
    blocks.append(block)
    block = np.ones((2, 2), dtype=int)
    blocks.append(block)
    # return values
    return arr, blocks


def optimize(wind, blocks, number):
    """
    simulate block falling
    """
    shaft = np.zeros((number * 4, 7), dtype=int)
    depth = number * 4
    height = depth
    step = 0
    windindex = 0
    cdet = {}
    while True:
        block = blocks[step % len(blocks)]
        size = block.shape
        # magic block materialization
        topheight = height - 3
        blockpos = [topheight - size[0], 2]
        if step % 100 == 0:
            print('.', end='', flush=True)
        # gather data for optimization
        if (step % len(blocks), windindex % len(wind)) not in cdet:
            cdet[(step % len(blocks), windindex % len(wind))] = []
        cdet[(step % len(blocks), windindex % len(wind))].append([step, depth - height])
        if len(cdet[(step % len(blocks), windindex % len(wind))]) > 2:
            break
        # block falling
        while True:
            # wind move
            winddelta = wind[windindex % len(wind)]
            if blockpos[1]+winddelta >= 0 and blockpos[1]+size[1]-1+winddelta < 7:
                shaftsection = shaft[blockpos[0]:blockpos[0] + size[0], blockpos[1] + winddelta:blockpos[1] + size[1] + winddelta]
                intersect = np.add(shaftsection, block)
                if 2 not in intersect:
                    blockpos[1] += winddelta
            windindex += 1
            # gravity move
            if blockpos[0] + size[0] == depth:
                # land on floor (no move)
                shaft[blockpos[0]:blockpos[0] + size[0], blockpos[1]:blockpos[1] + size[1]] += block
                height = depth - size[0]
                break
            shaftsection = shaft[blockpos[0] + 1:blockpos[0] + size[0] + 1, blockpos[1]:blockpos[1] + size[1]]
            intersect = np.add(shaftsection, block)
            if 2 in intersect:
                # land on other block(s) (no move)
                shaft[blockpos[0]:blockpos[0] + size[0], blockpos[1]:blockpos[1] + size[1]] += block
                if blockpos[0] < height:
                    height = blockpos[0]
                break
            # move on piece down
            blockpos[0] += 1
        step += 1
        if step > number - 1:
            break
    # evaluate optimization data
    rep_blocks = None
    rep_height = None
    base_data = {}
    for value in cdet.values():
        base_data[value[0][0]] = value[0][1]
        if len(value) > 1:
            new_blocks = value[1][0] - value[0][0]
            new_height = value[1][1] - value[0][1]
            if not rep_blocks:
                rep_blocks = new_blocks
                rep_height = new_height
            else:
                if rep_blocks > new_blocks:
                    rep_blocks = new_blocks
                if rep_height > new_height:
                    rep_height = new_height
    return base_data, rep_blocks, rep_height


def solve_part1(base_data, cycle_len, cycle_height, number):
    """
    simulate block falling
    """
    rep = number // cycle_len
    beg = number % cycle_len
    return rep*cycle_height + base_data[beg]


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
    data, blocks = parse_input(lines)
    base_data, cycle_len, cycle_height = optimize(data, blocks, 10000)
    res = solve_part1(base_data, cycle_len, cycle_height, 2022)
    print(f"\nPart 1 solution: {res}")

    # part 2
    res = solve_part1(base_data, cycle_len, cycle_height, 1000000000000)
    print(f"Part 2 solution: {res}")


if __name__ == '__main__':
    main()

# EOF
