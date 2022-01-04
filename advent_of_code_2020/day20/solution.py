#!/usr/bin/env python
# -*- coding:utf-8 -*-
"""
Advent of code 2020 - Day 20
"""

import argparse
import copy
import math
import numpy as np


def get_args():
    """
    Cmd line argument parsing (preprocessing)
    """
    # Assign description to the help doc
    parser = argparse.ArgumentParser(
        description='Advent of code 2020 - Day 20')

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


def create_monsters():
    """
    create monster representations
    """
    # create basic representation
    monsterstr = [
        '                  # ',
        '#    ##    ##    ###',
        ' #  #  #  #  #  #   ']
    monster = np.zeros((len(monsterstr), len(monsterstr[0])), dtype=int)
    monsterpart = 0
    for j, _ in enumerate(monsterstr):
        for i in range(len(monsterstr[0])):
            if monsterstr[j][i] == '#':
                monster[j][i] = 1
                monsterpart += 1
    monsters = []
    # add base position
    monsters.append(monster)
    # rotate base position
    for _ in range(3):
        newmonster = copy.deepcopy(monster)
        monster = np.rot90(newmonster, 3)
        monsters.append(monster)
    # flip position
    newmonster = copy.deepcopy(monster)
    monster = np.flip(newmonster, 0)
    monsters.append(monster)
    # rotate flipped position
    for _ in range(3):
        newmonster = copy.deepcopy(monster)
        monster = np.rot90(newmonster, 3)
        monsters.append(monster)

    return monsters


def prepare_tiles(lines):
    """
    Prepare tiles from data
    """
    tiles = {}
    tileid = -1
    newtile = []
    for line in lines:
        if not line:
            # create base position
            borders = []
            borders.append(newtile[0])  # north
            west = ''
            east = ''
            for newt in newtile:
                west += newt[0]
                east += newt[-1]
            borders.append(east)
            borders.append(newtile[-1])  # south
            borders.append(west)
            tiles[tileid] = []
            tiles[tileid].append(borders)
            # rotate base position
            for _ in range(3):
                newborders = ['', '', '', '']
                newborders[0] = copy.deepcopy(borders[3][::-1])
                newborders[1] = copy.deepcopy(borders[0])
                newborders[2] = copy.deepcopy(borders[1][::-1])
                newborders[3] = copy.deepcopy(borders[2])
                borders = newborders
                tiles[tileid].append(borders)
            # flip position
            newborders = ['', '', '', '']
            newborders[1] = copy.deepcopy(borders[1][::-1])
            newborders[3] = copy.deepcopy(borders[3][::-1])
            newborders[0] = copy.deepcopy(borders[2])
            newborders[2] = copy.deepcopy(borders[0])
            borders = newborders
            tiles[tileid].append(borders)
            # rotate flipped position
            for _ in range(3):
                newborders = ['', '', '', '']
                newborders[0] = copy.deepcopy(borders[3][::-1])
                newborders[1] = copy.deepcopy(borders[0])
                newborders[2] = copy.deepcopy(borders[1][::-1])
                newborders[3] = copy.deepcopy(borders[2])
                borders = newborders
                tiles[tileid].append(borders)
            # convert to number
            for i in range(8):
                for j in range(4):
                    number = int(tiles[tileid][i][j].replace('.', '0').replace('#', '1'), 2)
                    tiles[tileid][i][j] = number
        elif line[0:4] == 'Tile':
            # start of new tile
            newtile = []
            tileid = int(line[5:9])
        else:
            # add line to tile
            newtile.append(line)
    return tiles


def prepare_full_tiles(lines):
    """
    Prepare full tiles and its rotations
    """
    tiles = {}
    newtile = []
    tileid = -1
    emptylines = 0
    dim = 0
    for line in lines:
        if not line:
            emptylines += 1
        else:
            emptylines = 0
        if emptylines == 2:
            break
        if not line:
            # end of tile
            dim = len(newtile[0])
            fulltile = np.zeros((dim, dim), dtype=int)
            for i in range(0, dim):
                for j in range(0, dim):
                    if newtile[i][j] == '#':
                        fulltile[i][j] = 1
            tiles[tileid] = []
            # add basic tile
            tiles[tileid].append(fulltile)
            # rotate base position
            for _ in range(3):
                newtile = copy.deepcopy(fulltile)
                fulltile = np.rot90(newtile, 3)
                tiles[tileid].append(fulltile)
            # flip position
            newtile = copy.deepcopy(np.flip(fulltile, 0))
            fulltile = newtile
            tiles[tileid].append(fulltile)
            # rotate flipped position
            for _ in range(3):
                newtile = copy.deepcopy(fulltile)
                fulltile = np.rot90(newtile, 3)
                tiles[tileid].append(fulltile)
        elif line[0:4] == 'Tile':
            newtile = []
            tileid = int(line[5:9])
        else:
            newtile.append(line)
    return tiles


