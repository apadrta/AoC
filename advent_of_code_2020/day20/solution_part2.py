#!/usr/bin/env python
# -*- coding:utf-8 -*-
"""
Advent of code - 20A
"""

import argparse
import copy
import math
import random
import json
import numpy as np

#==============================================================================


def get_args():
	"""
	Cmd line argument parsing (preprocessing)
	"""
	# Assign description to the help doc
	parser = argparse.ArgumentParser(\
		description='Advent of code 2020')

	# Add arguments
	parser.add_argument(\
		'-i',
		'--infile',
		type=str,
		help='Inputfilename',
		required=True)

	parser.add_argument(\
		'-p',
		'--positions',
		type=str,
		help='Positions inputfilename',
		required=True)

	# Array for all arguments passed to script
	args = parser.parse_args()

	# Return arg variables
	return args.infile, args.positions

#==============================================================================

def main():
	"""
	Main function
	"""

	# process args
	infile, posfile = get_args()

	# read tiles
	data = []
	with open(infile, "r") as fileh:
		data = fileh.readlines()
	lines = [x.strip() for x in data]
	lines.append('')

	tileorder = []
	tiles = {}
	dim = 0
	for line in lines:
		if not line:
			# end of tile
			dim = len(newtile[0])
			fulltile = np.zeros((dim, dim), dtype=int)
			for i in range(0, dim):
				for j in range(0, dim):
					if newtile[i][j] == '#':
						fulltile[i][j] = 1
			tiles[tileid] = []
			tileorder.append(tileid)
			mynewtile = copy.deepcopy(fulltile)
			for rot in range(0, 4):
				for hflip in range(0, 2):
					htile = copy.deepcopy(mynewtile)
					if hflip == 1:
						htile = np.flip(htile, 0)
					for vflip in range(0, 2):
						vtile = copy.deepcopy(htile)
						if vflip == 1:
							vtile = np.flip(vtile, 1)
						#print(vtile)
						tiles[tileid].append(copy.deepcopy(vtile))
						
				prevtile = copy.deepcopy(mynewtile)
				mynewtile = np.rot90(prevtile, axes=(1,0))

		elif line[0:4] == 'Tile':
			newtile = []
			tileid = int(line[5:9])
		else:
			newtile.append(line)

	ntiles = len(tiles)
	#print("Number of tiles", ntiles)
	#print("Tiles size", dim)
	ssize = int(math.sqrt(len(tiles)))
	#print("Square size", ssize)

