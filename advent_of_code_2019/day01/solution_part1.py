#!/usr/bin/env python
# -*- coding:utf-8 -*-
"""
Advent of code - 1A
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
	nums = [float(x.strip()) for x in data]

	fuel = 0
	for x in nums:
		newf = floor(x / 3.0) - 2
		fuel += newf
	print("Total fuel: {}".format(fuel))

#==============================================================================

main()

#EOF
