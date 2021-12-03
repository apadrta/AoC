#!/usr/bin/env python
# -*- coding:utf-8 -*-
"""
Advent of code - 3A
"""

import argparse
from math import floor

#==============================================================================


def get_args():
	"""
	Cmd line argument parsing (preprocessing)
	"""
	# Assign description to the help doc
	parser = argparse.ArgumentParser(\
		description='Advent of code 2019')

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

def get_wirepart(data):
	"""
	compute max range
	"""
	parts = []
	start = (0, 0)
	for i in data:
		direction = i[0]
		size = int(i[1:])
		xdelta = 0
		ydelta = 0
		if direction == 'U':
			ydelta = size
		elif direction == 'D':
			ydelta = -size
		if direction == 'R':
			xdelta = size
		if direction == 'L':
			xdelta = -size

		end = (start[0] + xdelta, start[1] + ydelta)
		parts.append((start, end))
		start = end

	return parts

#==============================================================================

def get_crosspoints(red, blue):
	"""
	Compute crossing points
	"""

	cross = []
	for r in red:
		for b in blue:
			if r[0][0] == r[1][0]:
				# red is vertical
				if b[0][0] == b[1][0]:
					# blue is vertical
					#print('both vertical')
					continue
				else:
					# blue is horizontal
					if min(r[0][1], r[1][1]) < b[0][1] and b[0][1] < max(r[0][1], r[1][1]) and min(b[0][0], b[1][0]) < r[0][0] and r[0][0] < max(b[0][0], b[1][0]):
						cross.append((r[0][0], b[0][1]))
			else:
				# red is horizontal
				if b[0][0] == b[1][0]:
					# blue is vertical
					if min(b[0][1], b[1][1]) < r[0][1] and r[0][1] < max(b[0][1], b[1][1]) and min(r[0][0], r[1][0]) < b[0][0] and b[0][0] < max(r[0][0], r[1][0]):
						cross.append((r[0][1], b[0][0]))					
				else:
					# blue is horizontal
					#print('both horizontal')
					continue
	return cross

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
	wire_a = [x for x in data[0].strip().split(',')]
	wire_b = [x for x in data[1].strip().split(',')]

	parts_a = get_wirepart(wire_a)
	parts_b = get_wirepart(wire_b)

	cross = get_crosspoints(parts_a, parts_b)

	print(wire_a)
	print(wire_b)
	print(parts_a)
	print(parts_b)
	print(cross)

	dists = []
	for c in cross:
		dists.append(abs(c[0])+abs(c[1]))
	print(min(dists))

#==============================================================================

main()

#EOF
