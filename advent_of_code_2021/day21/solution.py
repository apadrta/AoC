#!/usr/bin/env python
# -*- coding:utf-8 -*-
"""
Advent of code 2021 - Day 21
"""

import argparse
from copy import deepcopy


numnum = {3: 1, 4: 3, 5: 6, 6: 7, 7: 6, 8: 3, 9: 1}


def get_args():
    """
    Cmd line argument parsing (preprocessing)
    """
    # Assign description to the help doc
    parser = argparse.ArgumentParser(
        description='Advent of code 2021: Day 21')

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


def play_deterministic_game(start_a, start_b):
    """
    Play one deterministic game
    """
    score = [0, 0]
    rolls = 0
    player = -1
    # reindex from zero
    pos = [start_a-1, start_b-1]
    last_dice = 0
    i = 0
    while score[0] < 1000 and score[1] < 1000:
        # determine player
        player = (player + 1) % 2
        moves = (last_dice + 1) % 100 + (last_dice + 2) % 100 + (last_dice + 3) % 100
        last_dice = (last_dice + 3) % 100
        rolls += 3
        pos[player] = (pos[player] + moves) % 10
        score[player] += pos[player] + 1
        i += 1
        if i > 1000:
            break
    return rolls * min(score)


def play_dirac_game(start_a, start_b):
    """
    Play one dirac game
    """
    states = {}
    states[(start_a - 1, start_b - 1, 0, 0)] = 1
    # state = (pos A, pos B, score A, score B)
    win_a = 0
    win_b = 0
    while states:
        # process player A
        new_states = {}
        for [pos_a, pos_b, score_a, score_b], value in states.items():
            for numkey, numvalue in numnum.items():
                newpos = (pos_a + numkey) % 10
                newscore = score_a + newpos + 1
                if (newpos, pos_b, newscore, score_b) not in new_states:
                    new_states[(newpos, pos_b, newscore, score_b)] = 0
                new_states[(newpos, pos_b, newscore, score_b)] += value * numvalue
        states = deepcopy(new_states)
        for [pos_a, pos_b, score_a, score_b], value in new_states.items():
            if score_a > 20:
                win_a += value
                del states[(pos_a, pos_b, score_a, score_b)]
        # process player B
        new_states = {}
        for [pos_a, pos_b, score_a, score_b], value in states.items():
            for numkey, numvalue in numnum.items():
                newpos = (pos_b + numkey) % 10
                newscore = score_b + newpos + 1
                if (pos_a, newpos, score_a, newscore) not in new_states:
                    new_states[(pos_a, newpos, score_a, newscore)] = 0
                new_states[(pos_a, newpos, score_a, newscore)] += value * numvalue
        states = deepcopy(new_states)
        for [pos_a, pos_b, score_a, score_b], value in new_states.items():
            if score_b > 20:
                win_b += value
                del states[(pos_a, pos_b, score_a, score_b)]
        print(".", end='', flush=True)
    return win_a


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
    start_a = int(lines[0].split(": ")[1])
    start_b = int(lines[1].split(": ")[1])

    # part 1
    print(f"\nPart 1 solution: {play_deterministic_game(start_a, start_b)}")
    # part 2
    print(f"\nPart 2 solution: {play_dirac_game(start_a, start_b)}")


if __name__ == '__main__':
    main()

# EOF
