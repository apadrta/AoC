#!/usr/bin/env python
# -*- coding:utf-8 -*-
"""
Advent of code - 3B
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

def get_wirepart_points(data):
	"""
	compute max range
	"""
	#print(data)
	parts = []
	start = (0, 0)
	for i in data:
		#print(i)
		direction = i[0]
		size = int(i[1:])
		xdelta = 0
		ydelta = 0
		xadd = 0
		yadd = 0
		if direction == 'U':
			ydelta = size
			yadd = 1
		elif direction == 'D':
			ydelta = -size
			yadd = -1
		if direction == 'R':
			xdelta = size
			xadd = 1
		if direction == 'L':
			xdelta = -size
			xadd = -1

		part = [start]
		for x in range(0, abs(xdelta) + 1):
			for y in range(0, abs(ydelta) + 1):
				#print(part)
				part.append((part[-1][0] + xadd, part[-1][1] + yadd))
		parts.append(part[:-1])
		start = part[-2]
		#print("New start: {}".format(start))

	return parts

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

	parts_a = get_wirepart_points(wire_a)
	parts_b = get_wirepart_points(wire_b)


	points_a = [(0, 0)]
	for x in parts_a:
		points_a.extend(x[1:])
	points_b = [(0, 0)]
	for x in parts_b:
		points_b.extend(x[1:])

	# get crossings (for part 1)
	set_a = set(points_a)
	set_b = set(points_b)

	cross = set_a & set_b - {(0, 0)}
	clen = min([abs(x[0])+abs(x[1]) for x in cross])
	#cross = get_crosspoints(parts_a, parts_b)

	# get length to crossing (for part 2)

	cpaths = []
	for c in cross:
		cpaths.append(points_a.index(c) + points_b.index(c))
	cpath = min(cpaths)

	#print(wire_a)
	#print(wire_b)
	#print(parts_a)
	#print(parts_b)
	#print(points_a)
	#print(points_b)
	#print(len(parts_a))
	#print(len(parts_b))
	#print(len(set_a))
	#print(len(set_b))
	#print(cross)
	print("part1: {}".format(clen))
	print("part2: {}".format(cpath))

	#dists = []
	#for c in cross:
	#	dists.append(abs(c[0])+abs(c[1]))
	#print(min(dists))

#==============================================================================

main()

#EOF
