#!/usr/bin/env python
# -*- coding:utf-8 -*-
"""
Advent of code 2021 - Day 20
"""

import argparse
from PIL import Image
import numpy as np


def get_args():
    """
    Cmd line argument parsing (preprocessing)
    """
    # Assign description to the help doc
    parser = argparse.ArgumentParser(
        description='Advent of code 2021: Day 20')

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


def get_index(myimage, point):
    """
    Main function
    """
    num = ''
    for i in range(point[0]-1, point[0]+2):
        for j in range(point[1]-1, point[1]+2):
            num += str(myimage[(i, j)])
    return int(num, 2)


def enhance(myimage, size, myfilter):
    """
    Main function
    """
    base = myfilter[myimage[(0, 0)]*511]
    newimage = np.zeros((size[0], size[1]), dtype=int)
    if base:
        newimage = np.ones((size[0], size[1]), dtype=int)
    for i in range(1, size[0]-1):
        for j in range(1, size[1]-1):
            index = get_index(myimage, (i, j))
            newimage[(i, j)] = myfilter[index]
    return newimage


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

    # determine algorithm
    myfilter = np.zeros(len(lines[0]), dtype=int)
    for index, char in enumerate(lines[0]):
        if char == '#':
            myfilter[index] = 1

    # determine image
    width = len(lines[2]) + 4
    height = len(lines[2:]) + 4
    myimage = np.zeros((width, height), dtype=int)
    i = 1
    for line in lines[2:]:
        i += 1
        j = 1
        for char in line:
            j += 1
            if char == '#':
                myimage[(i, j)] = 1

    # part 1 + part 2
    for i in range(50):
        # enhance
        newimage = enhance(myimage, (width, height), myfilter)
        # add surrounding border
        image2 = np.zeros((width+(i+1)*4, height+(i+1)*4), dtype=int)
        if newimage[(0, 0)]:
            image2 = np.ones((width+(i+1)*4, height+(i+1)*4), dtype=int)
        image2[2:width+2, 2:height+2] = newimage
        width += 4
        height += 4
        myimage = image2
        print(".", end="",  flush=True)
        if i == 1:
            print(f"\nPart 1 solution: {np.sum(newimage)}")
            Image.fromarray(newimage.astype('uint8')*255).save('sol1.png')

    print(f"\nPart 2 solution: {np.sum(myimage)}")
    Image.fromarray(myimage.astype('uint8')*255).save('sol2.png')


if __name__ == '__main__':
    main()

# EOF
