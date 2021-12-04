#!/usr/bin/env python
# -*- coding:utf-8 -*-
"""
Advent of code - 15A
"""


import argparse
from copy import deepcopy
from elfcpu import ElfCPU


def get_args():
    """
    Cmd line argument parsing (preprocessing)
    """
    # Assign description to the help doc
    parser = argparse.ArgumentParser(
        description='Advent of code 2019')

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


d_order2turn = {
    'N': 'E',
    'E': 'S',
    'S': 'W',
    'W': 'N'}
d_order2turn_c = {
    'N': 'W',
    'W': 'S',
    'S': 'E',
    'E': 'N'}
d_order2code = {
    'N': 1,
    'S': 2,
    'W': 3,
    'E': 4}
d_code2order = {
    1: 'N',
    2: 'S',
    3: 'W',
    4: 'E'}
d_order2reverse = {
    'N': 'S',
    'S': 'N',
    'W': 'W',
    'E': 'E'}
d_order2delta = {
    'N': (0, -1),
    'S': (0, +1),
    'W': (-1, 0),
    'E': (+1, 0)}


class ElfDroid():
    """
    Elf Droid for exploring the no-oxygen sections
    """

    def __init__(self):
        """
        Constructor
        """
        self.cpu = None
        self.pos = [0, 0]
        self.floor = {(0, 0): '.'}
        self.floor_borders = {'minx': 0, 'maxx': 0, 'miny': 0, 'maxy': 0}

    def init_cpu(self, filename):
        """
        Initialize droid CPU
        """
        self.cpu = ElfCPU()
        self.cpu.read_code(filename)
        self.cpu.run()

    def print_floor(self):
        """
        Print floor pretty
        """
        self.floor[(0, 0)] = 'S'
        for i in range(self.floor_borders['miny'], self.floor_borders['maxy'] + 1):
            out = ''
            for j in range(self.floor_borders['minx'], self.floor_borders['maxx'] + 1):
                if (j, i) in self.floor:
                    out += self.floor[(j, i)]
                else:
                    out += ' '
            print(out)

    def update_floor(self, pos, value):
        """
        Write new data position to floormap
        """
        # add new position data
        if value == 0:
            self.floor[pos] = '#'
        elif value == 1:
            self.floor[pos] = '.'
        elif value == 2:
            self.floor[pos] = 'O'
        # expand borders if necessary
        if pos[0] > self.floor_borders['maxx']:
            self.floor_borders['maxx'] = pos[0]
        if pos[0] < self.floor_borders['minx']:
            self.floor_borders['minx'] = pos[0]
        if pos[1] > self.floor_borders['maxy']:
            self.floor_borders['maxy'] = pos[1]
        if pos[1] < self.floor_borders['miny']:
            self.floor_borders['miny'] = pos[1]

    def __move(self, order):
        """
        Automaticaly Explore floor
        """
        # execute orders
        self.cpu.add_inputs([d_order2code[order]])
        self.cpu.run()
        reply = self.cpu.get_output()[-1]
        # update floor map
        loc = (self.pos[0] + d_order2delta[order][0], self.pos[1] + d_order2delta[order][1])
        self.update_floor(loc, reply)
        # if not wall, update positon
        if reply > 0:
            self.pos[0] += d_order2delta[order][0]
            self.pos[1] += d_order2delta[order][1]
        return reply

    def manual_explore(self, orders):
        """
        Manually explore floor
        """
        for order in orders:
            self.__move(order)

    def auto_explore(self):
        """
        Automaticaly explore floor
        """
        order = 'N'
        i = 0
        oxygen = [0, 0]
        while True:
            i += 1
            if i > 3500:
                break
            # move according to order
            reply = self.__move(order)
            # evalueate order
            if reply == 2:
                oxygen = deepcopy(self.pos)
            # prepare new order
            if reply == 0:
                # hit wall => "turn" right
                order = d_order2turn[order]
            else:
                # turn left if possible
                order = d_order2turn_c[order]
        return oxygen

    def count_steps(self, start, end):
        """
        Count steps of mimimal path from start point to end point
        """
        # initialize
        process = []
        for item, value in self.floor.items():
            if value != "#":
                process.append(item)
        known = {start: 0}
        process.remove(start)
        # start counting
        while process:
            for item in process:
                minvals = []
                if (item[0], item[1] + 1) in known:
                    minvals.append(known[(item[0], item[1] + 1)])
                if (item[0], item[1] - 1) in known:
                    minvals.append(known[(item[0], item[1] - 1)])
                if (item[0] + 1, item[1]) in known:
                    minvals.append(known[(item[0] + 1, item[1])])
                if (item[0] - 1, item[1]) in known:
                    minvals.append(known[(item[0] - 1, item[1])])
                if minvals:
                    known[item] = min(minvals) + 1
                    process.remove(item)
                    break
        return known[end]

    def spread_oxygen(self, start):
        """
        Spread oxygen from start point
        """
        # initialize
        process = []
        for item, value in self.floor.items():
            if value != "#":
                process.append(item)
        known = {start: 0}
        process.remove(start)
        # start counting
        while process:
            for item in process:
                minvals = []
                if (item[0], item[1] + 1) in known:
                    minvals.append(known[(item[0], item[1] + 1)])
                if (item[0], item[1] - 1) in known:
                    minvals.append(known[(item[0], item[1] - 1)])
                if (item[0] + 1, item[1]) in known:
                    minvals.append(known[(item[0] + 1, item[1])])
                if (item[0] - 1, item[1]) in known:
                    minvals.append(known[(item[0] - 1, item[1])])
                if minvals:
                    known[item] = min(minvals) + 1
                    process.remove(item)
                    break
        return max(known.values())


def main():
    """
    Main function
    """

    # process args
    infile = get_args()

    # create droid
    droid = ElfDroid()
    droid.init_cpu(infile)
#    droid.manual_explore('NENENNWNENENESEWSEWSWESWEENENEN')
    oxygen = droid.auto_explore()
    droid.print_floor()
    print("oxygen pos = {}".format(oxygen))
    steps = droid.count_steps((0, 0), tuple(oxygen))
    print("Solution of part 1:", steps)
    oxysteps = droid.spread_oxygen(tuple(oxygen))
    print("Solution of part 2:", oxysteps)


if __name__ == '__main__':
    main()

# EOF
