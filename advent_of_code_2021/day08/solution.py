#!/usr/bin/env python
# -*- coding:utf-8 -*-
"""
Advent of code 2021 - Day 8
"""

import argparse


def get_args():
    """
    Cmd line argument parsing (preprocessing)
    """
    # Assign description to the help doc
    parser = argparse.ArgumentParser(
        description='Advent of code 2021: Day 8')

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


correct_wiring = {
    "abcefg": 0,
    "cf": 1,
    "acdeg": 2,
    "acdfg": 3,
    "bcdf": 4,
    "abdfg": 5,
    "abdefg": 6,
    "acf": 7,
    "abcdefg": 8,
    "abcdfg": 9
}


def get_codebook(wiring):
    """
    Create codebook from wires (use external knowledge)
    """
    tmp = {}
    mapping = {}
    for wire in wiring:
        if len(wire) == 2:
            tmp[1] = set(wire)
        elif len(wire) == 4:
            tmp[4] = set(wire)
        elif len(wire) == 3:
            tmp[7] = set(wire)
        elif len(wire) == 7:
            tmp[8] = set(wire)
    for wire in wiring:
        if len(wire) == 5 and len(set(wire).intersection(tmp[1])) == 2:
            tmp[3] = set(wire)
    for wire in wiring:
        if len(wire) == 5 and len(set(wire).intersection(tmp[1])) == 1:
            if len(set(wire).intersection(tmp[8]-tmp[4] - tmp[3])) == 0:
                tmp[5] = set(wire)
            else:
                tmp[2] = set(wire)
    for wire in wiring:
        if len(wire) == 6:
            if len(set(wire).intersection(tmp[3])) == 5:
                tmp[9] = set(wire)
            else:
                if len(set(wire).intersection(tmp[5])) == 5:
                    tmp[6] = set(wire)
                else:
                    tmp[0] = set(wire)
    mapping[(tmp[7] - tmp[1]).pop()] = 'a'
    mapping[(tmp[8] - tmp[2] - tmp[1]).pop()] = 'b'
    mapping[(tmp[8] - tmp[0]).pop()] = 'd'
    mapping[(tmp[2].intersection(tmp[1])).pop()] = 'c'
    mapping[(tmp[8] - tmp[4] - tmp[3]).pop()] = 'e'
    mapping[(tmp[5].intersection(tmp[1])).pop()] = 'f'
    mapping[(set('abcdefg') - set(mapping.keys())).pop()] = 'g'

    return mapping


def str2num(mapping, data):
    """
    Convert data to number according to mapping
    """
    correct = ''
    for char in data:
        correct += mapping[char]
    return correct_wiring[''.join(sorted(correct))]


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

    digits = []
    for line in data:
        [wire, disp] = line.replace('\n', '').replace('\r', '').split(" | ")
        digits.append({'wire': wire.split(" "), 'disp': disp.split(" ")})

    numsum = 0
    for digit in digits:
        for item in digit['disp']:
            if len(item) in [2, 4, 3, 7]:
                numsum += 1
    # first part
    print(f"Part 1 solution: {numsum}")

    # second part
    numsum = 0
    for digit in digits:
        codebook = get_codebook(digit['wire'])
        out = 0
        for num in digit['disp']:
            out = out*10 + str2num(codebook, num)
        numsum += out
    print(f"Part 2 solution: {numsum}")


if __name__ == '__main__':
    main()

# EOF
