#!/usr/bin/env python
# -*- coding:utf-8 -*-
"""
Advent of code - 10A
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
	lines = [int(x.strip()) for x in data]

	lines = sorted(lines + [0] + [max(lines) + 3])

	# part one
	i = 1
	diffs = {}
	while i < len(lines):
		diff = lines[i] - lines[i-1]
		if diff in diffs:
			diffs[diff] += 1
		else:
			diffs[diff] = 1
		i += 1
	print("Part 1: {}".format(diffs[1] * diffs[3]))
	
	# part two

	graph = []
	i = 0
	while i < len(lines): 
		j = i + 1
		while j < len(lines):
			if lines[j] - lines[i] <= 3:
				graph.append([lines[i], lines[j]])
			else:
				break
			j += 1
		i += 1

	paths = {0 : 1}
	checks = [0]
	checked = []
	end = max(lines)
	while checks:
		newchecks = []
		for fromnode, tonode in graph:
			if fromnode in checks and fromnode not in checked and fromnode in paths:
				if tonode in paths:
					paths[tonode] += paths[fromnode]
				else:
					paths[tonode] = paths[fromnode]
				newchecks.append(tonode)
		checked.extend(checks)
		checks = newchecks
	
	print("Part2: {}".format(paths[max(lines)]))

#==============================================================================

main()

#EOF
