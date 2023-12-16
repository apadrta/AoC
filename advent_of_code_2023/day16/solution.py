#!/usr/bin/env python
# -*- coding:utf-8 -*-
"""
Advent of code 2023 - Day 16
"""

import argparse


def get_args():
    """
    Cmd line argument parsing (preprocessing)
    """
    # Assign description to the help doc
    parser = argparse.ArgumentParser(
        description='Advent of code 2023: Day 16'
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

    return data


def trace_ray(data, raydef):
    """
    trace ray throug the device
    """
    rays = [raydef]
    visited = {}

    while rays:
        ray = rays.pop()
        while True:
            # move to next tile
            if ray[2] == 'right':
                ray[1] += 1
            elif ray[2] == 'left':
                ray[1] -= 1
            elif ray[2] == 'down':
                ray[0] += 1
            else:  # up
                ray[0] -= 1
            # quit when next tile out of limit
            if not (0 <= ray[0] < len(data) and 0 <= ray[1] < len(data[0])):
                break
            # modify ray
            if data[ray[0]][ray[1]] == '|' and ray[2] in ['left', 'right']:
                rays.append([ray[0], ray[1], 'up'])
                ray[2] = 'down'
            elif data[ray[0]][ray[1]] == '-' and ray[2] in ['up', 'down']:
                rays.append([ray[0], ray[1], 'left'])
                ray[2] = 'right'
            elif data[ray[0]][ray[1]] == '/':
                if ray[2] == 'right':
                    ray[2] = 'up'
                elif ray[2] == 'up':
                    ray[2] = 'right'
                elif ray[2] == 'left':
                    ray[2] = 'down'
                elif ray[2] == 'down':
                    ray[2] = 'left'
            elif data[ray[0]][ray[1]] == '\\':
                if ray[2] == 'right':
                    ray[2] = 'down'
                elif ray[2] == 'down':
                    ray[2] = 'right'
                elif ray[2] == 'left':
                    ray[2] = 'up'
                elif ray[2] == 'up':
                    ray[2] = 'left'
            # process result
            if (ray[0], ray[1]) in visited and ray[2] in visited[(ray[0], ray[1])]:
                break
            if (ray[0], ray[1]) not in visited:
                visited[(ray[0], ray[1])] = []
            visited[(ray[0], ray[1])].append(ray[2])

    return len(visited)


def main():
    """
    Main function
    """

    # process args
    infile = get_args()

    # read data
    data = read_data_struct(infile)

    # part 1
    sums = trace_ray(data, [0, -1, 'right'])
    print(f"Part 1 solution: {sums}")

    # part 2
    rays = []
    for idx in range(0, len(data)):
        rays.append([idx, -1, 'right'])
        rays.append([idx, len(data[0]), 'left'])
    for idx in range(0, len(data[0])):
        rays.append([-1, idx, 'down'])
        rays.append([len(data), idx, 'up'])
    maxlight = 0
    for ray in rays:
        sums = trace_ray(data, ray)
        if sums > maxlight:
            maxlight = sums
    print(f"Part 2 solution: {maxlight}")


if __name__ == '__main__':
    main()

# EOF
