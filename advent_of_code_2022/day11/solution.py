#!/usr/bin/env python
# -*- coding:utf-8 -*-
"""
Advent of code 2022 - Day 11
"""

import argparse
from math import floor


def get_args():
    """
    Cmd line argument parsing (preprocessing)
    """
    # Assign description to the help doc
    parser = argparse.ArgumentParser(
        description='Advent of code 2022: Day 11')

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


def parse_data(lines):
    """
    parse  input data
    """
    monkeys = []
    monkey = {}
    monkey['inspections'] = 0
    for line in lines:
        if not line:
            monkeys.append(monkey)
            monkey = {}
            monkey['inspections'] = 0
        if 'Starting items' in line:
            monkey['items'] = [int(x) for x in line.split(': ')[1].split(', ')]
        if 'divisible' in line:
            monkey['divisible'] = int(line.split(' ')[-1])
        if 'If true' in line:
            monkey['true_throw'] = int(line.split(' ')[-1])
        if 'If false' in line:
            monkey['false_throw'] = int(line.split(' ')[-1])
        if 'Operation' in line:
            parts = line.split(' ')
            monkey['operation'] = parts[-2]
            if parts[-1] != 'old':
                parts[-1] = int(parts[-1])
            monkey['operand'] = parts[-1]
    monkeys.append(monkey)
    return monkeys


def simulate_monkeys(monkeys, rounds):
    """
    simulate throwing
    """
    for _ in range(0, rounds):
        # throw things
        for monkey in monkeys:
            for item in monkey['items']:
                # increase worry level
                value = monkey['operand']
                if monkey['operand'] == 'old':
                    value = item
                if monkey['operation'] == '+':
                    item = item + value
                else:
                    item = item * value
                # divide by 3
                item = floor(item / 3.0)
                monkey['inspections'] += 1
                # throw to other monkey
                target_monkey = monkey['false_throw']
                if item % monkey['divisible'] == 0:
                    target_monkey = monkey['true_throw']
                monkeys[target_monkey]['items'].append(item)
            monkey['items'] = []
    return monkeys


def simulate_monkeys_part2(monkeys, rounds):
    """
    simulate throwing
    """
    multi = 1
    for monkey in monkeys:
        multi *= monkey['divisible']
    for _ in range(0, rounds):
        # throw things
        for monkey in monkeys:
            for item in monkey['items']:
                # increase worry level
                value = monkey['operand']
                if monkey['operand'] == 'old':
                    value = item
                if monkey['operation'] == '+':
                    item = item + value
                else:
                    item = item * value
                # supress divergence
                item = item % multi
                monkey['inspections'] += 1
                # throw to other monkey
                target_monkey = monkey['false_throw']
                if item % monkey['divisible'] == 0:
                    target_monkey = monkey['true_throw']
                monkeys[target_monkey]['items'].append(item)
            monkey['items'] = []
    return monkeys


def monkey_bussines(monkeys):
    """
    Count monkey business
    """
    sums = []
    for monkey in monkeys:
        sums.append(monkey["inspections"])
    sums.sort()
    return sums[-1] * sums[-2]


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

    # evaluate part 1
    monkeys = parse_data(lines)
    final_monkeys = simulate_monkeys(monkeys, 20)
    res = monkey_bussines(final_monkeys)
    print(f"Part 1 solution: {res}")

    # evaluate part 2
    monkeys = parse_data(lines)
    final_monkeys = simulate_monkeys_part2(monkeys, 10000)
    res = monkey_bussines(final_monkeys)
    print(f"Part 2 solution: {res}")


if __name__ == '__main__':
    main()

# EOF
