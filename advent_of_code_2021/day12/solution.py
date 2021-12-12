#!/usr/bin/env python
# -*- coding:utf-8 -*-
"""
Advent of code 2021 - Day 12
"""

import argparse


def get_args():
    """
    Cmd line argument parsing (preprocessing)
    """
    # Assign description to the help doc
    parser = argparse.ArgumentParser(
        description='Advent of code 2021: Day 12')

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


def can_i_visit(path, move):
    """
    Check if move is first doubled
    """
    if move == 'start':
        return False
    checks = []
    doubles = 0
    for step in path + [move]:
        if step[0].islower():
            if step not in checks:
                checks.append(step)
            else:
                doubles += 1
    if doubles > 1:
        return False
    return True


class ElfNavigation():
    """
    Class for cave path navigation
    """

    def __init__(self, scan):
        """
        Cosntructor
        """
        self.data = []
        for item in scan:
            self.data.append(item)
            self.data.append([item[1], item[0]])

    def find_paths(self):
        """
        Find number of paths
        """
        paths = [['start']]
        complete_paths = []
        while paths:
            path = paths.pop()
            for move in self.data:
                if move[0] == path[-1]:
                    if move[1][0].islower() and move[1] in path:
                        continue
                    new_path = path + [move[1]]
                    if move[1] == 'end':
                        complete_paths.append(new_path)
                    if new_path not in paths:
                        paths.append(new_path)
        return len(complete_paths)

    def find_paths2(self):
        """
        Find number of paths for second part
        """
        paths = [['start']]
        complete_paths = []
        while paths:
            path = paths.pop()
            for move in self.data:
                if move[0] == path[-1]:
                    if not can_i_visit(path, move[1]):
                        continue
                    new_path = path + [move[1]]
                    if move[1] == 'end':
                        complete_paths.append(new_path)
                        continue
                    if new_path not in paths:
                        paths.append(new_path)
        return len(complete_paths)


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
    navdata = []
    for line in lines:
        navdata.append(line.split("-"))

    # part 1
    nav = ElfNavigation(navdata)
    print(f"Part 1 solution: {nav.find_paths()}")

    # part 2
    print(f"Part 2 solution: {nav.find_paths2()}")


if __name__ == '__main__':
    main()

# EOF
