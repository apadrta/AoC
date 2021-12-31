#!/usr/bin/env python
# -*- coding:utf-8 -*-
"""
Advent of code 2021 - Day 23
"""

import argparse
from copy import deepcopy


def get_args():
    """
    Cmd line argument parsing (preprocessing)
    """
    # Assign description to the help doc
    parser = argparse.ArgumentParser(
        description='Advent of code 2021: Day 23')

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


correct_roommate = {0: 'A', 1: 'B', 2: 'C', 3: 'D'}
correct_room = {'A': 0, 'B': 1, 'C': 2, 'D':3}
energy_cost = {'A': 1, 'B': 10, 'C': 100, 'D': 1000}


moves_r2h = [[0, 1], [0, 2], [1, 2], [1, 3], [2, 3], [2, 4], [3, 4], [3, 5]]
moves_h2r = [[0, 1], [0, 2], [1, 2], [1, 3], [2, 3], [2, 4], [3, 4], [3, 5]]


class ElfHomework():
    """
    Class for solving Amphipods problems
    """

    def __init__(self, lines):
        """
        Constructor
        """
        self.roomsize = len(lines)
        self.rooms = [[], [], [], []]
        for line in lines[::-1]:
            i = 0
            for char in line:
                if char in 'ABCD': 
                    self.rooms[i].append(char)
                    i += 1
        self.free = [-1, -1, -1, -1]
        for index, room in enumerate(self.rooms):
            correct = 0
            for amphipod in room:
                if amphipod == correct_roommate[index]:
                    correct += 1
            if correct == self.roomsize:
                self.free[index] = 0
        self.halls = [[], [], [], [], [], [], []]
        init_moves = []
        for room in range(4):
            for hall in range(7):
                init_moves.append([room, hall])
        self.init_state = [
            self.rooms,
            self.halls,
            self.free,
            0, 
            [],
            init_moves]

    def solve(self):
        """
        Solve the homework
        """
        states = [self.init_state]
        i = 0
        minnum = -1
        while states:
            # check if last state is solution
            if states[-1][2] == [0, 0, 0, 0]:
                if minnum == -1 or minnum > states[-1][3]:
                    minnum = states[-1][3]
                    print(f"\n new min. energy = {minnum}")
                states.pop()
                continue
            # check if last state is blind way (no further move is possible, go back)
            if not states[-1][4] and not states[-1][5]:
                states.pop()
                continue
            # optimalization - scratch state with higher energy than surrent minimum
            if minnum > -1 and states[-1][3] >= minnum:
                states.pop()
                continue
            # make move to the depth
            new_state = deepcopy(states[-1])
            # move - if somebody in last state can move from hall to home, do it
            if states[-1][4]:
                # perform move
                [start_pos, end_pos] = states[-1][4].pop()
                amphipod = new_state[1][start_pos].pop()
                new_state[0][end_pos].append(amphipod)
                # perform free computation
                new_state[2][end_pos] -= 1
                # perform energy computation
                path_len = self.roomsize - len(states[-1][0][end_pos]) - 1
                path_len += int(0.5 + abs(end_pos +1.5 - start_pos)) * 2
                if start_pos == 0 or start_pos == 6:
                    path_len -=1        
                new_state[3] = states[-1][3] + energy_cost[amphipod] * path_len
            # move (from home to hall)
            elif states[-1][5]:
                # perform move
                [start_pos, end_pos] = states[-1][5].pop()
                amphipod = new_state[0][start_pos].pop()
                new_state[1][end_pos].append(amphipod)
                # perform free computation
                bad_roommate = False
                for room_amphipod in new_state[0][start_pos]:
                    if room_amphipod != correct_roommate[start_pos]:
                        bad_roommate = True
                        break
                if not bad_roommate:
                    new_state[2][start_pos] = self.roomsize - len(new_state[0][start_pos])
                # perform energy computation
                path_len = self.roomsize - len(states[-1][0][start_pos])      
                path_len += int(0.5 + abs(start_pos +1.5 - end_pos)) * 2
                if end_pos == 0 or end_pos == 6:
                    path_len -=1
                new_state[3] = states[-1][3] + energy_cost[amphipod] * path_len
            # recompute newly created state moves (new moves - hall to rooms, [4])
            new_state[4] = []
            for index_h, hall in enumerate(new_state[1]):
                if not hall:
                    # empty hall
                    continue
                index_r = correct_room[hall[-1]]
                if new_state[2][index_r] <= 0:
                    # correct room not ready to accomodate amphipod
                    continue
                # check free path
                if index_r + 1 < index_h:
                    # left move
                    blocked = False
                    for index in range(index_h -1, index_r +1, -1):
                        if new_state[1][index]:
                            blocked = True
                            break
                    if blocked:
                        continue
                else:
                    # right move
                    blocked = False
                    for index in range(index_h +1, index_r +2):
                        if new_state[1][index]:
                            blocked = True
                            break
                if blocked:
                    continue
                new_state[4].append([index_h, index_r])
            # recompute newly created state moves (new moves - rooms to halls, [5])
            new_state[5] = []
            for index_r, room in enumerate(new_state[0]):
                if not room:
                    # empty room
                    continue
                if room[-1] == correct_roommate[index_r] and new_state[2][index_r] != -1:
                    # do not leave correct room
                    continue
                # left moves
                for index_h in range(index_r + 1, -1, -1):
                    if new_state[1][index_h]:
                        # hall blocked (no further move also possible)
                        break
                    new_state[5].append([index_r, index_h])
                # rught moves
                for index_h in range(index_r + 2, 7):
                    if new_state[1][index_h]:
                        # hall blocked (no further move also possible)
                        break
                    new_state[5].append([index_r, index_h])

            # add new state to states
            states.append(new_state)
            i += 1
            if i % 10000 == 0:
                print(".", end="", flush=True)

        return minnum


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

    # part 1
    obj = ElfHomework([lines[2]]+[lines[3]])
    energy = obj.solve()
    print(f"\nPart 1 solution: {energy}")

    # part 2
    obj = ElfHomework([lines[2]] + ['#D#C#B#A#'] + ['#D#B#A#C#'] + [lines[3]])
    obj.solve()
    print(f"\nPart 2 solution: {energy}")


if __name__ == '__main__':
    main()

# EOF
