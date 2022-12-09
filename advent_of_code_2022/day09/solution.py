#!/usr/bin/env python
# -*- coding:utf-8 -*-
"""
Advent of code 2022 - Day 9
"""

import argparse


def get_args():
    """
    Cmd line argument parsing (preprocessing)
    """
    # Assign description to the help doc
    parser = argparse.ArgumentParser(
        description='Advent of code 2022: Day 9')

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


delta = {
    'L': [-1, 0],
    'R': [1, 0],
    'D': [0, 1],
    'U': [0, -1],
}


def simulate_moves(moves):
    """
    Simulate rope moves
    """
    head = [0, 0]
    tail = [0, 0]
    hist = {(0, 0)}
    for move in moves:
        for _ in range(0, move[1]):
            # move head
            head[0] += delta[move[0]][0]
            head[1] += delta[move[0]][1]
            # move tail
            vect = [head[0] - tail[0], head[1] - tail[1]]
            if abs(vect[0]) > 1 or abs(vect[1]) > 1:
                if vect[0] != 0:
                    tail[0] += vect[0]//abs(vect[0])
                if vect[1] != 0:
                    tail[1] += vect[1]//abs(vect[1])
                hist.add((tail[0], tail[1]))
    return hist


def visualize_rope(rope):
    """
    Visualize rope
    """
    for jdx in range(-15, 15):
        line = ''
        for idx in range(-15, 15):
            if [idx, jdx] in rope:
                line += f'{rope.index([idx, jdx])}'
            else:
                line += '.'
        print(line)
    print('\n')


def simulate_moves_long(moves, ropelen, visualize=False):
    """
    Simulate rope moves for given length of rope
    """
    # initialize rope
    rope = []
    for _ in range(0, ropelen):
        rope.append([0, 0])

    hist = {(0, 0)}
    for move in moves:
        if visualize:
            print(f'MOVE {move}')
        for _ in range(0, move[1]):
            # move head
            rope[0][0] += delta[move[0]][0]
            rope[0][1] += delta[move[0]][1]
            # move one by one
            for idx in range(1, ropelen):
                vect = [
                    rope[idx-1][0] - rope[idx][0],
                    rope[idx-1][1] - rope[idx][1]
                ]
                if abs(vect[0]) > 1 or abs(vect[1]) > 1:
                    if vect[0] != 0:
                        rope[idx][0] += vect[0]//abs(vect[0])
                    if vect[1] != 0:
                        rope[idx][1] += vect[1]//abs(vect[1])
                else:
                    # no move = rest of rope stay calm
                    break
            hist.add((rope[-1][0], rope[-1][1]))
        if visualize:
            visualize_rope(rope)
    return hist


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

    # prepare data
    moves = []
    for line in lines:
        direction, number = line.split(' ')
        moves.append([direction, int(number)])

    # evaluate part 1
    tail = simulate_moves(moves)
    res = len(tail)
    print("Part 1 solution: {}".format(res))

    # evaluate part 2
    tail = simulate_moves_long(moves, 10, False)
    res = len(tail)
    print("Part 2 solution: {}".format(res))


if __name__ == '__main__':
    main()

# EOF
