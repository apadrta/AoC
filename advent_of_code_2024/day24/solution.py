#!/usr/bin/env python
# -*- coding:utf-8 -*-
"""
Advent of code 2024 - Day 24
"""

import argparse


def get_args():
    """
    Cmd line argument parsing (preprocessing)
    """
    # Assign description to the help doc
    parser = argparse.ArgumentParser(
        description='Advent of code 2024: Day 24'
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
    Read data from file and convert it to data structure
    """
    data = []
    with open(filename, "r", encoding="utf-8") as fileh:
        data = fileh.readlines()
    data = [x.strip() for x in data]

    cables = {}
    gates = {}
    for item in data:
        if not item:
            continue
        if ":" in item:
            name, value = item.split(": ")
            cables[name] = int(value)
            continue
        if "->" in item:
            parts = item.split(" ")
            gates[parts[4]] = [parts[1], parts[0], parts[2]]
    return cables, gates


def get_wiring(gates):
    """
    get all targets for each cable
    """
    wiring = {}
    for key, value in gates.items():
        if value[1] not in wiring:
            wiring[value[1]] = []
        wiring[value[1]].append(key)
        if value[2] not in wiring:
            wiring[value[2]] = []
        wiring[value[2]].append(key)
    return wiring


def eval_gate(gatetype, input1, input2):
    """
    evaluate gate
    """
    if gatetype == 'AND':
        return input1 & input2
    if gatetype == 'OR':
        return input1 | input2
    if gatetype == 'XOR':
        return input1 ^ input2
    return 0


def eval_wiring(gates, cables, wiring):
    """
    return final values of cables
    """
    work_cables = cables
    eval_gates = list(gates.keys())
    while eval_gates:
        check_gates = []
        for check in work_cables:
            if check not in wiring:
                continue
            for target in wiring[check]:
                if target not in check_gates:
                    check_gates.append(target)
        work_cables = []
        for check in check_gates:
            if gates[check][1] in cables and gates[check][2] in cables:
                cables[check] = eval_gate(gates[check][0], cables[gates[check][1]], cables[gates[check][2]])
                work_cables.append(check)
                if check in eval_gates:
                    eval_gates.remove(check)
    return cables


def eval_result(cables, resid):
    """
    evaluate results
    """
    finals = []
    for cable in cables.keys():
        if cable[0] == resid:
            finals.append(cable)
    finals = sorted(finals)
    res = 0
    for fin in finals[::-1]:
        res = res << 1
        res += cables[fin]
    return res


def eval_dependencies(gates, target, maxcnt=10):
    """
    evaluate dependencies of target
    """
    print(f'  wiring for {target}')
    deps = []
    states = [target]
    cnt = 0
    while states:
        if cnt > maxcnt:
            break
        cnt += 1
        if states[0] in deps:
            continue
        state = states.pop(0)
        if state not in gates:
            continue
        print(f'    gate {state}: {gates[state]}')
        states.append(gates[state][1])
        states.append(gates[state][2])


def check_cables(gates, cables, wiring):
    """
    check cables
    """
    tests = []
    for idx in range(0, 3):
        for jdx in range(0, 3):
            tests.append([idx, jdx, idx + jdx])

    pos = 0
    analyze = []
    while pos < 44:
        print(f'  Testing position {pos}')
        for test in tests:
            for idx in range(0, 45):
                cables[f'x{idx:02d}'] = 0
                cables[f'y{idx:02d}'] = 0
            cables[f'x{pos:02d}'] = test[0] & 0b1
            cables[f'y{pos:02d}'] = test[1] & 0b1
            cables[f'x{pos+1:02d}'] = (test[0]) >> 1 & 0b1
            cables[f'y{pos+1:02d}'] = (test[1] >> 1) & 0b1
            cables = eval_wiring(gates, cables, wiring)
            if cables[f'z{pos:02d}'] != (test[2] & 0b1) or cables[f'z{pos+1:02d}'] != ((test[2] >> 1) & 0b1):
                print(f'    -> Error (expected {test[2]}, seen {(cables[f"z{pos+1:02d}"] << 1) + cables[f"z{pos:02d}"]} in test {test})')
                if pos not in analyze:
                    analyze.append(pos)
        pos += 1
    return analyze


def main():
    """
    Main function
    """

    # process args
    infile = get_args()

    # read data
    cables, gates = read_data(infile)

    # part 1
    wiring = get_wiring(gates)
    cables = eval_wiring(gates, cables, wiring)
    sums = eval_result(cables, 'z')
    print(f"Part 1 solution: {sums}")

    # part 2
    print('Automatic detection of bad adding')
    analyze = check_cables(gates, cables, wiring)
    if analyze:
        print(f'Errors found on {len(analyze)} positions')
        print('Details for further manual analysis:')
    else:
        print('Wiring is OK.')
    for item in analyze:
        eval_dependencies(gates, f'z{item+1:02d}')
    print("Part 2 solution: cph,gws,hgj,nnt,npf,z13,z19,z33 (solved manually based on displayed information)")


if __name__ == '__main__':
    main()

# EOF
