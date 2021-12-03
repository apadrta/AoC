#!/usr/bin/env python
# -*- coding:utf-8 -*-
"""
Advent of code - 24A
"""

import argparse
import string

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

	# split to paths description
	paths = []
	for line in lines:
		#e, se, sw, w, nw, and ne
		path = []
		i = 0
		while i < len(line):
			if line[i] in ['e', 'w']:
				path.append(line[i])
				i += 1
			else:
				path.append(line[i:i+2])
				i += 2
		paths.append(path)
	#print(paths)

	# compute target coordinates

	diffs = {'e' : [1,0], 'se' : [0, -1], 'sw' : [-1, -1], 'w' : [-1,0], 'nw' : [0,1],  'ne' : [1,1]}


	tiles = {}	# 0 = white, 1 = black
	for path in paths:
		#print(path)
		pos = [0, 0]
		for p in path:
			pos[0] += diffs[p][0]
			pos[1] += diffs[p][1]
			#print(p, pos)
		if tuple(pos) in tiles:
			# flip over
			tiles[tuple(pos)] = (tiles[tuple(pos)] + 1) % 2
		else:
			# flip to black
			tiles[tuple(pos)] = 1
		
	#print(tiles)
	summ = 0
	for value in tiles.values():
		if value == 1:
			summ += 1


	print("Part 1:", summ)

	s = 0
	while s < 100:
		#print("Step =",s+1)
		mini = [0, 0]
		maxi = [0, 0]
		newtiles = {}
		for tile in tiles:
			if tile[0] < mini[0]:
				mini[0] = tile[0]
			if tile[1] < mini[1]:
				mini[1] = tile[1]
			if tile[0] > maxi[0]:
				maxi[0] = tile[0]
			if tile[1] > maxi[1]:
				maxi[1] = tile[1]
		for x in range(mini[0]-1, maxi[0]+2):
			for y in range(mini[1]-1, maxi[1]+2):
				#compute adjanced black
				black = 0
				for d in diffs.values():
					#print(d)
					check = (x + d[0], y + d[1])
					if check in tiles and tiles[check] == 1:
						black += 1
				#print(black)
				if black in [1, 2] and (x, y) in tiles and tiles[(x, y)] == 1:
					# black stays black
					newtiles[(x, y)] = 1
				if black == 2 and ((x, y) not in tiles or tiles[(x, y)] == 0):
					newtiles[(x, y)] = 1
		tiles = newtiles

		summ = 0
		for value in tiles.values():
			if value == 1:
				summ += 1
		print("Day {}: {}".format( s+1, summ))

		s +=1

#==============================================================================

main()

#EOF
