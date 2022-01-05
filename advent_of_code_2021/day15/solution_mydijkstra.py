#!/usr/bin/env python
# -*- coding:utf-8 -*-
"""
Advent of code 2021 - Day 15
"""

import argparse
import numpy as np
from dijkstar import Graph, find_path


def get_args():
    """
    Cmd line argument parsing (preprocessing)
    """
    # Assign description to the help doc
    parser = argparse.ArgumentParser(
        description='Advent of code 2021: Day 15')

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


def increase_danger(tile):
    """
    increase danger by one
    """
    size = np.size(tile, 0)
    for i in range(0, size):
        for j in range(0, size):
            tile[i, j] += 1
            if tile[i, j] > 9:
                tile[i, j] = 1
    return tile


def enlarge_floor(tile, repeat):
    """
    create larger floor (square)
    """
    size = np.size(tile, 0)
    newsize = size * repeat
    newmap = np.full((newsize, newsize), -1, dtype=int)
    for k in range(0, repeat * 2 - 1):
        if k < repeat:
            minrange = 0
            maxrange = k + 1
        else:
            minrange = k - repeat + 1
            maxrange = repeat
        for i in range(minrange, maxrange):
            pos = (i, k-i)
            newmap[pos[0]*size:(pos[0]+1)*size, pos[1]*size:(pos[1]+1)*size] = tile
        tile = increase_danger(tile)
    return newmap


def get_danger(floor):
    """
    Get cumulative danger optimal
    """
    size = np.size(floor, 0)
    graph = Graph()
    for i in range(0, size):
        for j in range(0, size):
            if j < size - 1:
                graph.add_edge((i*size)+j, (i*size)+(j+1), floor[(i, j+1)])
                graph.add_edge((i*size)+(j+1), (i*size)+j, floor[(i, j)])
            if i < size - 1:
                graph.add_edge((i*size)+j, (i+1)*size+j, floor[(i+1, j)])
                graph.add_edge((i+1)*size+j, (i*size)+j, floor[(i, j)])
    return find_path(graph, 0, size*size-1)


class MyDijkstra():
    """
    Own implementaion of Dijkstra algorithm (bodik can enjoy :-))
    """

    def __init__(self):
        """
        constructor
        """
        self.nodes = None
        self.edges_str = {}

    def add_edge(self, src, dst, value):
        """
        add edge to edges structure
        """
        if src not in self.edges_str:
            self.edges_str[src] = {}
        self.edges_str[src][dst] = value

    def set_data(self, data):
        """
        add data
        """
        sizex = np.size(data, 0)
        sizey = np.size(data, 1)
        self.nodes = []
        for i in range(sizex):
            for j in range(sizey):
                # update list of nodes
                self.nodes.append(i*sizey + j)
                # update transition structure
                if i < sizex - 1:
                    self.add_edge(i*sizey + j, (i+1)*sizey + j, data[i+1, j])
                if i > 0:
                    self.add_edge(i*sizey + j, (i-1)*sizey + j, data[i-1, j])
                if j < sizey - 1:
                    self.add_edge(i*sizey + j, (i)*sizey + j+1, data[i, j+1])
                if j > 0:
                    self.add_edge(i*sizey + j, (i)*sizey + j-1, data[i, j-1])

    def compute_path(self, start, end):
        """
        compute minimal path from start to end
        """
        # initialize
        unvisited_nodes = {}
        visited_nodes = {}
        for node in self.nodes:
            unvisited_nodes[node] = [-1, -1]   # node: [value, path_from]
        # start at... start
        src_node = start
        unvisited_nodes[src_node][0] = 0
        i = 0
        while unvisited_nodes:
            [src_value, path_from] = unvisited_nodes.pop(src_node)
            # evaluate nodes accessible from source
            if src_node in self.edges_str:
                for dst_node, value in self.edges_str[src_node].items():
                    if dst_node not in unvisited_nodes:
                        continue
                    distance = src_value + value
                    if unvisited_nodes[dst_node][0] == -1 or unvisited_nodes[dst_node][0] > distance:
                        unvisited_nodes[dst_node] = [distance, src_node]

            visited_nodes[src_node] = [src_value, path_from]
            # end optimalization
            if src_node == end:
                break
            # find unvisited node with minimal value
            min_node = -1
            for node, node_value in unvisited_nodes.items():
                if node_value[0] != -1 and (min_node == -1 or node_value[0] < unvisited_nodes[min_node][0]):
                    min_node = node
            src_node = min_node
            i += 1
            if i % 1000 == 0:
                print(f".", end='', flush=True)

        # generate path
#        path = []
#        node = end
#        while node != -1:
#            path.append(node)
#            node = visited_nodes[node][1]
#        print(path)
#        path = path[::-1]
#        last = path[0]
#        for item in path[1:]:
#            print(f"{last} ({self.edges_str[last][item]}) ", end="")
#            last = item
#        print(last)
        return visited_nodes[end][0]


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

    # first part
    danger = np.zeros((len(lines), len(lines[0])), dtype=int)
    i = 0
    for line in lines:
        j = 0
        for char in line:
            danger[(i, j)] = int(char)
            j += 1
        i += 1

    # part 1
    res = get_danger(danger)
    print(f"Part 1 solution: {res.total_cost}")

    obj = MyDijkstra()
    obj.set_data(danger)
    res = obj.compute_path(0, np.size(danger, 0) * np.size(danger, 0) - 1)
    print(res)
    # part 2
    newdanger = enlarge_floor(danger, 5)
    res = get_danger(newdanger)
    print(f"Part 2 solution: {res.total_cost}")
    obj = MyDijkstra()
    obj.set_data(newdanger)
    res = obj.compute_path(0, 5 * np.size(danger, 0) * 5 * np.size(danger, 0) - 1)
    print(res)


if __name__ == '__main__':
    main()

# EOF
