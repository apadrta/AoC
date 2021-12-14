#!/usr/bin/env python
# -*- coding:utf-8 -*-
"""
Advent of code 2019 - Day 17
"""


import argparse
import numpy as np
from elfcpu import ElfCPU


def get_args():
    """
    Cmd line argument parsing (preprocessing)
    """
    # Assign description to the help doc
    parser = argparse.ArgumentParser(
        description='Advent of code 2019 - Day 17')

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


def get_crossings(array):
    """
    Get number of crossing
    """
    border_diffs = [(-1, 0), (1, 0), (0, -1), (0, 1)]
    crossings = []
    i = 0
    while i < np.size(array, 0):
        j = 0
        while j < np.size(array, 1):
            robs = 0
            for diff in border_diffs:
                if (i == 0 and diff[0] == -1) or (i == np.size(array, 0) - 1 and diff[0] == 1):
                    continue
                if (j == 0 and diff[1] == -1) or (j == np.size(array, 1) - 1 and diff[1] == 1):
                    continue
                if array[(i + diff[0], j + diff[1])] != 46 and array[(i, j)] != 46:
                    robs += 1
            if robs == 4:
                crossings.append((i, j))
            j += 1
        i += 1
    return crossings


def left_or_right(array, begin, facing):
    """
    Decide if turn left or right
    """
    facings = {
        ord('^'): {'L': (-1, 0), 'P': (1, 0)},
        ord('>'): {'L': (0, -1), 'P': (0, 1)},
        ord('v'): {'L': (1, 0), 'P': (-1, 0)},
        ord('<'): {'L': (0, 1), 'P': (0, -1)}
        }
    for key, value in facings[facing].items():
        if (begin[0] + value[0]) < 0 or (begin[0] + value[0]) >= np.size(array, 0):
            continue
        if (begin[1] + value[1]) < 0 or (begin[1] + value[1]) >= np.size(array, 1):
            continue
        if array[(begin[0] + value[0], begin[1] + value[1])] == 35:
            return key
    return 'N'


def how_long(array, begin, facing):
    """
    Count number of steps to go forward
    """
    facings = {
        ord('^'): (0, -1),
        ord('>'): (1, 0),
        ord('v'): (0, 1),
        ord('<'): (-1, 0)
        }
    steps = 0
    pos = list(begin)
    while True:
        pos = (pos[0] + facings[facing][0], pos[1] + facings[facing][1])
        if pos[0] < 0 or pos[0] >= np.size(array, 0) or pos[1] < 0 or pos[1] >= np.size(array, 1) or array[(pos)] != 35:
            break
        steps += 1
    return steps


def prepare_path(array):
    """
    Prepare path for algorithm generation
    """
    startstr = [ord('^'), ord('>'), ord('v'), ord('<')]
    turn_l = {
        ord('^'): ord('<'),
        ord('<'): ord('v'),
        ord('v'): ord('>'),
        ord('>'): ord('^')
        }
    turn_r = {
        ord('^'): ord('>'),
        ord('>'): ord('v'),
        ord('v'): ord('<'),
        ord('<'): ord('^')
        }
    move_change = {
        ord('^'): (0, -1),
        ord('>'): (1, 0),
        ord('v'): (0, 1),
        ord('<'): (-1, 0)
        }
    begin = (0, 0)
    facing = 0
    i = 0
    while i < np.size(array, 0):
        j = 0
        while j < np.size(array, 1):
            if array[(i, j)] in startstr:
                begin = (i, j)
                facing = array[(i, j)]
                break
            j += 1
        i += 1
    commands = ''
    while True:
        # check turn
        turn = left_or_right(array, begin, facing)
        if turn == 'N':
            commands += "N"
            break
        if turn == 'L':
            facing = turn_l[facing]
            commands += "L,"
        else:
            facing = turn_r[facing]
            commands += "R,"
        # check forward
        moves = how_long(array, begin, facing)
        commands += str(moves) + ","
        begin = (begin[0] + move_change[facing][0] * moves, begin[1] + move_change[facing][1] * moves)
    return commands


def split_command(command, maxlen):
    """
    Split command to subprocesses A, B, C and create main code (limit length of all strings)
    """
    cmd = command.split(",")
    cmd_a = ''
    cmd_b = ''
    for i in range(1, maxlen//2 + 1):
        cmd_a = cmd[:(i)]
        cmd_a_str = ','.join(str(x) for x in cmd_a)
        for j in range(1, maxlen//2 + 1):
            cmd_b = cmd[(-j):]
            cmd_b_str = ','.join(str(x) for x in cmd_b)
            tmp = command.replace(cmd_a_str, "|").replace(cmd_b_str, "|")
            if '12' not in tmp:
                wrk = [x for x in tmp.split("|") if x]
                wrk_set = set()
                for item in wrk:
                    if not item:
                        continue
                    if item[0] == ',':
                        item = item[1:]
                    if not item:
                        continue
                    if item[-1] == ',':
                        item = item[:-1]
                    wrk_set.add(item)
                if len(wrk_set) == 1:
                    cmd_c_str = list(wrk_set)[0]
                    if cmd_a_str[-1] == ",":
                        cmd_a_str = cmd_a_str[:-1]
                    if cmd_b_str[-1] == ",":
                        cmd_b_str = cmd_b_str[:-1]
                    if cmd_c_str[-1] == ",":
                        cmd_c_str = cmd_c_str[:-1]
                    cmd_main = command.replace(cmd_a_str, "A").replace(cmd_b_str, "B").replace(cmd_c_str, "C")
                    if cmd_main[-1] == ",":
                        cmd_main = cmd_main[:-1]
                    return [cmd_main, cmd_a_str, cmd_b_str, cmd_c_str]
    return []


def main():
    """
    Main function
    """

    # process args
    filename = get_args()

    # prepare data for further processing
    cpu = ElfCPU()
    cpu.read_code(filename)
    cpu.run()
    reply = cpu.get_output()
    lines = (''.join(chr(x) for x in reply)).splitlines()

    robots = np.zeros((len(lines[0]), len(lines)), dtype=int)
    i = 0
    for line in lines:
        j = 0
        for char in line:
            robots[(j, i)] = ord(char)
            j += 1
        i += 1

    # part 1
    crossings = get_crossings(robots)
    numsum = 0
    for crossing in crossings:
        numsum += (crossing[0]) * (crossing[1])
        lines[crossing[1]] = lines[crossing[1]][:crossing[0]] + 'O' + lines[crossing[1]][crossing[0]+1:]
    # print the array with crossing
    for line in lines:
        print(line)

    print(f"Solution of part 1: {numsum}")

    # part 2
    # prepare path
    path = prepare_path(robots)
    commands = split_command(path[:-1], 20)
    cmd_arr = []
    for cmd in commands:
        cmd_arr += [ord(x) for x in cmd+'\n']
    # run robot
    cpu = ElfCPU()
    cpu.read_code(filename)
    cpu.code[0] = 2
    cpu.set_inputs(cmd_arr)
    cpu.run()
    cpu.set_inputs([ord('n'), ord('\n')])
    cpu.run()
    out = cpu.get_output()
    print(''.join(chr(x) for x in out[:-1]))
    print(f"Solution of part 2: {out[-1]}")


if __name__ == '__main__':
    main()

# EOF