def check_connections(tiles):
    """
    check number of possibe connections for zero position
    """
    conns = {}
    for tile_source_id in tiles.keys():
        conns[tile_source_id] = [0, 0, 0, 0]  # north, east, south, west
        for check_id in tiles.keys():
            if tile_source_id == check_id:
                continue
            for check_pos in range(8):
                if tiles[tile_source_id][0][0] == tiles[check_id][check_pos][2]:
                    # connected to north
                    conns[tile_source_id][0] += 1
                elif tiles[tile_source_id][0][2] == tiles[check_id][check_pos][0]:
                    # connected to south
                    conns[tile_source_id][2] += 1
                elif tiles[tile_source_id][0][1] == tiles[check_id][check_pos][3]:
                    # connected to east
                    conns[tile_source_id][1] += 1
                elif tiles[tile_source_id][0][3] == tiles[check_id][check_pos][1]:
                    # connected to west
                    conns[tile_source_id][3] += 1
    return conns


def organize_tiles(tiles, topleft):
    """
    Main function
    """
    ssize = int(math.sqrt(len(tiles)))
    known = {}
    queue = copy.deepcopy(list(tiles.keys()))
    for i in range(ssize):
        for j in range(ssize):
            if i == 0 and j == 0:
                # initialize
                queue.remove(topleft)
                known = {(0, 0): [topleft, 0]}  # (raster posititon): [tile_id, tile_position]
                continue
            target = []
            for tile in queue:
                for pos in range(8):
                    # check east connection
                    if (i-1, j) in known and \
                            tiles[known[(i-1, j)][0]][known[(i-1, j)][1]][1] == tiles[tile][pos][3]:
                        target = [tile, pos]
                        break
                    # check north connection
                    if (i, j-1) in known and \
                            tiles[known[(i, j-1)][0]][known[(i, j-1)][1]][2] == tiles[tile][pos][0]:
                        target = [tile, pos]
                        break
                if target:
                    queue.remove(tile)
                    known[(i, j)] = target
                    break
    return known


def make_big_picture(tiles, organisation):
    """
    create big picture according to tiles organisation
    """
    ssize = int(math.sqrt(len(tiles)))
    dim = np.size(tiles[list(tiles.keys())[0]][0], 0)
    fulldim = (dim-2)*ssize
    image = np.zeros((fulldim, fulldim), dtype=int)
    for i in range(ssize):
        for j in range(ssize):
            tile = tiles[organisation[(j, i)][0]][organisation[(j, i)][1]]
            image[i*(dim-2):(i+1)*(dim-2), j*(dim-2):(j+1)*(dim-2)] = tile[1:dim-1, 1:dim-1]
    return image


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
    lines.append('')

    # convert lines to tiles
    tiles = prepare_tiles(lines)
    ssize = int(math.sqrt(len(tiles)))
    # find top left corner
    connections = check_connections(tiles)
    topleft = -1
    for key, value in connections.items():
        if value == [0, 1, 1, 0]:
            topleft = key
    # organize tiles
    known = organize_tiles(tiles, topleft)

    # part 1 solution
    corner_multi = known[(0, 0)][0] * \
        known[(0, ssize-1)][0] * \
        known[(ssize-1, 0)][0] * \
        known[(ssize-1, ssize-1)][0]
    print(f"Part 1 solution: {corner_multi}")

    # define monsters
    monsters = create_monsters()

    # prepare full tiles and its rotations
    fulltiles = prepare_full_tiles(lines)

    # create one big picture
    picture = make_big_picture(fulltiles, known)

    # map the monter position
    mmap = copy.deepcopy(picture)
    for mon in monsters:
        for i in range(picture.shape[0] - mon.shape[0] + 1):
            for j in range(picture.shape[1] - mon.shape[1] + 1):
                pos = (i, j)
                sub = picture[pos[0]: pos[0] + mon.shape[0], pos[1]: pos[1] + mon.shape[1]]
                msea = np.multiply(mon, sub)
                if (msea == mon).all():
                    mmap[pos[0]: pos[0] + mon.shape[0], pos[1]: pos[1] + mon.shape[1]] = np.add(sub, mon)

    # part 2 solution
    print(f"Part 2 solution: {np.sum(mmap==1)}")


if __name__ == '__main__':
    main()


# EOF
