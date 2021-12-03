#!/usr/bin/env python
# -*- coding:utf-8 -*-
"""
Advent of code - 15A
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
	parser.add_argument(\
		'-s',
		'--steps',
		type=int,
		help='Number of simulation steps',
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
	infile,steps = get_args()

	# read data
	data = []
	with open(infile, "r") as fileh:
		data = fileh.readlines()
	lines = [x.strip() for x in data]

	nums = [int(x) for x in lines[0].split(',')]

	s = 0
	hist = {}
	last = 0
	while s < steps:
		if s < len(nums):
			hist[nums[s]] = [s, -1]  # [index, previndex]
			last = nums[s]
		elif hist[last][1] == -1:
			if 0 in hist:
				hist[0][1] = hist[0][0]
				hist[0][0] = s
			else:
				hist[0] = [s, -1]
			last = 0
		else:
			new =  hist[last][0] - hist[last][1]
			if new in hist:
				hist[new][1] = hist[new][0]
				hist[new][0] = s
			else:
				hist[new] = [s, -1]
			last = new

		#print(s, last, hist)
		s += 1

	print("Part 2: {}".format(last))



	

#==============================================================================

main()

#EOF
