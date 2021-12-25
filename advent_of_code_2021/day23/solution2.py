#!/usr/bin/env python
# -*- coding:utf-8 -*-
"""
Advent of code 2021 - Day 23 part2
"""

import argparse
from copy import deepcopy


def get_args():
    """
    Cmd line argument parsing (preprocessing)
    """
    # Assign description to the help doc
    parser = argparse.ArgumentParser(
        description='Advent of code 2021: Day 23 part2')

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


paths = {
    (0, 7): [1],
    (0, 8): [1, 2],
    (0, 9): [1, 2, 3],
    (0, 10): [1, 2, 3, 4],
    (1, 7): [],
    (1, 8): [2],
    (1, 9): [2, 3],
    (1, 10): [2, 3, 4],
    (2, 7): [],
    (2, 8): [],
    (2, 9): [3],
    (2, 10): [3, 4],
    (3, 7): [2],
    (3, 8): [],
    (3, 9): [],
    (3, 10): [4],
    (4, 7): [2, 3],
    (4, 8): [3],
    (4, 9): [],
    (4, 10): [],
    (5, 7): [2, 3, 4],
    (5, 8): [3, 4],
    (5, 9): [4],
    (5, 10): [],
    (6, 7): [2, 3, 4, 5],
    (6, 8): [3, 4, 5],
    (6, 9): [4, 5],
    (6, 10): [5]}

for index_from in range(7):
    for index_to in range(7, 11):
        for repeat in range(3):
            paths[(index_from, index_to + (repeat+1) * 4)] = deepcopy(paths[(index_from, index_to + repeat * 4)] + [index_to + repeat * 4])

distances = {
    (0, 7): 3,
    (0, 8): 5,
    (0, 9): 7,
    (0, 10): 9,
    (1, 7): 2,
    (1, 8): 4,
    (1, 9): 6,
    (1, 10): 8,
    (2, 7): 2,
    (2, 8): 2,
    (2, 9): 4,
    (2, 10): 6,
    (3, 7): 4,
    (3, 8): 2,
    (3, 9): 2,
    (3, 10): 4,
    (4, 7): 6,
    (4, 8): 4,
    (4, 9): 2,
    (4, 10): 2,
    (5, 7): 8,
    (5, 8): 6,
    (5, 9): 4,
    (5, 10): 2,
    (6, 7): 9,
    (6, 8): 7,
    (6, 9): 5,
    (6, 10): 3,
}

for index_from in range(7):
    for index_to in range(7, 11):
        for repeat in range(3):
            distances[(index_from, index_to + (repeat+1) * 4)] = distances[(index_from, index_to + repeat * 4)] + 1

correct_rooms = {
    1: [19, 15, 11, 7],
    10: [20, 16, 12, 8],
    100: [21, 17, 13, 9],
    1000: [22, 18, 14, 10]}


def place_amphipods(lines):
    """
    Prepare amphipods state/place vector
    """
    state = [0] * 23
    state_order = [7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22]
    last_place = 0
    for char in lines[2] + '#D#C#B#A#' + '#D#B#A#C#' + lines[3]:
        if char == 'A':
            state[state_order[last_place]] = 1
            last_place += 1
        elif char == 'B':
            state[state_order[last_place]] = 10
            last_place += 1
        elif char == 'C':
            state[state_order[last_place]] = 100
            last_place += 1
        elif char == 'D':
            state[state_order[last_place]] = 1000
            last_place += 1
    return state


class ElfAmphipods():
    """
    Class for solving Amphipods problems
    """

    def __init__(self, lines):
        """
        Constructor
        """
        self.states = [[place_amphipods(lines), 0]]
        self.burrow_paths = {}
        for key, value in paths.items():
            self.burrow_paths[key] = value
            self.burrow_paths[(key[1], key[0])] = value
        self.burrow_distances = {}
        for key, value in distances.items():
            self.burrow_distances[key] = value
            self.burrow_distances[(key[1], key[0])] = value

    def generate_moves(self, amphipods):
        """
        Generate possible moves for given amphipods positions
        """
        moves = []
        for from_index, value in enumerate(amphipods):
            if value == 0:
                # empty position (nothing to move)
                continue
            # dont go out, when correctly in home
            correct_homes = correct_rooms[value]
            bad_roommate = False
            for home in correct_homes:
                if amphipods[home] != value and amphipods[home] != 0:
                    bad_roommate = True
                    break
            if from_index in correct_homes and not bad_roommate:
                continue
            # prepare target indexes
            if from_index < 7:
                # position outside rooms -> try to go home
                targets = correct_rooms[value]
                # check if home is free or correctly occupied
                bad_home = False
                for target in targets:
                    if amphipods[target] != 0 and amphipods[target] != value:
                        bad_home = True
                        break
                if bad_home:
                    continue
                # dont go to upper homes when lowers is empty (targets are already sorted from deepest)
                deepest = targets[0]
                for target in targets:
                    if amphipods[target] == 0:
                        deepest = target
                        break
                targets = [deepest]
            else:
                # position inside rooms -> try to go out (only if necessary)
                targets = range(7)
            # process target indexes
            for to_index in targets:
                clear = True
                for node in self.burrow_paths[(from_index, to_index)] + [to_index]:
                    if amphipods[node] > 0:
                        clear = False
                        break
                if clear:
                    move = deepcopy(amphipods)
                    move[to_index] = move[from_index]
                    move[from_index] = 0
                    moves.append([move, move[to_index] * self.burrow_distances[(from_index, to_index)]])
        return moves

    def find_optimal_solution(self):
        """
        Find optimal solution
        """
        final_state = [0, 0, 0, 0, 0, 0, 0, 1, 10, 100, 1000, 1, 10, 100, 1000, 1, 10, 100, 1000, 1, 10, 100, 1000]
        queue = [deepcopy(self.states[0][0])]
        history = []
        energy = {tuple(self.states[0][0]): 0}
        i = 0
        while queue:
            # start with state with minimal energy spent
            state = queue[0]
            for check in queue:
                if energy[tuple(check)] < energy[tuple(state)]:
                    state = check
            # move from queue to history
            queue.remove(state)
            history.append(state)
            # get new possible moves
            new_moves = self.generate_moves(state)
            # process possible moves
            for new_move in new_moves:
                if new_move[0] == final_state:
                    # finished
                    return new_move[1] + energy[tuple(state)]
                if new_move[0] in history:
                    # repeating already known state
                    continue
                if new_move[0] in queue:
                    # get to already queued state
                    energy[tuple(new_move[0])] = min(energy[tuple(new_move[0])], new_move[1] + energy[tuple(state)])
                    continue
                # new state, never seen before
                queue.append(new_move[0])
                energy[tuple(new_move[0])] = new_move[1] + energy[tuple(state)]
            i += 1
            if i % 1000 == 0:
                print(".", end="", flush=True)


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

    # process data
    obj = ElfAmphipods(lines)
    energy = obj.find_optimal_solution()
    print(f"\nPart 2 solution: {energy}")


if __name__ == '__main__':
    main()

# EOF
