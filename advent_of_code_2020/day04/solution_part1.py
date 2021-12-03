#!/usr/bin/env python
# -*- coding:utf-8 -*-
"""
Advent of code - 4A
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

	item = {}
	valid = 0
	for line in lines:
		if not line:
			print(item)
			if len(item) == 8 or (len(item) == 7 and 'cid' not in item):
				print('VALID')
				valid += 1
			item = {}
		else:
			parts = line.split(' ')
			for part in parts:
				key, value = part.split(':')
				item[key] = value

	print("Valid passports: {}".format(valid))
	



#==============================================================================

main()

#EOF
