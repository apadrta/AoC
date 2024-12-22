#!/usr/bin/env python
# -*- coding:utf-8 -*-
"""
Advent of code 2024 - Day 22
"""

import argparse


def get_args():
    """
    Cmd line argument parsing (preprocessing)
    """
    # Assign description to the help doc
    parser = argparse.ArgumentParser(
        description='Advent of code 2024: Day 22')

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
    data = [int(x) for x in data]
    return data


def count_secret(base, number):
    """
    Generate pseudorandom number
    """
    idx = 0
    nums = [base]
    while idx < number:
        base = ((base << 6) ^ base) & 0b111111111111111111111111
        base = ((base >> 5) ^ base) & 0b111111111111111111111111
        base = ((base << 11) ^ base) & 0b111111111111111111111111
        idx += 1
        nums.append(base)
    return nums


def get_diffs(secrets):
    """
    get diffs and its values
    """
    diffs = []
    idx = 1
    while idx < len(secrets):
        diffs.append((secrets[idx] % 10) - (secrets[idx-1] % 10))
        idx += 1
    idx = 0
    data = {}
    while idx < len(diffs) - 3:
        diff = diffs[idx:idx+4]
        idx += 1
        if tuple(diff) not in data:
            # preserve just first combination
            data[tuple(diff)] = secrets[idx+3] % 10
    return data


def eval_market(market):
    """
    evaluate best combination
    """
    maxs = 0
    for combination, data in market.items():
        sums = 0
#        print(data)
        for key, value in data.items():
            sums += key * value
        if sums > maxs:
            maxs = sums
            print(combination, sums)
    return maxs


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
    market = {}
    for item in data:
        secrets = count_secret(item, 2000)
#        secrets = count_secret(123, 9)
        sums += secrets[-1]
        diffs = get_diffs(secrets)
        for key, value in diffs.items():
            if key not in market:
                market[key] = {}
            if value not in market[key]:
                market[key][value] = 0
            market[key][value] += 1
#    print(market)
    sums2 = eval_market(market)
    print(f"Part 1 solution: {sums}")

    # part 2
    print(f"Part 2 solution: {sums2}")


if __name__ == '__main__':
    main()

# EOF
