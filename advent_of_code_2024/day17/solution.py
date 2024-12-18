#!/usr/bin/env python
# -*- coding:utf-8 -*-
"""
Advent of code 2024 - Day 17
"""

import argparse


def get_args():
    """
    Cmd line argument parsing (preprocessing)
    """
    # Assign description to the help doc
    parser = argparse.ArgumentParser(
        description='Advent of code 2024: Day 16')

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
    registers = {}
    program = []
    for line in data:
        if line[:8] == "Register":
            reg, val = line[9:].split(': ')
            registers[reg] = int(val)
        elif line[:7] == "Program":
            program = [int(x) for x in line[9:].split(',')]
    return registers, program


class Elf3bit():
    """
    Class for representing 3bit elf computer
    """

    def __init__(self):
        """
        Constructor
        """
        self.regs = {}
        self.code = []
        self.ptr = 0
        self.out = []

    def set_registry(self, settings):
        """
        Set registry content
        """
        self.regs = settings

    def run_code(self, settings):
        """
        Run given code
        """
        self.code = settings
        self.ptr = 0
        self.out = []
        while self.ptr < len(self.code):
            if self.code[self.ptr] == 0:
                self.inst_adv()
            elif self.code[self.ptr] == 1:
                self.inst_bxl()
            elif self.code[self.ptr] == 2:
                self.inst_bst()
            elif self.code[self.ptr] == 3:
                self.inst_jnz()
            elif self.code[self.ptr] == 4:
                self.inst_bxc()
            elif self.code[self.ptr] == 5:
                self.inst_out()
            elif self.code[self.ptr] == 6:
                self.inst_bdv()
            elif self.code[self.ptr] == 7:
                self.inst_cdv()

    def combo(self, value):
        """
        Evaluate combo literal
        """
        if value < 4:
            return value
        if value == 4:
            return self.regs['A']
        if value == 5:
            return self.regs['B']
        if value == 6:
            return self.regs['C']
        return None

    def inst_adv(self):
        """
        Realize instruction
        """
        num = self.regs['A']
        den = 2**self.combo(self.code[self.ptr + 1])
        self.regs['A'] = int(num/den)
        self.ptr += 2

    def inst_bxl(self):
        """
        Realize instruction
        """
        self.regs['B'] = self.regs['B'] ^ self.code[self.ptr + 1]
        self.ptr += 2

    def inst_bst(self):
        """
        Realize instruction
        """
        self.regs['B'] = self.combo(self.code[self.ptr + 1]) % 8
        self.ptr += 2

    def inst_jnz(self):
        """
        Realize instruction
        """
        if self.regs['A']:
            self.ptr = self.code[self.ptr + 1]
            return
        self.ptr += 2

    def inst_bxc(self):
        """
        Realize instruction
        """
        self.regs['B'] = self.regs['B'] ^ self.regs['C']
        self.ptr += 2

    def inst_out(self):
        """
        Realize instruction
        """
        self.out.append(self.combo(self.code[self.ptr + 1]) % 8)
        self.ptr += 2

    def inst_bdv(self):
        """
        Realize instruction
        """
        num = self.regs['A']
        den = 2**self.combo(self.code[self.ptr + 1])
        self.regs['B'] = int(num/den)
        self.ptr += 2

    def inst_cdv(self):
        """
        Realize instruction
        """
        num = self.regs['A']
        den = 2**self.combo(self.code[self.ptr + 1])
        self.regs['C'] = int(num/den)
        self.ptr += 2


def find_a_for_replication(code):
    """
    Find A value to force codes 2,4,1,*,7,5,0,3,1,*,4,*,5,5,3,0 to print themselves
                                2,4,1,6,7,5,4,6,1,4,5,5,0,3,3,0
    """
    xor1 = code[3]
    xor2 = code[9]

    conditions = {}
    for target in [0, 1, 2, 3, 4, 5, 6, 7]:
        # compute possible shifts (last three bits)
        idx = 0
        conditions[target] = []
        while idx < 8:
            b_reg = idx & 0b111
            b_reg = b_reg ^ xor1
            shift = b_reg
            part2 = target ^ b_reg ^ xor2
            a_possible = part2 << shift | idx
            if (a_possible >> shift) ^ b_reg ^ xor2 == target:
                conditions[target].append({"lastbits": idx, "numbits": part2, "numshift": shift})
            idx += 1

    states = [0]
    for byte in code[::-1]:
        # find possible part of starting a_reg for all states and given byte of code
        new_states = []
        for state in states:
            for condition in conditions[byte]:
                check_num = (state << 3) | condition["lastbits"]
                check_val = (check_num >> (condition['numshift'])) & 0b111
                if check_val == condition["numbits"]:
                    new_state = state * 8 + condition["lastbits"]
                    new_states.append(new_state)
        states = new_states

    mins = states[0]
    for state in states[1:]:
        if state < mins:
            mins = state
    return mins


def main():
    """
    Main function
    """

    # process args
    infile = get_args()

    # read data
    regs, prog = read_data(infile)

    # part 1
    comp = Elf3bit()

    comp.set_registry(regs)
    comp.run_code(prog)
    sums = ",".join([str(x) for x in comp.out])
    print(f"Part 1 solution: {sums}")

    # part 2
    sums = find_a_for_replication(prog)
    print(f"Part 2 solution: {sums}")


if __name__ == '__main__':
    main()

# EOF
