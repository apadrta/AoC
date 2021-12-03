#!/usr/bin/env python
# -*- coding:utf-8 -*-
"""
Advent of code - 3A
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
	data = [x.replace('\n', '').replace('\r', '') for x in data]
	height = len(data)
	width = len(data[0])
	slope = 3
	tree = '#'
	
	print('block size = {} x {}'.format(width, height))

	index = 1
	pos = 1
	treeshit = 0
	for item in data:
		if item[index - 1] == tree:
			treeshit += 1
		#print(pos, index)
		pos = pos + slope
		index = pos % width
	print('Trees hit: {}'.format(treeshit))
		



#==============================================================================

main()

#EOF
