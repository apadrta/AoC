#!/usr/bin/env python
# -*- coding:utf-8 -*-
"""
Advent of code - 9AB
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
	parser.add_argument(\
		'-p',
		'--preambule',
		type=int,
		help='Preambule length',
		required=True)

	# Array for all arguments passed to script
	args = parser.parse_args()

	# Return arg variables
	return args.infile, args.preambule


#==============================================================================

def is_valid(pool, item):
	"""
	check validity
	"""
	for i in range(0, len(pool)):
		for j in range(i+1, len(pool)):
			if pool[i] + pool[j] == item:
				return True
	return False
			



def main():
	"""
	Main function
	"""

	# process args
	infile, preamble = get_args()

	# read data
	data = []
	with open(infile, "r") as fileh:
		data = fileh.readlines()
	lines = [int(x.strip()) for x in data]

	# init preamble
	pool_start = 0
	pool_end = preamble + pool_start
	first = 0

	# part one
	for value in lines[preamble:]:
		if is_valid(lines[pool_start:pool_end], value):
			pool_start += 1
			pool_end += 1
		else:
			first = value
			print("Part 1: {}".format(first))
			break

	# part two
	for i in range(0, len(lines)):
		summ = 0
		for j in range(i, len(lines)):
			summ += lines[j]
			if summ > first:
				break
			elif summ == first:
				print("Part 2: {}".format(min(lines[i:j+1]) + max(lines[i:j+1])))
				break
		if summ == first:
			break

	

#==============================================================================

main()

#EOF
