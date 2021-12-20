#!/usr/bin/env python
# -*- coding:utf-8 -*-
"""
Advent of code 2021 - Day 19
"""

import argparse
from math import floor, ceil
from time import time


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


def split_string(string):
    """
    split string to left and right parts
    """
    depth = 0
    commad = 99
    commapos = 0
    for index, char in enumerate(string):
        if char == '[':
            depth += 1
        elif char == ']':
            depth -= 1
        elif char == ',':
            if depth < commad:
                commad = depth
                commapos = index
    return string[1:commapos], string[commapos+1:-1]


def string2tree(string, nodeindex):
    """
    Convert string to tree representation
    """
    nodes = {}
    data = [[string, nodeindex, 'root']]  # [string to parse, root node, part]
    lastid = nodeindex - 1
    while data:
        work = data.pop()
        lastid += 1
        if work[0][0] == '[':
            # create new node
            nodes[lastid] = {'root': work[1], 'left': -1, 'right': -1, 'value': -1}
            if lastid > 0:
                nodes[work[1]][work[2]] = lastid
            left, right = split_string(work[0])
            # add node string for further processing
            data.append([left, lastid, 'left'])
            data.append([right, lastid, 'right'])
        else:
            # create leaf node
            nodes[lastid] = {'root': work[1], 'left': -1, 'right': -1, 'value': int(work[0])}
            nodes[work[1]][work[2]] = lastid
    return nodes


def tree2string(tree, root):
    """
    Convert tree to string representation
    """
    string = ''
    path = [[-1, 'none'], [root, 'left']]
    while True:
        nodeid = path[-1][0]
        if nodeid == -1:
            break
        if tree[nodeid]['value'] != -1:
            # process leaf
            string += str(tree[nodeid]['value'])
            path = path[:-1]
        elif path[-1][1] == 'left' and tree[path[-1][0]]['left'] != -1:
            # go left
            path[-1][1] = 'right'
            path.append([tree[path[-1][0]]['left'], 'left'])
            string += '['
        elif path[-1][1] == 'right' and tree[path[-1][0]]['right'] != -1:
            # go right
            path[-1][1] = 'back'
            path.append([tree[path[-1][0]]['right'], 'left'])
            string += ','
        elif path[-1][1] == 'back':
            path = path[:-1]
            string += ']'
    return string


