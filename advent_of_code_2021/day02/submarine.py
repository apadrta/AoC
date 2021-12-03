#!/usr/bin/env python
# -*- coding:utf-8 -*-

"""
Advent of code 2021 - Submarine for Day 2
"""


class ElfSubmarine():
    """
    Submarine object Mk-D02B
    """

    def __init__(self):
        """
        Constructor
        """
        self.horizontal = 0
        self.depth = 0
        self.aim = 0
        self.instructions = []

    def set_instructions(self, new_instructions):
        """
        Set the navigation instructions
        """
        self.instructions = new_instructions

    def read_instructions(self, filename):
        """
        Reads the navigation instructions from file
        """
        with open(filename, "r") as fileh:
            data = fileh.readlines()
        self.instructions = []
        for item in data:
            [order, value] = item.split(" ", 1)
            self.instructions.append([order, int(value.replace('\n', '').replace('\r', ''))])

    def __change_aim(self, val):
        """
        Change aim of the submarine
        """
        self.aim += val

    def __move(self, distance):
        """
        Move the submarine
        """
        self.horizontal += distance
        self.depth += self.aim * distance

    def navigate(self):
        """
        Process navigation instruction
        """
        for order in self.instructions:
            if order[0] == 'forward':
                self.__move(order[1])
            elif order[0] == 'up':
                self.__change_aim(-order[1])
            elif order[0] == 'down':
                self.__change_aim(order[1])
            else:
                print("Unknown order '{}' ignored.".format(order[0]))

    def get_state_hash(self):
        """
        Return hash of submarine state
        """
        return self.horizontal * self.depth

# EOF