#	tileorder = [1493, 2503, 1889, 3181, 3989, 3299, 1847, 1993, 2557, 3697, 2879, 1453, 1901, 2297, 3079, 3643, 1607, 2069, 1213, 3631, 3319, 3163, 3049, 1789, 1231, 1009, 3691, 1129, 3761, 1277, 2593, 3673, 2819, 1427, 1747, 1103, 3931, 3119, 1327, 2351, 2833, 1571, 1061, 3637, 2729, 1283, 1523, 1187, 2099, 1933, 2017, 2963, 2381, 1741, 3659, 2549, 3511, 3019, 3803, 3967, 3301, 1543, 2011, 3821, 1201, 2287, 2417, 2851, 3121, 2113, 3671, 1931, 1097, 1597, 2053, 1451, 1321, 1861, 2129, 1613, 2677, 1217, 1583, 3877, 2437, 2803, 3943, 2221, 3499, 1013, 3347, 1877, 1487, 3719, 2777, 1481, 1051, 1381, 2711, 3529, 1979, 2683, 1181, 2137, 2857, 2311, 2389, 2083, 1787, 3331, 2647, 1913, 2699, 3253, 2161, 2467, 2861, 2609, 2801, 1721, 3797, 3259, 3307, 3617, 3929, 3727, 3361, 1579, 2243, 1033, 1237, 3623, 2671, 1091, 2081, 2213, 3041, 2339, 3491, 2357, 2207, 2281, 1039, 2789]
	tileorder = [1291, 2657, 3931, 2203, 3673, 2797, 2861, 1531, 3323, 2617, 1559, 1117, 1009, 1153, 3049, 2251, 1279, 2423, 1019, 1889, 3391, 2467, 1327, 2003, 2389, 2699, 1787, 1907, 2381, 2549, 3677, 3967, 2719, 2857, 1361, 3517, 3671, 3529, 1571, 3257, 2081, 1321, 1129, 2087, 2441, 1993, 3457, 1187, 1627, 2027, 3271, 3301, 3121, 3637, 1249, 1657, 2833, 2671, 3697, 3181, 3137, 1741, 3779, 2341, 3011, 1109, 3727, 2333, 3929, 2161, 1879, 2729, 1601, 1931, 2237, 3343, 2309, 1831, 1319, 2417, 2953, 1439, 1721, 3217, 2803, 3541, 3877, 1637, 1901, 2143, 1619, 2687, 1861, 3803, 3041, 3001, 1621, 3229, 3163, 3347, 1933, 3533, 1489, 2609, 3557, 3371, 2039, 1663, 1039, 1747, 2393, 1847, 2957, 1093, 1231, 1867, 3617, 1949, 2351, 1429, 3373, 1499, 2887, 2791, 1583, 2399, 1609, 1237, 3067, 3413, 2621, 1871, 1213, 1297, 1973, 1021, 2663, 3221, 2269, 2099, 2053, 3467, 2707, 1543]
	# read positions
	data = []
	with open(posfile, "r") as fileh:
		data = fileh.readlines()
	lines = [x.strip() for x in data]
	pos = json.loads(lines[0])
	#print(pos)

	#print(tileorder)
	#print(tileorder[0])
	#print(tiles[tileorder[1]][2])

	wdim = ssize * (dim-2)
	whole = np.zeros((wdim, wdim), dtype=int)
	for x in range(0, ssize):
		for y in range(0, ssize):
			ntile = y * ssize + x
			offset = (x * (dim-2), y * (dim-2))
			tileid = tileorder[pos[ntile][0]]
			posid = pos[ntile][1]
			#print(ntile, offset, pos[ntile], tileid, posid)

			inarr = tiles[tileid][posid]
			#print(inarr)
			whole[offset[1]:offset[1] + dim-2, offset[0]:offset[0] + dim-2] = inarr[1:-1, 1:-1]
	#print(whole)


	monsterstr = ['                  # ', '#    ##    ##    ###', ' #  #  #  #  #  #   ']
	monster = np.zeros((len(monsterstr), len(monsterstr[0])), dtype = int)
	monsterpart = 0
	for y in range(0, len(monsterstr)):
		for x in range(0, len(monsterstr[0])):
			if monsterstr[y][x] == '#':
				monster[y][x] = 1
				monsterpart += 1
	#print(monsterpart)
	#print(monster)

	monsters = []
	newmonster = copy.deepcopy(monster)
	for rot in range(0, 4):
		for hflip in range(0, 2):
			hmonster = copy.deepcopy(newmonster)
			if hflip == 1:
				hmonster = np.flip(hmonster, 0)
			for vflip in range(0, 2):
				vmonster = copy.deepcopy(hmonster)
				if vflip == 1:
					vmonster = np.flip(vmonster, 1)
				#print(vtile)
				monsters.append(copy.deepcopy(vmonster))
				
		prevmonster = copy.deepcopy(newmonster)
		newmonster = np.rot90(prevmonster, axes=(1,0))

	#print(monsters)

	#map the monter position
	mmap = copy.deepcopy(whole)
	for m in monsters:
		#m[(0, 2)] = 10
		#print(m)
		#print(m.shape)
		#print(whole.shape)
		#print(whole.shape[0] - m.shape[0])
		#print(whole.shape[1] - m.shape[1])
		#print("---")
		#print(whole)
		for x in range(0, whole.shape[0] - m.shape[0]+1):
			for y in range(0, whole.shape[1] - m.shape[1]+1):
				pos = (x,y)
				#print((y, x))
				sub = whole[pos[0] : pos[0] + m.shape[0], pos[1] : pos[1] + m.shape[1]]
				msea = np.multiply(m, sub)
				if (msea == m).all():
					#print("Monster at {}".format(pos))
					#print(sub)
					mmap[pos[0] : pos[0] + m.shape[0], pos[1] : pos[1] + m.shape[1]] = np.add(sub, m)
					#print(mmap[pos[0] : pos[0] + m.shape[0], pos[1] : pos[1] + m.shape[1]])

	# count
	print("Part2:", np.sum(mmap==1))



	#print(monsters[0])
	#print(monsters[1])
	#print(monsters[2])
	#print(monsters[3])

	#print(tiles[1951][0])
	#print(tiles[2729][0])



	# print("Part 2: {}".format(res))
	

#==============================================================================

main()

#EOF
