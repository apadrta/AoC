#!/usr/bin/env python
# -*- coding:utf-8 -*-
"""
Advent of code 2023 - Day 20
"""

import argparse
import math


def get_args():
    """
    Cmd line argument parsing (preprocessing)
    """
    # Assign description to the help doc
    parser = argparse.ArgumentParser(
        description='Advent of code 2023: Day 20'
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

    wiring = {}
    conjs = {}
    for line in data:
        item, targets = line.split(' -> ')
        iname = 'broadcast'
        itype = 'b'
        if item[0] in '%&':
            iname = item[1:]
            itype = item[0]
        wiring[iname] = [itype, targets.split(', ')]
        if item[0] == '&':
            conjs[iname] = []
    for cname, clist in conjs.items():
        for iname, ilist in wiring.items():
            if cname in ilist[1]:
                clist.append(iname)
    return wiring, conjs


def push_button(wiring, conjs, pushes):
    """
    count pulses
    """

    # prepare state
    state = {}
    for name, details in wiring.items():
        if details[0] == '%':
            state[name] = 0  # off
        elif details[0] == '&':
            state[name] = {}
            for node in conjs[name]:
                state[name][node] = 0  # off

    # run signals
    count = [0, 0]
    for _ in range(0, pushes):
        signals = []
        count[0] += 1
        for target in wiring['broadcast'][1]:
            signals.append(['broadcast', target, 0])
        while signals:
            sig = signals.pop(0)
            count[sig[2]] += 1
            if sig[1] not in wiring:
                continue
            if wiring[sig[1]][0] == '%':
                if sig[2] == 1:
                    continue
                state[sig[1]] = (state[sig[1]] + 1) % 2
                for target in wiring[sig[1]][1]:
                    signals.append([sig[1], target, state[sig[1]]])
            elif wiring[sig[1]][0] == '&':
                state[sig[1]][sig[0]] = sig[2]
                out = 0
                for data in state[sig[1]].values():
                    if data == 0:
                        out = 1
                        break
                for target in wiring[sig[1]][1]:
                    signals.append([sig[1], target, out])

    return count[0] * count[1]


def eval_rx(wiring, conjs):
    """
    count pulses
    """

    # find signal source for rx
    keypart = ''
    for name, data in wiring.items():
        if 'rx' in data[1]:
            keypart = name
            break
    wanted = conjs[keypart]
    found = []

    # prepare state
    state = {}
    for name, details in wiring.items():
        if details[0] == '%':
            state[name] = 0  # off
        elif details[0] == '&':
            state[name] = {}
            for node in conjs[name]:
                state[name][node] = 0  # off

    # run signals
    count = [0, 0]
    jdx = 0
    while wanted:
        jdx += 1
        lowrx = 0
        signals = []
        count[0] += 1
        for target in wiring['broadcast'][1]:
            signals.append(['broadcast', target, 0])
        while signals:
            sig = signals.pop(0)
            count[sig[2]] += 1
            if sig[1] == 'rx' and sig[2] == 0:
                lowrx += 0
            if sig[0] in wanted and sig[2] == 1:
                wanted.remove(sig[0])
                found.append(jdx)
            if sig[1] not in wiring:
                continue
            if wiring[sig[1]][0] == '%':
                if sig[2] == 1:
                    continue
                state[sig[1]] = (state[sig[1]] + 1) % 2
                for target in wiring[sig[1]][1]:
                    signals.append([sig[1], target, state[sig[1]]])
            elif wiring[sig[1]][0] == '&':
                state[sig[1]][sig[0]] = sig[2]
                out = 0
                for data in state[sig[1]].values():
                    if data == 0:
                        out = 1
                        break
                for target in wiring[sig[1]][1]:
                    signals.append([sig[1], target, out])
        # if we are lucky...
        if lowrx == 1:
            return jdx
    # compute first occurence off all ones (to send low to rx)
    res = 1
    for val in found:
        res = math.lcm(res, val)
    return res


def main():
    """
    Main function
    """

    # process args
    infile = get_args()

    # read data
    wiring, conjs = read_data_struct(infile)

    # part 1
    sums = 0
    sums = push_button(wiring, conjs, 1000)
    print(f"Part 1 solution: {sums}")

    # part 2
    count = eval_rx(wiring, conjs)
    print(f"Part 2 solution: {count}")


if __name__ == '__main__':
    main()

# EOF
