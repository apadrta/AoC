#!/usr/bin/env python
# -*- coding:utf-8 -*-
"""
Advent of code 2019 - Day 16
"""

import argparse


def get_args():
    """
    Cmd line argument parsing (preprocessing)
    """
    # Assign description to the help doc
    parser = argparse.ArgumentParser(
        description='Advent of code 2019: Day 16')

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


class ElfFFT():
    """
    Class for signal filtering using FFT
    """

    def __init__(self):
        """
        Constructor
        """
        self.base = [0, 1, 0, -1]
        self.patterns = []
        self.signal = []

    def __init_patterns(self, number):
        """
        Initializa patterns field
        """
        num = 0

        while num < number:
            pat = []
            for item in self.base:
                pat += [item] * (num + 1)
            self.patterns.append(pat)
            num += 1

    def set_signal(self, initsignal):
        """
        Set signal
        """
        self.signal = initsignal
        self.__init_patterns(len(self.signal))

    def __process_digit(self, digit, pos):
        """
        Process one digit form signal
        """
        rep = len(digit) // len(self.patterns[pos])
        fft = (self.patterns[pos] * (rep + 2))[1:len(digit)+1]
        sums = 0
        index = 0
        while index < len(digit):
            sums += digit[index] * fft[index]
            index += 1
        return int(str(sums)[-1])

    def __filter_signal(self):
        """
        Filter whole signal
        """
        out = []
        index = 0
        while index < len(self.signal):
            out.append(self.__process_digit(self.signal, index))
            index += 1
        self.signal = out

    def fft(self, phases):
        """
        Perform multiple filtering
        """
        index = 0
        while index < phases:
            self.__filter_signal()
            index += 1


def main():
    """
    Main function
    """

    # process args
    infile = get_args()

    # read data
    data = []
    with open(infile, "r") as fileh:
        data = fileh.readline().replace('\n', '').replace('\r', '')
    nums = [int(x) for x in data]

    # nums =[1, 2, 3, 4, 5, 6, 7, 8]
    signal_filter = ElfFFT()
    signal_filter.set_signal(nums)
    signal_filter.fft(100)
    print(''.join(str(x) for x in signal_filter.signal[:8]))

# print("Part 1 solution: {}".format(board.get_final_score(number)))
# print("Part 2 solution: {}".format(boards[winner_order[-1]].get_final_score(number)))


if __name__ == '__main__':
    main()

# EOF
