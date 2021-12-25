#!/usr/bin/env python
# -*- coding:utf-8 -*-
"""
Advent of code 2021 - Day 24
"""

import argparse
from math import floor


def get_args():
    """
    Cmd line argument parsing (preprocessing)
    """
    # Assign description to the help doc
    parser = argparse.ArgumentParser(
        description='Advent of code 2021: Day 24')

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


class ElfALU():
    """
    Class for solving Amphipods problems
    """

    def __init__(self, lines):
        """
        Constructor
        """
        self.code = []
        self.codenum = []
        self.__read_code(lines)

    def __read_code(self, lines):
        """
        Prepare code from lines
        """
        code_lit = ['x', 'y', 'z', 'w', 'inp', 'mul', 'div', 'add', 'mod', 'eql']
        self.code = []
        for line in lines:
            self.code.append([x if x in code_lit else int(x) for x in line.split(" ")])
        for instruction in self.code:
            if instruction[0] == 'inp':
                self.codenum.append([])
            self.codenum[-1].append(instruction)

    def run_codenum(self, num_id, state, char):
        """
        Run part of code
        """
        for instruction in self.codenum[num_id]:
            if instruction[0] == 'inp':
                state[instruction[1]] = char
            elif instruction[0] == 'mul':
                if instruction[2] in ['x', 'y', 'z', 'w']:
                    state[instruction[1]] = state[instruction[1]] * state[instruction[2]]
                else:
                    state[instruction[1]] = state[instruction[1]] * instruction[2]
            elif instruction[0] == 'add':
                if instruction[2] in ['x', 'y', 'z', 'w']:
                    state[instruction[1]] = state[instruction[1]] + state[instruction[2]]
                else:
                    state[instruction[1]] = state[instruction[1]] + instruction[2]
            elif instruction[0] == 'mod':
                if instruction[2] in ['x', 'y', 'z', 'w']:
                    state[instruction[1]] = state[instruction[1]] % state[instruction[2]]
                else:
                    state[instruction[1]] = state[instruction[1]] % instruction[2]
            elif instruction[0] == 'div':
                if instruction[2] in ['x', 'y', 'z', 'w']:
                    state[instruction[1]] = floor(state[instruction[1]] / state[instruction[2]])
                else:
                    state[instruction[1]] = floor(state[instruction[1]] / instruction[2])
            elif instruction[0] == 'eql':
                if instruction[2] in ['x', 'y', 'z', 'w']:
                    state[instruction[1]] = 1 if state[instruction[1]] == state[instruction[2]] else 0
                else:
                    state[instruction[1]] = 1 if state[instruction[1]] == instruction[2] else 0
            else:
                print(f'unknown command "{instruction[0]}"')
                return 666
        return state['z']

    def get_partnum(self, num_id, input_z, char):
        """
        Precompute key values
        """
        var_x7 = input_z % 26 + self.codenum[num_id][5][2]
        if var_x7 == char:
            var_x7 = 0
        else:
            var_x7 = 1
        var_y11 = (25 * var_x7) + 1
        var_y16 = (char + self.codenum[num_id][15][2]) * var_x7
        return var_x7, var_y11, var_y16

    def get_inputs_zs(self, num_id, output_z, variables, char):
        """
        Compute possible input z values for given output_z and precomputed variables
        """
        var_zs = []
        var_z = output_z - variables[2]
        if var_z % variables[1] != 0:
            return []
        var_z = var_z // variables[1]
        divnum = self.codenum[num_id][4][2]
        for i in range(0, divnum):
            # recompute output z for computed inputz
            input_z = var_z * divnum + i
            control_z = self.run_codenum(num_id, {'x': 0, 'y': 0, 'z': input_z, 'w': 0, 'bufer': ''}, char)
            if control_z == output_z:
                var_zs.append(input_z)
        return var_zs

    def trace_z(self):
        """
        Trace allowed z values and reconstruct the maximum number allowed
        """
        target_zs = []
        target_zs.append({'target_z': 0, 'buffer': '', 'code_index': 13})
        history = []
        i = 0
        while target_zs:
            act_z = target_zs.pop()
            new_zs = []
            for check_z in range(26):
                for check_inp in range(1, 10):
                    variables = self.get_partnum(act_z['code_index'], check_z, check_inp)
                    possible_zs = self.get_inputs_zs(act_z['code_index'], act_z['target_z'], variables, check_inp)
                    for possible in possible_zs:
                        new_z = {'target_z': possible, 'buffer': str(check_inp) + act_z['buffer'], 'code_index': act_z['code_index'] - 1}
                        if new_z in new_zs or new_z in target_zs or new_z in history:
                            continue
                        new_zs.append(new_z)
                        if len(new_z['buffer']) == 14:
                            return new_z['buffer']
            target_zs += new_zs
            i += 1
            if i % 10000 == 0:
                print(".", end="", flush=True)

    def trace_z_reverse(self):
        """
        Trace allowed z values and reconstruct the maximum number allowed
        """
        target_zs = []
        target_zs.append({'target_z': 0, 'buffer': '', 'code_index': 13})
        history = []
        i = 0
        while target_zs:
            act_z = target_zs.pop()
            new_zs = []
            for check_z in range(26):
                for check_inp in range(1, 10):
                    variables = self.get_partnum(act_z['code_index'], check_z, check_inp)
                    possible_zs = self.get_inputs_zs(act_z['code_index'], act_z['target_z'], variables, check_inp)
                    for possible in possible_zs:
                        new_z = {'target_z': possible, 'buffer': str(check_inp) + act_z['buffer'], 'code_index': act_z['code_index'] - 1}
                        if new_z in new_zs or new_z in target_zs or new_z in history:
                            continue
                        new_zs.append(new_z)
                        if len(new_z['buffer']) == 14:
                            return new_z['buffer']
            target_zs += new_zs[::-1]
            i += 1
            if i % 10000 == 0:
                print(".", end="", flush=True)


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

    # process data
    obj = ElfALU(lines)
    max_number = obj.trace_z()
    # part 1
    print(f"\nPart 1 solution: {max_number}")
    min_number = obj.trace_z_reverse()
    # part 1
    print(f"\nPart 2 solution: {min_number}")


if __name__ == '__main__':
    main()

# EOF