class SnailfishEquation():
    """
    Class for cave path navigation
    """

    def __init__(self):
        """
        Cosntructor
        """
        self.tree = None
        self.lastid = 0
        self.root = -1

    def first_down_right(self, start):
        """
        Find most right leaf in subtree
        """
        while self.tree[start]['right'] != -1:
            start = self.tree[start]['right']
        return start

    def first_down_left(self, start):
        """
        Find most left leaf in subtree
        """
        while self.tree[start]['left'] != -1:
            start = self.tree[start]['left']
        return start

    def first_up_left(self, start, ignore):
        """
        Find most left leaf in tree up from start (and do go back to ignore)
        """
        while start != -1:
            if self.tree[start]['left'] != ignore:
                return self.first_down_right(self.tree[start]['left'])
            ignore = start
            start = self.tree[start]['root']
        return -1

    def first_up_right(self, start, ignore):
        """
        Find most right leaf in tree up from start (and do go back to ignore)
        """
        while start != -1:
            if self.tree[start]['right'] != ignore:
                return self.first_down_left(self.tree[start]['right'])
            ignore = start
            start = self.tree[start]['root']
        return -1

    def add(self, newpart):
        """
        Add new snailfish number and reduce it if necessary
        """
        # add new snailfish number
        if not self.tree:
            self.lastid = 0
            self.root = 0
            self.tree = string2tree(newpart, self.lastid)
            self.lastid = len(self.tree) - 1
            self.tree[self.root]['root'] = -1
        else:
            newtree = string2tree(newpart, self.lastid + 1)
            self.lastid = self.lastid + len(newtree) + 1
            newitem = {'root': -1, 'left': self.root, 'right': min(newtree.keys()), 'value': -1}
            self.tree[self.root]['root'] = self.lastid
            newtree[min(newtree.keys())]['root'] = self.lastid
            self.root = self.lastid
            self.tree = self.tree | newtree
            self.tree[self.lastid] = newitem

        # repeat reduction while possible
        change = True
        while change:
            change = False
            check = True
            while check:
                check = self.explode()
                if check:
                    change = True
            # make one split if possible
            check = self.split()
            if check:
                change = True

    def explode(self):
        """
        Make one leftmost explode
        """
        # find leftmost leave for exploding
        path = [[-1, 'none'], [self.root, 'left']]
        depth = 0
        while True:
            if path[-1][0] == -1:
                break
            if self.tree[path[-1][0]]['value'] != -1:
                # process leaf
                if depth == 5:
                    break
                path = path[:-1]
                depth -= 1
            if path[-1][1] == 'left' and self.tree[path[-1][0]]['left'] != -1:
                # go left
                path[-1][1] = 'right'
                path.append([self.tree[path[-1][0]]['left'], 'left'])
                depth += 1
            elif path[-1][1] == 'right' and self.tree[path[-1][0]]['right'] != -1:
                # go right
                path[-1][1] = 'back'
                path.append([self.tree[path[-1][0]]['right'], 'left'])
                depth += 1
            elif path[-1][1] == 'back':
                path = path[:-1]
                depth -= 1
        explode_left = path[-1][0]
        if explode_left == -1:
            # no candidate for explode found
            return False

        # perfform exploding
        explode_root = self.tree[explode_left]['root']
        explode_right = self.tree[explode_root]['right']
        explode_root_root = self.tree[explode_root]['root']
        if explode_root == self.tree[explode_root_root]['left']:
            # find nodes for arithmetic operations
            sum_right = self.first_down_left(self.tree[explode_root_root]['right'])
            sum_left = self.first_up_left(explode_root_root, explode_root)
            # make erithmetic operations
            self.tree[sum_right]['value'] += self.tree[explode_right]['value']
            if sum_left != -1:
                self.tree[sum_left]['value'] += self.tree[explode_left]['value']
            self.tree[explode_right]['value'] = 0
            # make changes in tree (delete root and left)
            self.tree[explode_root_root]['left'] = explode_right
            self.tree[explode_right]['root'] = explode_root_root
            del self.tree[explode_left]
            del self.tree[explode_root]
        else:
            # find nodes for arithmetic operations
            sum_right = self.first_up_right(explode_root_root, explode_root)
            sum_left = self.first_down_right(self.tree[explode_root_root]['left'])
            # make erithmetic operations
            if sum_right != -1:
                self.tree[sum_right]['value'] += self.tree[explode_right]['value']
            self.tree[sum_left]['value'] += self.tree[explode_left]['value']
            self.tree[explode_left]['value'] = 0
            # make changes in tree (delete root and left)
            self.tree[explode_root_root]['right'] = explode_left
            self.tree[explode_left]['root'] = explode_root_root
            del self.tree[explode_right]
            del self.tree[explode_root]
        return True

    def split(self):
        """
        make leftmost split
        """
        path = [[-1, 'none'], [self.root, 'left']]
        while True:
            if path[-1][0] == -1:
                break
            if self.tree[path[-1][0]]['value'] != -1:
                # process leaf
                if self.tree[path[-1][0]]['value'] > 9:
                    newleftval = floor(self.tree[path[-1][0]]['value'] / 2)
                    newrightval = ceil(self.tree[path[-1][0]]['value'] / 2)
                    self.tree[self.lastid+1] = {
                       'root': path[-1][0],
                       'left': -1,
                       'right': -1,
                       'value': newleftval}
                    self.tree[self.lastid+2] = {
                        'root': path[-1][0],
                        'left': -1,
                        'right': -1,
                        'value': newrightval}
                    self.tree[path[-1][0]]['value'] = -1
                    self.tree[path[-1][0]]['left'] = self.lastid + 1
                    self.tree[path[-1][0]]['right'] = self.lastid + 2
                    self.lastid += 2
                    return True
                path = path[:-1]
            if path[-1][1] == 'left' and self.tree[path[-1][0]]['left'] != -1:
                # go left
                path[-1][1] = 'right'
                path.append([self.tree[path[-1][0]]['left'], 'left'])
            elif path[-1][1] == 'right' and self.tree[path[-1][0]]['right'] != -1:
                # go right
                path[-1][1] = 'back'
                path.append([self.tree[path[-1][0]]['right'], 'left'])
            elif path[-1][1] == 'back':
                # go back/up
                path = path[:-1]
        return False

    def get_magnitude(self):
        """
        compute magnitude
        """
        path = [[-1, 'none'], [self.root, 'left']]
        values = {}
        while True:
            nodeid = path[-1][0]
            if self.tree[nodeid]['value'] != -1:
                # process leaf
                values[nodeid] = self.tree[nodeid]['value']
                path = path[:-1]
            elif self.tree[nodeid]['left'] in values and self.tree[nodeid]['right'] in values:
                # process complete node
                left_node_id = self.tree[nodeid]['left']
                right_node_id = self.tree[nodeid]['right']
                values[nodeid] = 3 * values[left_node_id] + 2 * values[right_node_id]
                path = path[:-1]
                if nodeid == self.root:
                    break
            elif path[-1][1] == 'left' and self.tree[path[-1][0]]['left'] not in values:
                # go left
                path[-1][1] = 'right'
                path.append([self.tree[path[-1][0]]['left'], 'left'])
            elif path[-1][1] == 'right' and self.tree[path[-1][0]]['right'] not in values:
                # go right
                path[-1][1] = 'back'
                path.append([self.tree[path[-1][0]]['right'], 'left'])
            elif path[-1][1] == 'back':
                path = path[:-1]
        return values[self.root]


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
    starttime = time()
    obj = SnailfishEquation()
    for line in lines:
        obj.add(line)
    mag = obj.get_magnitude()
    endtime = time()
    print(f"Part 1 solution: {mag}")
    print(f" -> {tree2string(obj.tree, obj.root)}")
    print(f" -> time elapsed {endtime-starttime:6.2f} s")

    # part 2
    maxmag = 0
    maxstr = ''
    starttime = time()
    for i, valuei in enumerate(lines):
        for j, valuej in enumerate(lines):
            if i == j:
                continue
            obj = SnailfishEquation()
            obj.add(valuei)
            obj.add(valuej)
            mag = obj.get_magnitude()
            if mag > maxmag:
                maxmag = mag
                maxstr = tree2string(obj.tree, obj.root)
            obj = SnailfishEquation()
            obj.add(valuej)
            obj.add(valuei)
            mag = obj.get_magnitude()
            if mag > maxmag:
                maxmag = mag
                maxstr = tree2string(obj.tree, obj.root)
        print(".", end="",  flush=True)
    endtime = time()
    print(f"\nPart 2 solution: {maxmag}")
    print(f" -> {maxstr}")
    print(f" -> time elapsed {endtime-starttime:6.2f} s")


if __name__ == '__main__':
    main()

# EOF
