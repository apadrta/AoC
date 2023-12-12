#!/usr/bin/env python
# -*- coding:utf-8 -*-
"""
Advent of code 2023 - Day 12
"""

import argparse
import re
from copy import deepcopy


def get_args():
    """
    Cmd line argument parsing (preprocessing)
    """
    # Assign description to the help doc
    parser = argparse.ArgumentParser(
        description='Advent of code 2023: Day 12'
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

    # split information
    records = []
    for line in data:
        chars, nums = line.split(' ')
        records.append([[x for x in chars], [int(x) for x in nums.split(',')]])

    return records


def get_arrangments(record):
    """
    count possible arrangement (part 1 ok)
    """

    # generate possible variants
    buff = [[record[0], 0]]
    res = []
    while buff:
        work, pos = buff.pop(0)
        # pos is/maybe OK (.)
        if pos < len(work) and work[pos] in '.?':
            work1 = deepcopy(work)
            work1[pos] = '.'
            if work1.count('?') == 0:
                res.append(''.join(work1))
            else:
                buff.append([work1, pos + 1])
        # pos is/may be broken (#)
        if pos < len(work) and work[pos] in '#?':
            work[pos] = '#'
            if work.count('?') == 0:
                res.append(''.join(work))
            else:
                buff.append([work, pos + 1])

    # check validity
    valid = 0
    reg = re.compile('#+')
    for item in res:
        # check number of broken
        if sum(record[1]) != item.count('#'):
            continue
        # check numbers placing
        pos = [len(x) for x in reg.findall(item)]
        if pos != record[1]:
            continue
        valid += 1
    return valid


def unfold(data):
    """
    Unfold (multiple by 5) data
    """
    new_data = []
    for item in data:
        new_data.append([((item[0] + ['?']) * 5)[:-1], item[1] * 5])
    return new_data


def get_arrangments2(recdata, recnums):
    """
    count possible arrangement (part2 testing data ok)
    """

    # compute possible positions for block of used lenghts
    posnums = {}
    for num in recnums:
        if num in posnums:
            continue
        posnums[num] = []
        pos = -1
        while pos < len(recdata) - num + 1:
            pos += 1
            if pos > 0 and recdata[pos - 1] == '#':
                # impossible location (previous cannot be .)
                continue
            if pos < len(recdata) - num and recdata[pos + num] == '#':
                # impossible location (next cannot be .)
                continue
            if recdata[pos:pos+num].count('?') + recdata[pos:pos+num].count('#') != num:
                # impossible location (block possition cannot be all #s)
                continue

            posnums[num].append(pos)

    # create initial state
    statepos = []
    lastpos = 0
    for num in recnums:
        for idx, pos in enumerate(posnums[num]):
            if pos >= lastpos:
                lastpos = pos + 1
                statepos.append(idx)
                break
    # process states
    states = [[statepos, len(recnums)]]
    sums = 0
    counter = 0
    pruned = 0
    while states:
        state = states.pop()
        if counter % 100000 == 0:
            print(f'iter={counter}, pruned={pruned}, states={len(states) + 1}, work on {state}', )
        # move by last possible

        state[1] = state[1] - 1
        if state[1] == -1:
            # check non covered #s
            workdata = deepcopy(recdata)
            for idx, value in enumerate(state[0]):
                rep = 'X' * recnums[idx]
                checkpos = posnums[recnums[idx]][value]
                workdata[checkpos:checkpos+recnums[idx]] = rep
            if workdata.count('#') > 0:
                continue
            sums += 1
            continue
        workpos = state[0][state[1]]
        for idx in range(workpos, len(posnums[recnums[state[1]]])):
            # stop when interfering with following item (too big step)
            if state[1] < len(recnums) - 1:
                next_begin = posnums[recnums[state[1]+1]][state[0][state[1]+1]]
                current_end = posnums[recnums[state[1]]][idx] + recnums[state[1]]
                if current_end >= next_begin:
                    break
            # skip given position when some #s are left betwenn current end and next begin
            next_begin = len(recnums) + 1
            if state[1] < len(recnums) - 1:
                next_begin = posnums[recnums[state[1]+1]][state[0][state[1]+1]]
            current_end = posnums[recnums[state[1]]][idx] + recnums[state[1]]
            if recdata[current_end:next_begin].count('#') > 0:
                pruned += 1
                continue
            workstate = deepcopy(state)
            workstate[0][workstate[1]] = idx
            states.append(workstate)
        counter += 1

    return sums


def get_arrangments3(recdata, recnums):
    """
    count possible arrangement (ok for both parts)
    """
    state = {(0, 0): 1}

    for chars in recdata:
        if chars == "?":
            chars = [".", "#"]
        else:
            chars = [chars]

        new_state = {}
        for key, value in state.items():
            # key = (sum of nums, pos)
            for char in chars:
                if key[1] == len(recnums):
                    if char == ".":
                        if (key[0], key[1]) not in new_state:
                            new_state[(key[0], key[1])] = 0
                        new_state[(key[0], key[1])] += value
                else:
                    if key[0] == recnums[key[1]]:
                        if char == ".":
                            if (0, key[1]+1) not in new_state:
                                new_state[(0, key[1]+1)] = 0
                            new_state[(0, key[1]+1)] += value
                    else:
                        if char == "." and key[0] == 0:
                            if (key[0], key[1]) not in new_state:
                                new_state[(key[0], key[1])] = 0
                            new_state[(key[0], key[1])] += value
                        if char == "#":
                            if (key[0]+1, key[1]) not in new_state:
                                new_state[(key[0] + 1, key[1])] = 0
                            new_state[(key[0] + 1, key[1])] += value
        state = new_state

    res = 0
    if (0, len(recnums)) in state:
        res += state[(0, len(recnums))]
    if (recnums[-1], len(recnums)-1) in state:
        res += state[(recnums[-1], len(recnums)-1)]
    return res


def main():
    """
    Main function
    """

    # process args
    infile = get_args()

    # read data
    records = read_data_struct(infile)

    # part 1
    sums = 0
    for record in records:
        sums += get_arrangments3(record[0], record[1])
    print(f"Part 1 solution: {sums}")

    # part 2
    records = read_data_struct(infile)
    records = unfold(records)

    sums = 0
    for record in records:
        sums += get_arrangments3(record[0], record[1])
    print(f"Part 2 solution: {sums}")


if __name__ == '__main__':
    main()

# EOF
