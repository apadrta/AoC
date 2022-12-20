#!/usr/bin/env python
# -*- coding:utf-8 -*-
"""
Advent of code 2022 - Day 20
"""

import argparse


def get_args():
    """
    Cmd line argument parsing (preprocessing)
    """
    # Assign description to the help doc
    parser = argparse.ArgumentParser(
        description='Advent of code 2022: Day 20')

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
    data = []
    for line in lines:
        data.append(int(line))
    return data


def mix2array(numbers, first):
    """
    mix numbers structure to array
    """
    # mix
    idx = 0
    while idx < len(numbers):
        # move idx-th item
        source_index = idx
        value = numbers[source_index]['value']
        # no move for zero value
        idx += 1
        if value == 0:           
            continue
        # take out from list
        numbers[numbers[source_index]['next_item']]['prev_item'] = numbers[source_index]['prev_item']
        numbers[numbers[source_index]['prev_item']]['next_item'] = numbers[source_index]['next_item']
        if source_index == first:
            first = numbers[source_index]['next_item']
        # find position to put in
        target_index = source_index
        if value < 0:
            jdx = 0
            while jdx <= (-1 * value) % (len(numbers) - 1):
                jdx += 1
                target_index = numbers[target_index]['prev_item']
        else:
            jdx = 0
            while jdx < value % (len(numbers) - 1):
                jdx += 1
                target_index = numbers[target_index]['next_item']
        # add to list after target
        numbers[source_index]['prev_item'] = target_index
        numbers[source_index]['next_item'] = numbers[target_index]['next_item']
        numbers[numbers[source_index]['prev_item']]['next_item'] = source_index
        numbers[numbers[source_index]['next_item']]['prev_item'] = source_index
    # convert to array
    arr = [None] * len(numbers)
    idx = 0
    pos = first
    while idx < len(numbers):
        arr[idx] = numbers[pos]['value']
        pos = numbers[pos]['next_item']
        idx += 1
    return arr, numbers, first


def solve_part1(data, key, repetitions):
    """
    decrypt
    """
    arr = [x * key for x in data]
    first = 0
    # transform to structure
    numbers = []
    for idx, number in enumerate(arr):
        next_item = (idx + 1) % len(arr)
        prev_item = (len(arr) + idx - 1) % len(arr)
        numbers.append({'value': number, 'next_item': next_item, 'prev_item': prev_item})
    for _ in range(0, repetitions):
        # perform mixing
        arr, numbers, first = mix2array(numbers, first)
    pos = arr.index(0)
    return arr[(pos + 1000) % len(arr)] + arr[(pos + 2000) % len(arr)] + arr[(pos+3000) % len(arr)]


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

    # preprocess data
    data = parse_input(lines)

    # part 1
    res = solve_part1(data, 1, 1)
    print(f"Part 1 solution: {res}")

    # part 2
    res = solve_part1(data, 811589153, 10)
    print(f"Part 2 solution: {res}")


if __name__ == '__main__':
    main()

# EOF
