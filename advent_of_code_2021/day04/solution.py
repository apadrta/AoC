#!/usr/bin/env python
# -*- coding:utf-8 -*-
"""
Advent of code 2021 - Day 4
"""

import argparse


def get_args():
    """
    Cmd line argument parsing (preprocessing)
    """
    # Assign description to the help doc
    parser = argparse.ArgumentParser(
        description='Advent of code 2021: Day 4')

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


class ElfBingoBoard():
    """
    Bingo board for elf submarine
    """

    def __init__(self, data):
        """
        Constructor (from N lines)
        """
        self.winners = []
        # add rows to winners
        for item in data:
            self.winners.append(item)
        # add columns to winners
        for pos in range(0, len(data[0])):
            newcol = []
            for item in data:
                newcol.append(item[pos])
            self.winners.append(newcol)

    def check_number(self, number):
        """
        Check if number is in board and remove it from winners (rows and columns)
        """
        for pos in range(0, len(self.winners)):
            if number in self.winners[pos]:
                self.winners[pos].remove(number)

    def check_bingo(self):
        """
        Check if bingo is reached
        """
        for winner in self.winners:
            if len(winner) == 0:
                return True
        return False

    def get_final_score(self, number):
        """
        Get final score
        """
        # multiply winner
        value = 0
        for winner in self.winners:
            for num in winner:
                value += num
        # remove duplicities row/column
        value = value // 2 * number
        return value


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

    # process data
    drawn = [int(x) for x in data[0].replace('\n', '').replace('\r', '').split(",")]
    boards = []
    temp = []
    for line in data[2:]:
        line = line.replace('\n', '').replace('\r', '').replace('  ', ' ')
        if line:
            if line[0] == ' ':
                line = line[1:]
            temp.append([int(x) for x in line.split(" ")])
        else:
            board = ElfBingoBoard(temp)
            boards.append(board)
            temp = []
    if temp:
        board = ElfBingoBoard(temp)
        boards.append(board)

    # play bingo
    winner_order = []
    part1 = False
    for number in drawn:
        pos = 0
        for board in boards:
            board.check_number(number)
            if board.check_bingo():
                if not part1:
                    print("Part 1 solution: {}".format(board.get_final_score(number)))
                    part1 = True
                if pos not in winner_order:
                    winner_order.append(pos)
            pos += 1
        if len(winner_order) == len(boards):
            print("Part 2 solution: {}".format(boards[winner_order[-1]].get_final_score(number)))
            break


if __name__ == '__main__':
    main()

# EOF
