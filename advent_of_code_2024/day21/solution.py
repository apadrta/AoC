#!/usr/bin/env python
# -*- coding:utf-8 -*-
"""
Advent of code 2024 - Day 21
"""

import argparse
from copy import deepcopy

vector = {
    0: [-1, 0],
    1: [0, 1],
    2: [1, 0],
    3: [0, -1]
}


def get_args():
    """
    Cmd line argument parsing (preprocessing)
    """
    # Assign description to the help doc
    parser = argparse.ArgumentParser(
        description='Advent of code 2024: Day 21'
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


def generate_metadata(keyboard):
    """
    Generate meta data for button pushing
    """
    # prepare variables
    chars = ''
    for row in keyboard:
        chars += ''.join(x for x in row)
    pos = {}
    idx = 0
    while idx < len(keyboard):
        jdx = 0
        while jdx < len(keyboard[0]):
            pos[keyboard[idx][jdx]] = (idx, jdx)
            jdx += 1
        idx += 1
    # fill metadata
    metadata = {}
    for src, srcval in pos.items():
        if src == '':
            continue
        if src not in metadata:
            metadata[src] = {}
        for dst, dstval in pos.items():
            if dst == '':
                continue
            v_char = "v"
            if srcval[0] > dstval[0]:
                v_char = "^"
            v_str = abs(dstval[0] - srcval[0])*v_char
            h_char = ">"
            if srcval[1] > dstval[1]:
                h_char = "<"
            h_str = abs(dstval[1] - srcval[1])*h_char
            metadata[src][dst] = []
            if keyboard[dstval[0]][srcval[1]] != '':
                metadata[src][dst].append(f"{v_str}{h_str}")
            if keyboard[srcval[0]][dstval[1]] != '':
                if f"{h_str}{v_str}" not in metadata[src][dst]:
                    metadata[src][dst].append(f"{h_str}{v_str}")
    return metadata


def code2states(code):
    """
    Create basic numstring
    """
    # information about keyboard
    num_meta = generate_metadata([['7', '8', '9'], ['4', '5', '6'], ['1', '2', '3'], ['', '0', 'A']])
    # generate order strings
    nums = ['']
    code = "A" + code
    idx = 0
    while idx < len(code) - 1:
        new = []
        for num in nums:
            for path in num_meta[code[idx]][code[idx+1]]:
                new.append(num + path + 'A')
        nums = new
        idx += 1
    # convert to states
    states = []
    for num in nums:
        new = []

        last = 'A'
        idx = 0
        matrix = {}
        while idx < len(num):
            transid = (last, num[idx])
            if transid not in matrix:
                matrix[transid] = 0
            matrix[transid] += 1
            last = num[idx]
            idx += 1
        states.append(matrix)
        sums = 0
        for value in matrix.values():
            sums += value
#        print(f"FIRST SUM={sums}")
    return states


def orders2trans(orders):
    """
    Convert string to list of transitions
    """
    idx = 0
    trans = []
    while idx < len(orders) - 1:
        trans.append((orders[idx], orders[idx+1]))
        idx += 1
    return trans


def add_robot(orders):
    """
    add robot to the cascade
    """
    # information about keyboard
    robot_meta = generate_metadata([['', '^', 'A'], ['<', 'v', '>']])

    states = []
    for order in orders:
        works = [{}]
        for key, value in order.items():
            new_works = []
            for work in works:
                for path in robot_meta[key[0]][key[1]]:
                    akt = deepcopy(work)
                    for trans in orders2trans('A' + path + 'A'):
                        if trans not in akt:
                            akt[trans] = 0
                        akt[trans] += value
                    new_works.append(akt)
            works = new_works
        states += works
    for state in states:
        sums = 0
        for value in state.values():
            sums += value
    return states


def get_len(order):
    """
    Compute length of order
    """
    sums = 0
    for value in order.values():
        sums += value
    return sums


def min_len(orders):
    """
    Find and return minimal length of orders
    """
    mins = -1
    for order in orders:
        sums = get_len(order)
        if mins == -1 or sums < mins:
            mins = sums
    return mins


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
    for code in data:
        orders = code2states(code)
        orders = add_robot(orders)
        orders = add_robot(orders)
        sums += min_len(orders) * int(code[0:3])
    print(f"Part 1 solution: {sums}")

    # part 2
    sums = 0
    for code in data:
        print(f'CODE {code} ', end='', flush=True)
        orders = code2states(code)
        for _ in range(0, 25):
            new_orders = []
            prune = min_len(orders)
            for order in orders:
                if get_len(order) == prune:
                    new_orders.append(order)
            orders = new_orders
            print('.', end='', flush='True')
            orders = add_robot(orders)
        sums += min_len(orders) * int(code[0:3])
        print('\n')
    print(f"\nPart 2 solution: {sums}")


if __name__ == '__main__':
    main()

# EOF
