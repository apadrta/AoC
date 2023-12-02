#!/usr/bin/env python
# -*- coding:utf-8 -*-
"""
Advent of code 2023 - Day 2
"""

import argparse


def get_args():
    """
    Cmd line argument parsing (preprocessing)
    """
    # Assign description to the help doc
    parser = argparse.ArgumentParser(
        description='Advent of code 2023: Day 2'
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

    games = []
    for line in data:
        gid, cubes = line.split(': ')
        item = {'id': int(gid.split(' ')[1]), 'rounds': []}
        reaches = cubes.split('; ')
        for reach in reaches:
            infos = reach.split(', ')
            field = {}
            for info in infos:
                number, color = info.split(' ')
                field[color] = int(number)
            item['rounds'].append(field)
        games.append(item)
    return games


def check_possibility(rounds, data):
    """
    check if data are compliant with game
    """
    for item in rounds:
        for color, value in item.items():
            if data[color] < value:
                return False
    return True


def get_min_cubes_power(rounds):
    """
    compute power of minimal number of cubes
    """
    mins = {'red': 0, 'green': 0, 'blue': 0}
    for item in rounds:
        for color, value in item.items():
            if mins[color] < value:
                mins[color] = value
    return mins['red'] * mins['green'] * mins['blue']


def main():
    """
    Main function
    """

    # process args
    infile = get_args()

    # read data
    games = read_data_struct(infile)
#    print(games)

    # part 1
    sums = 0
    for game in games:
        res = check_possibility(
                game['rounds'],
                {'red': 12, 'green': 13, 'blue': 14}
                )
        if res:
            sums += game["id"]
    print(f"Part 1 solution: {sums}")

    # part 2
    sums = 0
    for game in games:
        sums += get_min_cubes_power(game['rounds'])
    print(f"Part 2 solution: {sums}")


if __name__ == '__main__':
    main()

# EOF
