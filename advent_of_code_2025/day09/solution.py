#!/usr/bin/env python
# -*- coding:utf-8 -*-
"""
Advent of Code solution
"""

import argparse
from PIL import Image, ImageDraw


def get_args():
    """
    Cmd line argument parsing (preprocessing)
    """
    # Assign description to the help doc
    parser = argparse.ArgumentParser(
        description='Advent of code 2025 day 9')

    # Add arguments
    parser.add_argument(
        '-i',
        '--infile',
        type=str,
        help='Input filename',
        required=True)

    # Array for all arguments passed to script
    args = parser.parse_args()

    # Return arg variables
    return args.infile


def read_data(filename):
    """
    read input data
    """
    data = []
    with open(filename, "r", encoding="utf8") as fhnd:
        data = fhnd.readlines()
    data = [x.strip() for x in data]

    rectangles = []
    for item in data:
        rectangles.append([int(x) for x in item.split(',')])
    return rectangles


def get_biggest(data):
    """
    find biggest rectangle
    """
    maxarea = 0
    for idx, itemi in enumerate(data):
        for itemj in data[(idx+1):]:
            area = (abs(itemi[0] - itemj[0]) + 1) * (abs(itemi[1] - itemj[1]) + 1)
            maxarea = max(maxarea, area)
    return maxarea


def get_edges(nodes):
    """
    get vertical and horizontal edges
    """
    horizontal = []
    vertical = []

    for idx, value in enumerate(nodes[:-1]):
        if value[0] == nodes[idx + 1][0]:
            # vertical
            miny = min(value[1], nodes[idx + 1][1])
            maxy = max(value[1], nodes[idx + 1][1])
            vertical.append([value[0], miny, maxy])
        else:
            minx = min(value[0], nodes[idx + 1][0])
            maxx = max(value[0], nodes[idx + 1][0])
            horizontal.append([value[1], minx, maxx])
    return horizontal, vertical


def get_biggest_inside_bf(nodes):
    """
    get biggest inside rectangle (nothing clever)
    """
    # preprocess data
    nodes.append(nodes[0])
    horizontals, verticals = get_edges(nodes)
    maxarea = 0
    coords = []
    # bruteforce all possible combination of nodes
    for idx, node_i in enumerate(nodes):
        for node_j in nodes[idx+1:-1]:
            # check validity (no intersection of other edge with the border of rectangle
            min_x = min(node_i[0], node_j[0])+0.5
            min_y = min(node_i[1], node_j[1])+0.5
            max_x = max(node_i[0], node_j[0])-0.5
            max_y = max(node_i[1], node_j[1])-0.5
            isok = True
            for vert in verticals:
                if min_x <= vert[0] <= max_x and (vert[1] <= min_y <= vert[2] or vert[1] <= max_y <= vert[2]):
                    isok = False
                    break
            if not isok:
                continue
            for hori in horizontals:
                if min_y <= hori[0] <= max_y and (hori[1] <= min_x <= hori[2] or hori[1] <= max_x <= hori[2]):
                    isok = False
                    break
            if not isok:
                continue
            # check area of valid rectangle
            area = (abs(node_i[0]-node_j[0])+1)*(abs(node_i[1]-node_j[1])+1)
            if area > maxarea:
                maxarea = area
                coords = [node_i, node_j]
    return maxarea, coords


def draw_data(nodes, filename):
    """
    visualize data and the rectangle
    """
    ratio = 50
    boundary = 50

    min_x = min(node[0] for node in nodes) // ratio
    max_x = max(node[0] for node in nodes) // ratio
    min_y = min(node[1] for node in nodes) // ratio
    max_y = max(node[1] for node in nodes) // ratio

    size_x = max_x - min_x + 2 * boundary
    size_y = max_y - min_y + 2 * boundary

    img = Image.new("RGB", (size_x, size_y), (0, 0, 0))
    draw = ImageDraw.Draw(img)

    for idx, node in enumerate(nodes[:-1]):
        draw.line(((node[0] - min_x) // ratio + boundary, (node[1] - min_y) // ratio + boundary, (nodes[idx+1][0] - min_x) // ratio + boundary, (nodes[idx + 1][1] - min_y) // ratio + boundary), fill=(0, 255, 0), width=5)

    img.save(filename)


def main():
    """
    main
    """

    filename = get_args()
    data = read_data(filename)

    # part 1
    sums = get_biggest(data)
    print(f"Solution part 1: {sums}")

    # part 2
    sums, _ = get_biggest_inside_bf(data)
    print(f"Solution part 2: {sums}")

    # vizualization
    draw_data(data, 'day9.png')
    print('Visualization completed.')


if __name__ == '__main__':
    main()

# EOF
