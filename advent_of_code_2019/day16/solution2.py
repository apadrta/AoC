#!/usr/bin/env python
# -*- coding:utf-8 -*-
"""
Advent of code 2019 - Day 16
"""

import argparse


def get_args():
    """
    Cmd line argument parsing (preprocessing)
    """
    # Assign description to the help doc
    parser = argparse.ArgumentParser(
        description='Advent of code 2019: Day 16')

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


def fft_fast(data, phases):
    """
    Fast variant of fft (used external knowledge)
    """
    print("Computing started")
    signal = data * 10000
    offset = (signal[int(signal[0:7]):])
    for i in range(0, phases):
        print(f"  Phase {i}")
        string = ''
        off = 0
        while off < len(offset):
            if off == 0:
                total = 0
                for off2 in offset:
                    total += int(off2)
            elif off > 0:
                total -= int(offset[off-1])
            string += str(total)[-1]
            off += 1
        offset = string
    return offset[0:8]


def main():
    """
    Main function
    """

    # process args
    infile = get_args()

    # read data
    data = []
    with open(infile, "r") as fileh:
        data = fileh.readline().replace('\n', '').replace('\r', '')

    print(f"Part 2 solution: {fft_fast(data, 100)}")


if __name__ == '__main__':
    main()

# EOF
