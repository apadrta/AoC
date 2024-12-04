#!/usr/bin/env python
# -*- coding:utf-8 -*-
"""
Advent of code 2024 - Day 4
"""

import argparse


def get_args():
    """
    Cmd line argument parsing (preprocessing)
    """
    # Assign description to the help doc
    parser = argparse.ArgumentParser(
        description='Advent of code 2024: Day 4')

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
    return data


def get_words(data, wordlen):
    """
    Get list of all possible words
    """
    # possible directions
    diffs = [
        (-1, 0),
        (-1, +1),
        (0, +1),
        (+1, +1),
        (+1, 0),
        (+1, -1),
        (0, -1),
        (-1, -1),
        ]
    words = []
    for idx in range(0, len(data)):
        for jdx in range(0, len(data[0])):
            for diff in diffs:
                word = ''
                for kdx in range(0, wordlen):
                    row = idx + kdx * diff[0]
                    col = jdx + kdx * diff[1]
                    if (row < 0) or (row > len(data) - 1) or (col < 0) or (col > len(data[0]) - 1):
                        break
                    word += data[row][col]
                if len(word) == wordlen:
                    words.append(word)
    return words


def count_mas(data):
    """
    Count all accurence of two crossed "MAS" string
    """
    mas_pos = [
        (-1, -1, 1, 1),
        (1, 1, -1, -1),
        (-1, 1, 1, -1),
        (1, -1, -1, 1)
    ]
    sums = 0
    for idx in range(1, len(data) - 1):
        for jdx in range(1, len(data[0]) - 1):
            if data[idx][jdx] != "A":
                continue
            mas_cnt = 0
            for pos in mas_pos:
                if data[idx + pos[0]][jdx + pos[1]] == "M" and data[idx + pos[2]][jdx + pos[3]] == "S":
                    mas_cnt += 1
            if mas_cnt == 2:
                sums += 1
    return sums


def main():
    """
    Main function
    """

    # process args
    infile = get_args()

    # read data
    data = read_data(infile)

    # part 1
    sums = 0
    words = get_words(data, 4)
    for word in words:
        if word == "XMAS":
            sums += 1
    print(f"Part 1 solution: {sums}")

    # part 2
    sums = count_mas(data)
    print(f"Part 2 solution: {sums}")


if __name__ == '__main__':
    main()

# EOF
