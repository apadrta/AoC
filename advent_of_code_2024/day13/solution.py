#!/usr/bin/env python
# -*- coding:utf-8 -*-
"""
Advent of code 2024 - Day 13
"""

import argparse
from sympy import symbols, Eq, solve


def get_args():
    """
    Cmd line argument parsing (preprocessing)
    """
    # Assign description to the help doc
    parser = argparse.ArgumentParser(
        description='Advent of code 2024: Day 13'
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
    arcades = []
    for item in data:
        if "Button A" in item:
            arcade = {}
            nums = item[10:].split(", ")
            arcade["A"] = [int(x[2:]) for x in nums]
        elif "Button B" in item:
            nums = item[10:].split(", ")
            arcade["B"] = [int(x[2:]) for x in nums]
        elif "Prize:" in item:
            nums = item[7:].split(", ")
            arcade["P"] = [int(x[2:]) for x in nums]
            arcades.append(arcade)
    return arcades


def eval_machine(data):
    """
    Evalate pressing machine buttons
    """
    # solve system of equations
    varx, vary = symbols('varx vary')
    eq1 = Eq(data["A"][0] * varx + data["B"][0] * vary, data["P"][0])
    eq2 = Eq(data["A"][1] * varx + data["B"][1] * vary, data["P"][1])
    solution = solve((eq1, eq2), (varx, vary))

    # process output
    if solution[varx] < 0 or solution[vary] < 0:
        return None
    if int(solution[varx])*data["A"][0] + int(solution[vary])*data["B"][0] != data["P"][0]:
        return None
    return [int(solution[varx]), int(solution[vary])]


def main():
    """
    Main function
    """

    # process args
    infile = get_args()

    # read data
    data = read_data_struct(infile)

    # part 1
    sums = 0
    for claw in data:
        solution = eval_machine(claw)
        if solution:
            sums += 3 * solution[0] + solution[1]
    print(f"Part 1 solution: {sums}")

    # part 2
    for idx, value in enumerate(data):
        data[idx]["P"] = [x + 10000000000000 for x in value["P"]]
    sums = 0
    for claw in data:
        solution = eval_machine(claw)
        if solution:
            sums += 3 * solution[0] + solution[1]
    print(f"Part 2 solution: {sums}")


if __name__ == '__main__':
    main()

# EOF
