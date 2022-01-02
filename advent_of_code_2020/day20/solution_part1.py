#!/usr/bin/env python
# -*- coding:utf-8 -*-
"""
Advent of code - 19A
"""

import argparse
import copy
import math
import random

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

	# Array for all arguments passed to script
	args = parser.parse_args()

	# Return arg variables
	return args.infile


def conditions_ok(state, tiles, tileorder, pos, ssize):
	"""
	evaluete if all border conditions are met
	"""

	#print("  Evaluate pos {}".format(pos))
	#print("  ", state)
	#print(tileorder[state[pos][0]])
	if pos == 0:
		# first is always OK
		return True


	#if pos == 1 and tileorder[state[pos][0]] == 2311 and tileorder[state[pos-1][0]] == 1951:
	#	print("check")
	#	prevborder = tiles[tileorder[state[pos-1][0]]][state[pos-1][1]]
	#	currborder = tiles[tileorder[state[pos][0]]][state[pos][1]]
	#	print(prevborder[3])
	#	print(currborder[2])
	#	print(prevborder[3] == currborder[2])



	if (pos % ssize != 0):
		# no west border check for first column
		prevborder = tiles[tileorder[state[pos-1][0]]][state[pos-1][1]]
		currborder = tiles[tileorder[state[pos][0]]][state[pos][1]]
		
		if prevborder[3] != currborder[2]:
			return False
		
	if (pos >= ssize):
		# no northcheck for first line
		prevborder = tiles[tileorder[state[pos-ssize][0]]][state[pos-ssize][1]]
		currborder = tiles[tileorder[state[pos][0]]][state[pos][1]]
		#print("P[{}] {}".format(tileorder[state[pos-ssize][0]], prevborder[1]))
		#print("C[{}] {}".format(tileorder[state[pos][0]], currborder[0]))
		if prevborder[1] != currborder[0]:
			return False

	return True

