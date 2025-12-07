#!/usr/bin/env python
# -*- coding:utf-8 -*-
"""
Advent of Code solution
"""

import argparse


def get_args():
    """
    Cmd line argument parsing (preprocessing)
    """
    # Assign description to the help doc
    parser = argparse.ArgumentParser(
        description='Advent of code 2025 day 7')

    # Add arguments
    parser.add_argument(
        '-i',
        '--infile',
        type=str,
        help='Input filename',
        required=True)

    # Array for all arguments passed to script
    args = parser.parse_args()

    # Return arg variables
    return args.infile


def read_data(filename):
    """
    read input data
    """
    data = []
    with open(filename, "r", encoding="utf8") as fhnd:
        data = fhnd.readlines()
    data = [x.strip() for x in data]

    start = []
    for idx, value in enumerate(data[0]):
        if value == 'S':
            start = idx
            break

    splitters = []
    for item in data[1:]:
        act = []
        for idx, value in enumerate(item):
            if value == '^':
                act.append(idx)
        splitters.append(act)
    return start, splitters


def trace_beams(start, data):
    """
    make part 1 beams tracing
    """
    archive = []
    process = [start]
    for split in data:
        if not split:
            continue
        new = []
        for ray in process:
            if ray in split:
                # two new rays created + old ray to archive
                if ray - 1 not in new:
                    new.append(ray - 1)
                if ray + 1 not in new:
                    new.append(ray + 1)
                archive.append(ray)
            else:
                # ray is continuous (no split)
                if ray not in new:
                    new.append(ray)
        process = new
    return len(archive)


def trace_quantum_beams(start, data):
    """
    make part 2 beams tracing
    """
    process = {start: 1}
    for split in data:
        if not split:
            continue
        new = {}
        for ray, occ in process.items():
            if ray in split:
                # two new rays created
                if ray - 1 not in new:
                    new[ray - 1] = 0
                new[ray - 1] += 1 * occ
                if ray + 1 not in new:
                    new[ray + 1] = 0
                new[ray + 1] += 1 * occ
            else:
                # ray is continuous (no split)
                if ray not in new:
                    new[ray] = 0
                new[ray] += occ
        process = new
    sums = 0
    for item in new.values():
        sums += item

    return sums


def main():
    """
    main
    """

    filename = get_args()
    start, data = read_data(filename)

    # part 1
    sums = trace_beams(start, data)
    print(f"Solution part 1: {sums}")

    # part 2
    sums = trace_quantum_beams(start, data)
    print(f"Solution part 2: {sums}")


if __name__ == '__main__':
    main()

# EOF
