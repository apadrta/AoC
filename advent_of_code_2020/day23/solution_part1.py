#!/usr/bin/env python
# -*- coding:utf-8 -*-
"""
Advent of code - 23A
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
	parser.add_argument(\
		'-s',
		'--steps',
		type=int,
		help='number of steps',
		required=True)

	# Array for all arguments passed to script
	args = parser.parse_args()

	# Return arg variables
	return args.infile, args.steps


#==============================================================================


def main():
	"""
	Main function
	"""

	# process args
	infile, steps = get_args()

	# read data
	data = []
	with open(infile, "r") as fileh:
		data = fileh.readlines()
	lines = [x.strip() for x in data]

	cups = []
	for c in lines[0]:
		cups.append(int(c))
	#print(cups)

	s = 0
	ncups = len(cups)
	while s < steps:
		#print("Step {}".format(s+1))
		ci = cups[0]
		c3 = cups[1:4]
		d = ci - 1
		if d < 1:
			d = 9
		while d in c3:
			d -= 1
			if d < 1:
				d = 9
		di = cups.index(d)
		#print(  "input", cups)
		#print("  current: {}, cups3 {}, destination {}".format(ci, c3, cups[di]))
		# move three cups to final position
		#print([cups[0]])
		#print([cups[4:di+1]])
		#print(c3)
		#print([cups[di+1:]])
		cups = [cups[0]] + cups[4:di+1] + c3 + cups[di+1:]
		#print("  output", cups)


		# rotate (first is always current)
		cups = cups[1:] + [cups[0]]
		s += 1

	#print(cups)
	i = cups.index(1)
	cups = cups[i+1:] + cups[:i]
	#print(cups)
	os = ''
	for c in cups:
		os += str(c)
	#print(os)

	print("Part 1:", os)

#==============================================================================

main()

#EOF
