#!/usr/bin/env python
# -*- coding:utf-8 -*-
"""
Advent of code 2021 - Day 16
"""

import argparse
from math import prod


def get_args():
    """
    Cmd line argument parsing (preprocessing)
    """
    # Assign description to the help doc
    parser = argparse.ArgumentParser(
        description='Advent of code 2021: Day 16')

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


def evaluate(operator, data):
    """
    evaluate formula
    """
    ret = 0
    if operator == 0:
        ret = sum(data)
    elif operator == 1:
        ret = prod(data)
    elif operator == 2:
        ret = min(data)
    elif operator == 3:
        ret = max(data)
    elif operator == 5:
        ret = 1 if data[0] > data[1] else 0
    elif operator == 6:
        ret = 1 if data[0] < data[1] else 0
    elif operator == 7:
        ret = 1 if data[0] == data[1] else 0
    return ret


class ElfPacketParser():
    """
    Parser for elf BITS
    """

    def __init__(self):
        """
        constructor
        """
        self.data = ''
        self.ptr = 0
        self.maxlvl = 0

    def set_packet(self, binpacket):
        """
        add data for parsing
        """
        self.data = ''.join([format(int(x, 16), "04b").replace("0b", "") for x in binpacket])

    def parse(self):
        """
        parse packets
        """
        # self init
        ptr = 0
        buff = [["init", 0, "init", []]]
        versum = 0
        result = 0

        while buff:
            # process header
            version = int(self.data[ptr:ptr+3], 2)
            ptr += 3
            ptype = int(self.data[ptr:ptr+3], 2)
            ptr += 3
            packetsize = 6
            versum += version
            to_process = False

            # process data
            if ptype == 4:
                # number -> update last item operands
                num = ''
                while self.data[ptr] == "1":
                    num += self.data[ptr+1:ptr+5]
                    ptr += 5
                    packetsize += 5
                num += self.data[ptr+1:ptr+5]
                num = int(num, 2)
                buff[-1][3].append(num)
                ptr += 5
                packetsize += 5
            else:
                # operator -> new item will be created
                mode = self.data[ptr]
                ptr += 1
                packetsize += 1
                if mode == "0":
                    subpacketsize = int(self.data[ptr:ptr+15], 2)
                    ptr += 15
                    packetsize += 15
                    to_process = ["bits", subpacketsize, ptype, []]
                else:
                    subpackets = int(self.data[ptr:ptr+11], 2)
                    ptr += 11
                    packetsize += 11
                    to_process = ["packets", subpackets, ptype, []]

            # udpdate counters in open items
            for i in range(len(buff)):
                if buff[i][0] == "bits":
                    buff[i][1] -= packetsize
            if buff[-1][0] == "packets":
                buff[-1][1] -= 1

            # add new open items
            if to_process:
                buff.append(to_process)

            # evaluate last item when single operation available and put the result to previous item
            while buff and buff[-1][1] == 0:
                if buff[-1][2] in [0, 1, 2, 3, 5, 6, 7]:
                    buff[-2][3].append(evaluate(buff[-1][2], buff[-1][3]))

                # check if finished
                if buff[-1][0] == "init":
                    result = buff[-1][3]
                # remove processed item
                buff.pop()
        return versum, result[0]


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

    # part 1 + part 2
    obj = ElfPacketParser()
    obj.set_packet(lines[0])
    versum, result = obj.parse()

    print(f"Part 1 solution: {versum}")

    # part 2
    print(f"Part 2 solution: {result}")


if __name__ == '__main__':
    main()

# EOF
