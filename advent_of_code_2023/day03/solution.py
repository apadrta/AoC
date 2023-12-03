#!/usr/bin/env python
# -*- coding:utf-8 -*-
"""
Advent of code 2023 - Day 3
"""

import argparse


def get_args():
    """
    Cmd line argument parsing (preprocessing)
    """
    # Assign description to the help doc
    parser = argparse.ArgumentParser(
        description='Advent of code 2023: Day 3'
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

    numbers = []
    symbols = {}
    for yidx, line in enumerate(data):
        act_number = 0
        act_len = 0
        for xidx, char in enumerate(line):
            if char.isnumeric():
                # proccess digit
                act_number = act_number * 10 + int(char)
                act_len += 1
            elif char != '.':
                # process symbol
                symbols[(xidx, yidx)] = char
            # store finished number
            if act_len > 0:
                if not char.isnumeric():
                    numbers.append({'num': act_number, 'x_from': xidx - act_len, 'x_to': xidx - 1, 'y': yidx})
                    act_number = 0
                    act_len = 0
                elif xidx == len(line) - 1:
                    numbers.append({'num': act_number, 'x_from': xidx - act_len + 1, 'x_to': xidx, 'y': yidx})
                    act_number = 0
                    act_len = 0
    return numbers, symbols


def is_adjanced(number, symbols):
    """
    check if some symbol is near the number
    """
    for symbol in symbols.keys():
        if number['x_from'] - 1 <= symbol[0] <= number['x_to'] + 1 and number['y'] - 1 <= symbol[1] <= number['y'] + 1:
            return True
    return False


def get_gear_value(gear_pos, numbers):
    """
    return gear value (or zero if not gear
    """
    nums = []
    for number in numbers:
        if abs(gear_pos[1] - number['y']) > 1:
            continue
        if gear_pos[0] < number['x_from'] - 1:
            continue
        if gear_pos[0] > number['x_to'] + 1:
            continue
        nums.append(number['num'])
        if len(nums) == 2:
            return nums[0] * nums[1]
    return 0


def main():
    """
    Main function
    """

    # process args
    infile = get_args()

    # read data
    numbers, symbols = read_data_struct(infile)

    # part 1
    sums = 0
    for number in numbers:
        if is_adjanced(number, symbols):
            sums += number['num']
    print(f"Part 1 solution: {sums}")

    # part 2
    sums = 0
    for position, symbol in symbols.items():
        if symbol == '*':
            sums += get_gear_value(position, numbers)
    print(f"Part 2 solution: {sums}")


if __name__ == '__main__':
    main()

# EOF
