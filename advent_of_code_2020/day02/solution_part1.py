#!/usr/bin/env python
# -*- coding:utf-8 -*-
"""
Advent of code - 2A
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

	valid = 0
	invalid = 0
	for item in data:
		limits, char, passwd = item.split(' ')
		char = char[0]
		passwd = passwd.replace('\n', '').replace('\r', '')
		minlim, maxlim = limits.split('-')
		minlim = int(minlim)
		maxlim = int(maxlim)

		if passwd.count(char) >= minlim and passwd.count(char) <= maxlim:
			valid += 1
		else:
			invalid += 1

	print("valid = {}".format(valid))
	print("invalid = {}".format(invalid))

#==============================================================================

main()

#EOF
