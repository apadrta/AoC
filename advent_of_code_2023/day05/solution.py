#!/usr/bin/env python
# -*- coding:utf-8 -*-
"""
Advent of code 2023 - Day 5
"""

import argparse


def get_args():
    """
    Cmd line argument parsing (preprocessing)
    """
    # Assign description to the help doc
    parser = argparse.ArgumentParser(
        description='Advent of code 2023: Day 5'
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
    data = [x.replace('  ', ' ').strip() for x in data]

    seeds = [int(x) for x in data[0][7:].split(' ')]
    maps = {}
    actmap = {}
    for item in data[2:]:
        if 'map' in item:
            if actmap:
                maps[actmap['from']] = actmap
            name = item.split(' ')[0].split('-to-')
            actmap = {'from': name[0], 'to': name[1], 'mapping': []}
        elif item:
            # convert mapping to structure [from, to, modifier] (i.e. if input is in from-to, add modifier to get output)
            mod = [int(x) for x in item.split(' ')]
            actmap['mapping'].append([mod[1], mod[1] + mod[2] - 1, mod[0] - mod[1]])
    if actmap:
        maps[actmap['from']] = actmap
    return seeds, maps


def transform_data(value, valtype, maps):
    """
    Tranform input value according to given map
    """
    if valtype not in maps:
        return None, None
    for trans in maps[valtype]['mapping']:
        if trans[0] <= value <= trans[1]:
            return value + trans[2], maps[valtype]['to']

    return value, maps[valtype]['to']


def main():
    """
    Main function
    """

    # process args
    infile = get_args()

    # read data
    seeds, maps = read_data_struct(infile)
#    print(seeds, maps)

    # part 1
    mins = None
    for seed in seeds:
        val = seed
        valtype = 'seed'
        while valtype and valtype != 'location':
            val, valtype = transform_data(val, valtype, maps)
        if not mins:
            mins = val
        elif val < mins:
            mins = val
    print(f"Part 1 solution: {mins}")

    # part 2
    new_seeds = []
    srange = []
    for idx, value in enumerate(seeds):
        if idx % 2 == 0:
            srange = [value]
        else:
            srange.append(srange[0] + value - 1)
            new_seeds.append(srange)

    mins = None
    idx = 0
    for srange in new_seeds:
        seed = srange[0]
        while seed <= srange[1]:
            val = seed
            valtype = 'seed'
            while valtype and valtype != 'location':
                val, valtype = transform_data(val, valtype, maps)
            if not mins:
                mins = val
            elif val < mins:
                mins = val
            seed += 1
            idx += 1
            if idx % 100000 == 0:
                print(f'Seed checked: {idx/1000000:.6f}')
    print(f"Part 2 solution: {mins}")


if __name__ == '__main__':
    main()

# EOF
