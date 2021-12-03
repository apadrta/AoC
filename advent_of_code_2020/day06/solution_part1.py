#!/usr/bin/env python
# -*- coding:utf-8 -*-
"""
Advent of code - 6AB
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
	lines = [x.strip() for x in data] + ['']

	groups = []
	total = 0
	total2 = 0
	group = ''
	for line in lines:
		if not line:
			#print(group)
			#print(set(group))
			#print(len(set(group)))
			total = total + len(set(group))
			groups.append(group)
			#print(groups)
			allg = set(groups[0])
			for g in groups:
				#print("  ", g)
				allg = allg.intersection(set(g))
				#print("  ", allg)
			#print("  ", len(allg))
			total2 = total2 + len(allg)
			group = ''
			groups = []
		else:
			group = group + line
			groups.append(line)

	print("Part 1: {}".format(total))
	print("Part 2: {}".format(total2))
	

#==============================================================================

main()

#EOF
