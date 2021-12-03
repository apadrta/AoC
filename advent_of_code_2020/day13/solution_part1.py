#!/usr/bin/env python
# -*- coding:utf-8 -*-
"""
Advent of code - 13A
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
	lines = [x.strip() for x in data]

	# read rules
	depart = int(lines[0])
	buses = [int(x) for x in lines[1].split(',') if x != 'x']

	minbus = 0
	minwait = max(buses)
	for bus in buses:
		wait = bus - (depart % bus)
		if wait < minwait:
			minwait = wait
			minbus = bus
	print(minwait, minbus)
	print("Part 1: {}".format(minwait * minbus))


#==============================================================================

main()

#EOF
