#!/usr/bin/env python
# -*- coding:utf-8 -*-
"""
Advent of code - 12A
"""

import argparse

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

	# read rules
	moves = []
	for line in lines:
		moves.append([line[0], int(line[1:])])

	x = 0
	y = 0
	wx = 10
	wy = 1
	heading = 1 # 0 = N, 1 = E, 2 = S, 3 = W

	for move in moves:
		if move[0] == 'N':
			wy += move[1]
		elif move[0] == 'S':
			wy -= move[1]
		elif move[0] == 'E':
			wx += move[1]
		elif move[0] == 'W':
			wx -= move[1]
		elif move[0] == 'L':
			for i in range(0, int(move[1]/90)):
				newy = wx
				newx = -wy
				wx = newx
				wy = newy
		elif move[0] == 'R':
			for i in range(0, int(move[1]/90)):
				newy = -wx
				newx = wy
				wx = newx
				wy = newy
		elif move[0] == 'F':
			y += wy * move[1]
			x += wx * move[1]
		#print(move, wx, wy, x, y)

	#print(x, y)

	print("Part 2: {}".format(abs(x) + abs(y)))


#==============================================================================

main()

#EOF
