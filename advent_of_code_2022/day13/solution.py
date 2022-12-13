#!/usr/bin/env python
# -*- coding:utf-8 -*-
"""
Advent of code 2022 - Day 13
"""

import argparse
from ast import literal_eval
from functools import cmp_to_key


def get_args():
    """
    Cmd line argument parsing (preprocessing)
    """
    # Assign description to the help doc
    parser = argparse.ArgumentParser(
        description='Advent of code 2022: Day 13')

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


def eval_packets2(packet_a, packet_b):
    """
    compare two packets
    """
    # compare int-int combination
    if isinstance(packet_a, int) and isinstance(packet_b, int):
        if packet_a > packet_b:
            return -1
        if packet_a == packet_b:
            return 0
        return 1
    # compare list-int combination
    if isinstance(packet_a, list) and isinstance(packet_b, int):
        if not packet_a:
            return 1
        res = eval_packets2(packet_a, [packet_b])
        if res == -1:
            return -1
        return res
    # compare int-list combination
    if isinstance(packet_a, int) and isinstance(packet_b, list):
        if not packet_b:
            return -1
        res = eval_packets2([packet_a], packet_b)
        if res == -1:
            return -1
        return res
    # compare list-list combinations
    idx = 0
    res = 0
    while True:
        # end of both lists reached
        if idx == len(packet_a) and idx == len(packet_b):
            return res
        # packet A is shorter (no problem in previous comparison)
        if idx == len(packet_a):
            return 1
        # packet B is shorter (no problem in previous comparison)
        if idx == len(packet_b):
            return -1
        # compare two items in list
        res = eval_packets2(packet_a[idx], packet_b[idx])
        if res == -1:
            return -1
        if res == 1:
            return 1
        idx += 1


def eval_packets2rev(packet_a, packet_b):
    """
    compare two packets in reverse order
    """
    return eval_packets2(packet_a, packet_b) * -1


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
    pairs = []
    pair = []
    for line in lines:
        if line:
            packet = literal_eval(line)
            pair.append(packet)
        else:
            pairs.append(pair)
            pair = []
    pairs.append(pair)

    res = 0
    for idx, pair in enumerate(pairs):
        order = eval_packets2(pair[0], pair[1])
        if order == 1:
            res += (idx + 1)
    print(f"Part 1 solution: {res}")

    # part 2
    data = [[[2]], [[6]]]
    for line in lines:
        if line:
            data.append(literal_eval(line))
    # sort
    sdata = sorted(data, key=cmp_to_key(eval_packets2rev))

#    for item in sdata:
#        print(item)
    res = (sdata.index([[2]]) + 1) * (sdata.index([[6]]) + 1)
    print(f"Part 2 solution: {res}")


if __name__ == '__main__':
    main()

# EOF
