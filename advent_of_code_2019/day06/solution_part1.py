#!/usr/bin/env python
# -*- coding:utf-8 -*-
"""
Advent of code - 6A
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

def path2com(paths, start):
	"""
	get list of systems visited when going from start to com
	"""
	path = []
	curr = start
	while curr != 'COM':
		#print(curr)
		path.append(paths[curr])
		curr = paths[curr]
	return path

#==============================================================================

def main():
	"""
	Main function
	"""

	# process args
	infile = get_args()

	# read data
	rdata = []
	with open(infile, "r") as fileh:
		rdata = fileh.readlines()

	data = [x.strip() for x in rdata]

	# make dict
	ptrs = {}
	todo = []
	for item in data:
		value, key = item.split(')')
		ptrs[key] = value
		todo.append(key)

	# assign path lengths
	paths = {'COM' : 0}
	while todo:
		#print(len(todo))
		for key in todo:
			if ptrs[key] in paths:
				paths[key] = paths[ptrs[key]] + 1
				todo.remove(key)
	
	# sum paths lengths
	#print(paths)
	summary = 0
	for value in paths.values():
		summary += value
	print("part1: {}".format(summary))


	youpath = path2com(ptrs, 'YOU')[::-1]
	sanpath = path2com(ptrs, 'SAN')[::-1]

	i = 0
	while youpath[i] == sanpath[i]:
		i += 1
	print(youpath[(i-1)::][::-1])
	print(sanpath[(i-1)::])


	#print(youpath)
	#print(sanpath)


	print("part2: {}".format(len(youpath[(i-1)::]) + len(sanpath[(i-1)::]) - 2))







#==============================================================================

main()

#EOF
