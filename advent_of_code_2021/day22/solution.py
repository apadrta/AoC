#!/usr/bin/env python
# -*- coding:utf-8 -*-
"""
Advent of code 2021 - Day 22
"""

import argparse


def get_args():
    """
    Cmd line argument parsing (preprocessing)
    """
    # Assign description to the help doc
    parser = argparse.ArgumentParser(
        description='Advent of code 2021: Day 22')

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


def lines2instructions(lines):
    """
    Convert lines to instructions field
    """
    instructions = []
    for line in lines:
        [order, values] = line.split(" ")
        new_inst = {}
        new_inst['order'] = order
        [x_size, y_size, z_size] = values.split(",")
        new_inst['cube'] = [[], [], []]
        new_inst['cube'][0] = [int(x) for x in x_size[2:].split('..')]
        new_inst['cube'][1] = [int(x) for x in y_size[2:].split('..')]
        new_inst['cube'][2] = [int(x) for x in z_size[2:].split('..')]
        instructions.append(new_inst)
    return instructions


def intersect(object_a, object_b):
    """
    Return intersection of two areas
    """
    object_new = [[], [], []]
    for dim in range(3):
        # check if whether object has lower position
        if object_a[dim][0] < object_b[dim][0]:
            low = object_a[dim]
            high = object_b[dim]
        else:
            low = object_b[dim]
            high = object_a[dim]
        # check interserction
        if low[1] < high[0]:
            # no intersetion
            return None
        if high[1] <= low[1]:
            # high is inside low
            object_new[dim] = [high[0], high[1]]
            continue
        object_new[dim] = [high[0], low[1]]
    return object_new


def core_manipulation(instructions):
    """
    Matipulate with core accordind instruction
    """
    areas = []   # field of [area, type (1=on, -1=off)]
    for instruction in instructions:
        new_items = []
        for area in areas:
            inter = intersect(instruction['cube'], area[0])
            if inter:
                new_items.append([inter, area[1] * -1])
        areas += new_items
        if instruction['order'] == 'on':
            areas.append([instruction['cube'], +1])
        print(".", end='', flush=True)
    return areas


def sum_areas(areas):
    """
    Sum areas
    """
    numsum = 0
    for area in areas:
        volume = area[1]
        for dim in range(3):
            volume *= area[0][dim][1] - area[0][dim][0] + 1
        numsum += volume
    return numsum


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

    # convert data to instructions
    instructions = lines2instructions(lines)

    # part 1
    limited_instructions = []
    for item in instructions:
        # use only instruction with at least part of its cube in initialization area
        limited = intersect(item['cube'], [[-50, 50], [-50, 50], [-50, 50]])
        if limited:
            limited_instructions.append({'order': item['order'], 'cube': limited})
    core = core_manipulation(limited_instructions)
    print(f"\nPart 1 solution: {sum_areas(core)} (core objects: {len(core)})")

    # part 2
    core = core_manipulation(instructions)
    print(f"\nPart 1 solution: {sum_areas(core)} (core objects: {len(core)})")


if __name__ == '__main__':
    main()

# EOF
