#!/usr/bin/env python
# -*- coding:utf-8 -*-
"""
Advent of code 2019 Day 21
"""


import argparse
from elfcpu import ElfCPU


def get_args():
    """
    Cmd line argument parsing (preprocessing)
    """
    # Assign description to the help doc
    parser = argparse.ArgumentParser(
        description='Advent of code 2019 Day 21')

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


class ElfDroid():
    """
    Elf Droid for exploring tractor beam
    """

    def __init__(self):
        """
        Constructor
        """
        self.cpu = None

    def init_cpu(self, filename):
        """
        Initialize droid CPU
        """
        self.cpu = ElfCPU()
        self.cpu.read_code(filename)
        self.cpu.run()

    def run_orders(self, orders):
        """
        Manually explore floor
        """
        for order in orders:
            self.cpu.add_inputs(order)
            self.cpu.run()
            reply = self.cpu.get_output()
        return reply


def springscript2intcode(program):
    """
    convert springscript to intcode
    """
    intcode = []
    for instruction in program:
        intcode.append([ord(x) for x in instruction] + [10])
    return intcode


def print_res(res):
    """
    print result in readable form
    """
    for char in res:
        if char < 128:
            print(chr(char), end='')
        else:
            print(char)
            return char
    return None


def solution_part1(infile):
    """
    solution of part1 (use WALK)
    """
    # initialize
    droid = ElfDroid()
    droid.init_cpu(infile)
    script = [
        'NOT T T',
        'AND A T',
        'AND B T',
        'AND C T',
        'NOT T T',
        'AND D T',
        'OR T J',
        'WALK'
    ]
    code = springscript2intcode(script)
    res = droid.run_orders(code)
    ret = print_res(res)
    return ret


def solution_part2(infile):
    """
    solution of part2 (use RUN)
    """
    # initialize
    droid = ElfDroid()
    droid.init_cpu(infile)
    script = [
        'NOT T T',
        'AND A T',
        'AND B T',
        'AND C T',
        'NOT T T',
        'AND D T',
        'OR E J',
        'OR H J',
        'AND T J',
        'RUN'
    ]
    code = springscript2intcode(script)
    res = droid.run_orders(code)
    ret = print_res(res)
    return ret


def main():
    """
    Main function
    """

    # process args
    infile = get_args()

    # part one
    res = solution_part1(infile)
    print(f"Solution of part 1: {res}")

    # part two
    res = solution_part2(infile)
    print(f"Solution of part 2: {res}")


if __name__ == '__main__':
    main()

# EOF
