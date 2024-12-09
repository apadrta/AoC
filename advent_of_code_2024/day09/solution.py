#!/usr/bin/env python
# -*- coding:utf-8 -*-
"""
Advent of code 2024 - Day 9
"""

import argparse


def get_args():
    """
    Cmd line argument parsing (preprocessing)
    """
    # Assign description to the help doc
    parser = argparse.ArgumentParser(
        description='Advent of code 2024: Day 9')

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
    data = [int(x) for x in data[0]]
    return data


def count_checksum(data):
    """
    Degragment and count data
    """
    checksum = 0
    idx = 0   # disk position
    bdx = 0   # block processed from begin
    edx = len(data) - 1  # block processed from end
    blocks_num = 0
    blocks_val = 0
    free_space = -1
    endidx = sum(data[::2])
    while True:
        if not bdx % 2:
            jdx = 0
            while jdx < data[bdx]:
                checksum += idx * (bdx//2)
                jdx += 1
                idx += 1
                if idx == endidx:
                    return checksum
            bdx += 1
        else:
            if free_space == -1:
                free_space = data[bdx]
                continue
            if blocks_num == 0:
                blocks_num = data[edx]
                blocks_val = edx//2
                edx = edx - 2
                continue
            if free_space > 0:
                blocks_num = blocks_num - 1
                free_space = free_space - 1
                checksum += idx * blocks_val
                idx += 1
            else:
                free_space = -1
                bdx += 1
        if idx == endidx:
            return checksum
    return checksum


def count_checksum2(data):
    """
    Degragment and count data
    """
    # prepare block representation
    disk = []
    free_blocks = []
    blocks = []
    pos = 0
    for idx, value in enumerate(data):
        if idx % 2:
            disk += [-1]*value
            free_blocks.append({"pos": pos, "len": value})
        else:
            disk += [(idx//2)] * value
            blocks.append({"pos": pos, "len": value, "value": idx//2})
        pos += value

    # try to move blocks
    for block in blocks[::-1]:
        # find suitable free block
        moveto = -1
        for idx, free in enumerate(free_blocks):
            if free["len"] >= block["len"]:
                moveto = idx
                break
        # if possible, move block
        if moveto == -1:
            continue
        if block['pos'] <= free_blocks[moveto]["pos"]:
            continue
        idx = 0
        while idx < block["len"]:
            disk[free_blocks[moveto]["pos"] + idx] = block["value"]
            disk[block["pos"] + idx] = -1
            idx += 1
        if block["len"] == free_blocks[moveto]["len"]:
            free_blocks.remove(free_blocks[moveto])
        else:
            free_blocks[moveto]["pos"] += block["len"]
            free_blocks[moveto]["len"] -= block["len"]
    # make checksum
    checksum = 0
    for idx, value in enumerate(disk):
        if value == -1:
            continue
        checksum += idx * value

    return checksum


def main():
    """
    Main function
    """

    # process args
    infile = get_args()

    # read data
    data = read_data(infile)

    # part 1
    sums = count_checksum(data)
    print(f"Part 1 solution: {sums}")

    # part 2
    sums = count_checksum2(data)
    print(f"Part 2 solution: {sums}")


if __name__ == '__main__':
    main()

# EOF
