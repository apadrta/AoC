#!/usr/bin/env python
# -*- coding:utf-8 -*-
"""
Advent of code - 3B
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

def trees_enc(data, tree, xslope, yslope):
	"""
	Count encoutered trees
	"""
	height = len(data)
	width = len(data[0])

	index = 1
	pos = 1
	treeshit = 0
	for item in data[::yslope]:
		if item[index - 1] == tree:
			treeshit += 1
		pos = pos + xslope
		index = pos % width
	return treeshit


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

	tree = '#'	
	res1 = trees_enc(data, tree, 1, 1)
	res2 = trees_enc(data, tree, 3, 1)
	res3 = trees_enc(data, tree, 5, 1)
	res4 = trees_enc(data, tree, 7, 1)
	res5 = trees_enc(data, tree, 1, 2)
	print('Trees hit 1-1: {}'.format(res1))
	print('Trees hit 3-1: {}'.format(res2))
	print('Trees hit 5-1: {}'.format(res3))
	print('Trees hit 7-1: {}'.format(res4))
	print('Trees hit 1-2: {}'.format(res5))
	print('multipla: {}'.format(res1 * res2 * res3 * res4 * res5))
		



#==============================================================================

main()

#EOF
