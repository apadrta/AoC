#!/usr/bin/env python
# -*- coding:utf-8 -*-
"""
Advent of code 2022 - Day 10
"""

import argparse


def get_args():
    """
    Cmd line argument parsing (preprocessing)
    """
    # Assign description to the help doc
    parser = argparse.ArgumentParser(
        description='Advent of code 2022: Day 10')

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


def evaluate_register(code):
    """
    evaluate register content in time
    """
    # preprocess
    tick = 0
    regs = [1]
    for inst in code:
        if inst[0] == 'noop':
            tick += 1
            regs.append(regs[-1])
        elif inst[0] == 'addx':
            tick += 2
            regs.append(regs[-1])
            regs.append(regs[-1] + inst[1])
    return regs


def make_checksum(regs):
    """
    make checksum from given regs
    """
    # make checksum
    sums = regs[20-1] * 20
    idx = 60
    while idx < len(regs):
        sums += idx * regs[idx-1]
        idx += 40
    return sums


def decode_crt(regs):
    """
    decode CRT content
    """
    crt = []
    line = ''
    pos = 0
    for idx, _ in enumerate(regs):
        if abs(pos - regs[idx]) <= 1:
            line += '#'
        else:
            line += ' '
        pos += 1
        if pos == 40:
            print(line)
            pos = 0
            line = ''
    return crt


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

    # prepare data
    instructions = []
    for line in lines:
        parts = line.split(' ')
        if parts[0] == 'noop':
            instructions.append([parts[0]])
        else:
            instructions.append([parts[0], int(parts[1])])

    # evaluate register values
    registers = evaluate_register(instructions)

    # evaluate part 1
    res = make_checksum(registers)
    print("Part 1 solution: {}".format(res))

    # evaluate part 2
    print("Part 2 solution:")
    res = decode_crt(registers)


if __name__ == '__main__':
    main()

# EOF