#==============================================================================

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

	tiles = {}
	for line in lines:
		if not line:
			# end of tile
			borders = []
			borders.append(newtile[0])  # north
			borders.append(newtile[-1]) # south
			west = ''
			east = ''
			for nt in newtile:
				west += nt[0]
				east += nt[-1]
			borders.append(west)
			borders.append(east)
			tiles[tileid] = []
			newborders = copy.deepcopy(borders)

			for rot in range(0, 4):
				for hflip in range(0, 2):
					hborders = copy.deepcopy(newborders)
					if hflip == 1:
						hborders[2] = newborders[2][::-1]
						hborders[3] = newborders[3][::-1]
						hborders[0] = newborders[1]
						hborders[1] = newborders[0]
					for vflip in range(0, 2):
						vborders = copy.deepcopy(hborders)
						if vflip == 1:
							vborders[0] = hborders[0][::-1]
							vborders[1] = hborders[1][::-1]
							vborders[2] = hborders[3]
							vborders[3] = hborders[2]
						tiles[tileid].append(copy.deepcopy(vborders))
				prevborders = copy.deepcopy(newborders)
				newborders = ['', '', '' , '']
				newborders[3] = prevborders[0]
				newborders[1] = prevborders[3][::-1]
				newborders[2] = prevborders[1]
				newborders[0] = prevborders[2][::-1]
				
						

		elif line[0:4] == 'Tile':
			newtile = []
			tileid = int(line[5:9])
		else:
			newtile.append(line)
	#tiles[tileid] = newtile
	#print(tiles)
	ntiles = len(tiles)
	print("Number of tiles", ntiles)
	ssize = int(math.sqrt(len(tiles)))
	print("Square size", ssize)

	#print(tiles[1951][0])
	#print(tiles[2729][0])


	# start backtracking
	print("Start backtracking")
	state = []
	for i in range(0, ntiles):
		state.append([-1, 0])  
	pos = 0
	tileorder = list(tiles.keys())
	#random.shuffle(tileorder)
	#with open("tileorder.ini.txt", "w") as fileh:
	#	for tileo in tileorder:
	#		fileh.write("{}, ".format(tileo))
	#tileorder = [1493, 2503, 1889, 3181, 3989, 3299, 1847, 1993, 2557, 3697, 2879, 1453, 1901, 2297, 3079, 3643, 1607, 2069, 1213, 3631, 3319, 3163, 3049, 1789, 1231, 1009, 3691, 1129, 3761, 1277, 2593, 3673, 2819, 1427, 1747, 1103, 3931, 3119, 1327, 2351, 2833, 1571, 1061, 3637, 2729, 1283, 1523, 1187, 2099, 1933, 2017, 2963, 2381, 1741, 3659, 2549, 3511, 3019, 3803, 3967, 3301, 1543, 2011, 3821, 1201, 2287, 2417, 2851, 3121, 2113, 3671, 1931, 1097, 1597, 2053, 1451, 1321, 1861, 2129, 1613, 2677, 1217, 1583, 3877, 2437, 2803, 3943, 2221, 3499, 1013, 3347, 1877, 1487, 3719, 2777, 1481, 1051, 1381, 2711, 3529, 1979, 2683, 1181, 2137, 2857, 2311, 2389, 2083, 1787, 3331, 2647, 1913, 2699, 3253, 2161, 2467, 2861, 2609, 2801, 1721, 3797, 3259, 3307, 3617, 3929, 3727, 3361, 1579, 2243, 1033, 1237, 3623, 2671, 1091, 2081, 2213, 3041, 2339, 3491, 2357, 2207, 2281, 1039, 2789]
	tileorder = [1291, 2657, 3931, 2203, 3673, 2797, 2861, 1531, 3323, 2617, 1559, 1117, 1009, 1153, 3049, 2251, 1279, 2423, 1019, 1889, 3391, 2467, 1327, 2003, 2389, 2699, 1787, 1907, 2381, 2549, 3677, 3967, 2719, 2857, 1361, 3517, 3671, 3529, 1571, 3257, 2081, 1321, 1129, 2087, 2441, 1993, 3457, 1187, 1627, 2027, 3271, 3301, 3121, 3637, 1249, 1657, 2833, 2671, 3697, 3181, 3137, 1741, 3779, 2341, 3011, 1109, 3727, 2333, 3929, 2161, 1879, 2729, 1601, 1931, 2237, 3343, 2309, 1831, 1319, 2417, 2953, 1439, 1721, 3217, 2803, 3541, 3877, 1637, 1901, 2143, 1619, 2687, 1861, 3803, 3041, 3001, 1621, 3229, 3163, 3347, 1933, 3533, 1489, 2609, 3557, 3371, 2039, 1663, 1039, 1747, 2393, 1847, 2957, 1093, 1231, 1867, 3617, 1949, 2351, 1429, 3373, 1499, 2887, 2791, 1583, 2399, 1609, 1237, 3067, 3413, 2621, 1871, 1213, 1297, 1973, 1021, 2663, 3221, 2269, 2099, 2053, 3467, 2707, 1543]
	used = []
	s = 0
	while True:
		#print("used", used)
		s += 1
		# find tile on next post

		# pick state to check
		if state[pos][0] == -1:
			# not initialized
			#print("Start on pos {}".format(pos))
			tilei = 0
			while tileorder[tilei] in used:
				tilei += 1
			#print("  Trying ", tileorder[tilei])
			modi = 0
		else:
			#print(tiles[tileorder[tilei]])
			if modi < len(tiles[tileorder[tilei]]) - 1:
				# try next rotation
				modi += 1
			else:
				trynext = True
				# check if all tiles has been tested
				if tilei == len(tileorder) - 1:
					trynext = False
				else:
					# find next unchecked avaialable tile
					while tilei < len(tileorder) - 1:
						tilei += 1	
						if tileorder[tilei] not in used:
							break
					
				if tilei >= len(tileorder):
					trynext = False
				if trynext:
					#print("  Trying ", tileorder[tilei])
					modi = 0
				else:
					#print("< Go back to pos {}".format(pos -1))
					# no other tiles - go one step back
					state[pos] = [-1, -1]
					#print(state)
					pos -= 1
					used.remove(tileorder[state[pos][0]])
					tilei = state[pos][0]
					modi = state[pos][1]
					
					continue
					
		# check validity of placed tile
		state[pos] = [tilei, modi]
		#print("Try to place tile {} (mod {}) to pos {}".format(tileorder[tilei], modi, pos))
		if conditions_ok(state, tiles, tileorder, pos, ssize):
			
			used.append(tileorder[tilei])
			tileid = tileorder[tilei]

			#print("> Placed {} [mod {}]".format(tileid, modi))
			#print("  used", used)
			#print("  state", state)
			pos += 1
			if pos >= len(tileorder):
				# all tiles placed
				break

		if s % 10000000 == 0:
			print(state)

	print(state)
	print("Part 1: {}".format(tileorder[state[0][0]] * tileorder[state[ssize -1][0]] * tileorder[state[-1][0]] * tileorder[state[-ssize][0]] ))

	# print("Part 2: {}".format(res))
	

#==============================================================================

main()

#EOF
