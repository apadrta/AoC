#!/usr/bin/env python
# -*- coding:utf-8 -*-
"""
Advent of code 2024 - Day 12
"""

import argparse


def get_args():
    """
    Cmd line argument parsing (preprocessing)
    """
    # Assign description to the help doc
    parser = argparse.ArgumentParser(
        description='Advent of code 2024: Day 12'
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
    return data


def split_objects(letters):
    """
    Split object
    """
    objs = []
    obj = [letters.pop(0)]
    while letters:
        target = -1
        for idx, letter in enumerate(letters):
            for item in obj:
                if abs(item[0] - letter[0]) == 1 and item[1] == letter[1]:
                    target = idx
                    break
                if abs(item[1] - letter[1]) == 1 and item[0] == letter[0]:
                    target = idx
                    break
            if target > -1:
                break
        if target > -1:
            obj.append(letters.pop(target))
        else:
            objs.append(obj)
            obj = [letters.pop(0)]
    if obj:
        objs.append(obj)
    return objs


def data2objects(data):
    """
    Extract objects from data
    """
    letters = {}
    for idx, line in enumerate(data):
        for jdx, char in enumerate(line):
            if char not in letters:
                letters[char] = []
            letters[char].append((idx, jdx))
    objs = []
    for value in letters.values():
        objs += split_objects(value)
    return objs


def eval_object(obj):
    """
    Eval object
    """
    neighbours = [(-1, 0), (1, 0), (0, -1), (0, 1)]
    border = 0
    parts = [{}, {}, {}, {}]
    for item in obj:
        for idx, diff in enumerate(neighbours):
            if (diff[0] + item[0], diff[1] + item[1]) not in obj:
                if idx in [0, 1]:
                    if item[0] not in parts[idx]:
                        parts[idx][item[0]] = []
                    parts[idx][item[0]].append(item[1])
                else:
                    if item[1] not in parts[idx]:
                        parts[idx][item[1]] = []
                    parts[idx][item[1]].append(item[0])
                border += 1
    sides = 0
    for levels in parts:
        for level in levels.values():
            work = sorted(level)
            sides += 1
            idx = 1
            while idx < len(work):
                if work[idx] - work[idx - 1] > 1:
                    sides += 1
                idx += 1
    return border * len(obj), sides * len(obj)


def main():
    """
    Main function
    """

    # process args
    infile = get_args()

    # read data
    data = read_data_struct(infile)
    objects = data2objects(data)

    # part 1
    sums = 0
    sums2 = 0
    for obj in objects:
        parts, sides = eval_object(obj)
        sums += parts
        sums2 += sides
    print(f"Part 1 solution: {sums}")

    # part 2
    print(f"Part 2 solution: {sums2}")


if __name__ == '__main__':
    main()

# EOF
