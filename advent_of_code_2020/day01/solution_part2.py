#!/usr/bin/env python
# -*- coding:utf-8 -*-
"""
Advent of code - 1B
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
	nums = [int(x.replace('\n', '').replace('\r', '')) for x in data]
	nums = sorted(nums)
	print(nums)

	for x in nums:
		for y in nums:
			for z in nums:
				if x + y + z == 2020:
					print("{0} + {1} + {2} = {3}\n{0} * {1} * {2} = {4}".format(x, y, z, x+y+z, x*y*z))
					break
			if x + y + z == 2020:
				break
		if x + y +z == 2020:
			break



#==============================================================================

main()

#EOF
