#!/usr/bin/env python
# -*- coding:utf-8 -*-
"""
Advent of code 2023 - Day 15
"""

import argparse


def get_args():
    """
    Cmd line argument parsing (preprocessing)
    """
    # Assign description to the help doc
    parser = argparse.ArgumentParser(
        description='Advent of code 2023: Day 15'
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
    data = data[0].split(',')

    return data


def count_hash(item):
    """
    count elf hash
    """
    res = 0
    for char in item:
        res += ord(char)
        res = (res * 17) % 256
    return res


def init_boxes(data):
    """
    init elf light boxes
    """
    # initialize
    boxes = []
    lenses = []
    for idx in range(0, 256):
        boxes.append([])
        lenses.append({})
    # reorder according to the rules
    for item in data:
        boxid = 0
        idx = 0
        while item[idx].islower():
            boxid += ord(item[idx])
            boxid = (boxid * 17) % 256
            idx += 1
        label = item[0:idx]
        if item[idx] == '=':
            if label not in boxes[boxid]:
                boxes[boxid].append(label)
            lenses[boxid][label] = int(item[idx+1::])
        else:
            if label in boxes[boxid]:
                boxes[boxid].remove(label)
    # compute focusing power
    power = 0
    for boxid, box in enumerate(boxes):
        for idx, item in enumerate(box):
            power += (boxid + 1) * (idx + 1) * lenses[boxid][item]
    return power


def main():
    """
    Main function
    """

    # process args
    infile = get_args()

    # read data
    data = read_data_struct(infile)

    # part 1
    sums = 0
    for item in data:
        sums += count_hash(item)
    print(f"Part 1 solution: {sums}")

    # part 2
    sums = init_boxes(data)
    print(f"Part 2 solution: {sums}")


if __name__ == '__main__':
    main()

# EOF
