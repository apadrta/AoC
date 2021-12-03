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
	hist = []
	while s < steps:
		if s < len(nums):
			hist.append(nums[s])
		elif hist.count(hist[s-1]) == 1:
			hist.append(0)
		else:
			#last = hist[:-1][::-1].index(hist[s-1]) + 1
			#print(hist[s-1], last)
			hist.append(hist[:-1][::-1].index(hist[s-1]) + 1)
		#print(s, hist)
		s += 1



	print("Part 1: {}".format(hist[-1]))



	

#==============================================================================

main()

#EOF
