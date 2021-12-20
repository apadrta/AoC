#!/usr/bin/env python
# -*- coding:utf-8 -*-
"""
Advent of code 2021 - Day 19
"""

import argparse
from copy import deepcopy


def get_args():
    """
    Cmd line argument parsing (preprocessing)
    """
    # Assign description to the help doc
    parser = argparse.ArgumentParser(
        description='Advent of code 2021: Day 19')

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


def scanner2matrix(data):
    """
    Create vector matrix
    """
    size = len(data)
    matrix = {}
    for i in range(size):
        for j in range(size):
            matrix[(i, j)] = [
                data[j][0] - data[i][0],
                data[j][1] - data[i][1],
                data[j][2] - data[i][2]]
    return matrix


class ElfBeaconScanner():
    """
    Class for evaluating beacon scanner
    """

    def __init__(self, defoverlap):
        """
        Constructor
        """
        self.scanners = {}         # primary scanner data
        self.matrixes = {}         # vector-distance transformed data
        self.overlap = defoverlap  # number of minimal overlap
        self.normalize = {}        # normalization shift [(from, to), vector]
        self.scanner_pos = [[0, 0, 0]]      # scanner position for part 2

    def read_data(self, filename):
        """
        Read data from file
        """
        # read data from file
        data = []
        with open(filename, "r") as fileh:
            data = fileh.readlines()
        lines = [x.strip() for x in data]
        # parse data for each scanner
        self.scanners = {}
        self.matrixes = {}
        index = -1
        for line in lines:
            if not line:
                continue
            if line[0:3] == '---':
                index += 1
                self.scanners[index] = [[]]
            else:
                self.scanners[index][0].append([int(x) for x in line.split(",")])
                self.matrixes[index] = [scanner2matrix(self.scanners[index][0])]
        # convert
        for scanner, data in self.scanners.items():
            for i in range(0, 3):
                self.scanners[scanner].append(deepcopy(self.scanners[scanner][-1]))
                self.rotate_y(scanner, len(self.scanners[scanner])-1)
                self.matrixes[scanner].append(scanner2matrix(self.scanners[scanner][-1]))
            self.scanners[scanner].append(deepcopy(self.scanners[scanner][-1]))
            self.rotate_x(scanner, len(self.scanners[scanner]) - 1)
            self.rotate_x(scanner, len(self.scanners[scanner]) - 1)
            self.matrixes[scanner].append(scanner2matrix(self.scanners[scanner][-1]))
            for i in range(0, 3):
                self.scanners[scanner].append(deepcopy(self.scanners[scanner][-1]))
                self.rotate_y(scanner, len(self.scanners[scanner]) - 1)
                self.matrixes[scanner].append(scanner2matrix(self.scanners[scanner][-1]))
            self.scanners[scanner].append(deepcopy(self.scanners[scanner][-1]))
            self.rotate_x(scanner, len(self.scanners[scanner]) - 1)
            self.matrixes[scanner].append(scanner2matrix(self.scanners[scanner][-1]))
            for i in range(3):
                self.scanners[scanner].append(deepcopy(self.scanners[scanner][-1]))
                self.rotate_z(scanner, len(self.scanners[scanner]) - 1)
                self.matrixes[scanner].append(scanner2matrix(self.scanners[scanner][-1]))
            self.scanners[scanner].append(deepcopy(self.scanners[scanner][-1]))
            self.rotate_x(scanner, len(self.scanners[scanner]) - 1)
            self.rotate_x(scanner, len(self.scanners[scanner]) - 1)
            self.matrixes[scanner].append(scanner2matrix(self.scanners[scanner][-1]))
            for i in range(3):
                self.scanners[scanner].append(deepcopy(self.scanners[scanner][-1]))
                self.rotate_z(scanner, len(self.scanners[scanner]) - 1)
                self.matrixes[scanner].append(scanner2matrix(self.scanners[scanner][-1]))
            self.scanners[scanner].append(deepcopy(self.scanners[scanner][-1]))
            self.rotate_y(scanner, len(self.scanners[scanner]) - 1)
            self.matrixes[scanner].append(scanner2matrix(self.scanners[scanner][-1]))
            for i in range(3):
                self.scanners[scanner].append(deepcopy(self.scanners[scanner][-1]))
                self.rotate_x(scanner, len(self.scanners[scanner]) - 1)
                self.matrixes[scanner].append(scanner2matrix(self.scanners[scanner][-1]))
            self.scanners[scanner].append(deepcopy(self.scanners[scanner][-1]))
            self.rotate_y(scanner, len(self.scanners[scanner]) - 1)
            self.rotate_y(scanner, len(self.scanners[scanner]) - 1)
            self.matrixes[scanner].append(scanner2matrix(self.scanners[scanner][-1]))
            for i in range(3):
                self.scanners[scanner].append(deepcopy(self.scanners[scanner][-1]))
                self.rotate_x(scanner, len(self.scanners[scanner]) - 1)
                self.matrixes[scanner].append(scanner2matrix(self.scanners[scanner][-1]))
            print(".", end="",  flush=True)

    def rotate_z(self, sindex, rot):
        """
        Rotate aroud z axis by 90
        """
        for index, value in enumerate(self.scanners[sindex][rot]):
            self.scanners[sindex][rot][index] = [-value[1], value[0], value[2]]

    def rotate_x(self, sindex, rot):
        """
        Rotate aroud x axis by 90
        """
        for index, value in enumerate(self.scanners[sindex][rot]):
            self.scanners[sindex][rot][index] = [value[0], -value[2], value[1]]

    def rotate_y(self, sindex, rot):
        """
        Rotate aroud y axis by 90
        """
        for index, value in enumerate(self.scanners[sindex][rot]):
            self.scanners[sindex][rot][index] = [-value[2], value[1], value[0]]

    def find_overlap(self, aindex, arot, bindex, brot):
        """
        Find overlap (assume correct rotation)
        """
        # initialize mapping of single vectors
        lines = []    # [[a, b], [a, b]], where a = line in A matrix, b - line in B matrix
        for apoints, avector in self.matrixes[aindex][arot].items():
            for bpoints, bvector in self.matrixes[bindex][brot].items():
                if avector == bvector and avector != [0, 0, 0]:
                    lines.append([apoints, bpoints])
        # try to make continuos line of length self.overlap
        stop = False
        path = []
        for line in lines:
            paths = [[list(line[0]), list(line[1])]]
            while paths:
                path = paths.pop()
                if len(path[0]) == self.overlap:
                    stop = True
                    break
                for segment in lines:
                    if segment[0][0] != path[0][-1] or segment[1][0] != path[1][-1]:
                        continue
                    if segment[0][1] not in path[0] and segment[1][1] not in path[1]:
                        paths.append([path[0] + [segment[0][1]], path[1] + [segment[1][1]]])
            if stop:
                break
        if path and len(path[0]) == self.overlap:
            return path
        return []

    def merge_two_scanners(self, base_scanner, base_rot, new_scanner):
        """
        Merge beacons from scanners together
        """
        # test all rotations of new_scanner with basic position of base_scanner
        path = []
        for i in range(24):
            path = self.find_overlap(base_scanner, base_rot, new_scanner, i)
            if path:
                break
        return path, i

    def normalize_coordinates(self, base_scanner, base_rot, new_scanner, new_rot, calib_base, calib_new):
        """
        Merge beacons from scanners together
        """
        calib_b = self.scanners[base_scanner][base_rot][calib_base]
        calib_n = self.scanners[new_scanner][new_rot][calib_new]
        shift = [calib_b[0] - calib_n[0], calib_b[1] - calib_n[1], calib_b[2] - calib_n[2]]
        self.scanner_pos.append(shift)
        new_calibrated = []
        for value in self.scanners[new_scanner][new_rot]:
            new_value = [value[0] + shift[0], value[1] + shift[1], value[2] + shift[2]]
            new_calibrated.append(new_value)
        for index, value in enumerate(self.scanners[new_scanner][new_rot]):
            self.scanners[new_scanner][new_rot][index] = [
                value[0] + shift[0],
                value[1] + shift[1],
                value[2] + shift[2]]
        return new_calibrated

    def merge_scanners(self):
        """
        Merge beacons from scanners together
        """
        beacons = deepcopy(self.scanners[0][0])
        known = []
        known.append([0, 0])  # [scanner id, scanner rotation]
        remain = list(range(1, len(self.scanners)))
        remain.reverse()
        repeat = []
        base_scanner = 0
        new_scanner = 1
        path = []
        new_rot = 0
        while True:
            # test all scanners ...
            new_scanner = remain.pop()
            path = []
            # with all bases (stop after first)
            for base_known in known:
                base_scanner = base_known[0]
                base_rot = base_known[1]
                path, new_rot = self.merge_two_scanners(base_scanner, base_rot, new_scanner)
                if path:
                    break
            if path:
                # existing overlap -> add new points
                new_beacons = self.normalize_coordinates(
                    base_scanner,
                    base_rot,
                    new_scanner,
                    new_rot,
                    path[0][0],
                    path[1][0])
                for beacon in new_beacons:
                    if beacon not in beacons:
                        beacons.append(beacon)
                known.append([new_scanner, new_rot])
            else:
                repeat.append(new_scanner)
            if not remain and repeat:
                remain = repeat
                repeat = []
            if not remain and not repeat:
                break
            print(".", end="",  flush=True)
        return len(beacons)

    def manhatan_scanners(self):
        """
        Get biggest Manhatan distance
        """
        maxlen = 0
        for scan_a in self.scanner_pos:
            for scan_b in self.scanner_pos:
                newlen = abs(scan_a[0]-scan_b[0]) + \
                    abs(scan_a[1]-scan_b[1]) + \
                    abs(scan_a[2]-scan_b[2])
                if newlen > maxlen:
                    maxlen = newlen
        return maxlen


def main():
    """
    Main function
    """

    # process args
    infile = get_args()

    # part 1
    obj = ElfBeaconScanner(12)
    print("Reading data and preparing")
    obj.read_data(infile)
    print("\nProcessing data")
    print(f"\nPart 1 solution: {obj.merge_scanners()}")
    # part 2
    print(f"Part 2 solution: {obj.manhatan_scanners()}")


if __name__ == '__main__':
    main()

# EOF
