#!/usr/bin/env python
# -*- coding:utf-8 -*-
"""
Advent of code - 14A
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

	memory = {}
	mask = 36 * 'X'

	for line in lines:
		inst, value = line.split(' = ')
		if inst == 'mask':
			mask = value
			#print('MASK')
			#print(mask)
		elif inst[:3] == 'mem':
			#print(line)
			#print('---')
			#print(mask)
			addr = int(int(inst[4:-1]))
			bval = bin(int(value))[2:]
			bval = (len(mask) - len(bval)) * '0' + bval
			#print(bval)
			mval = ''
			for i in range(0, len(mask)):
				if mask[i] == 'X':
					mval += bval[i]
				else:
					mval += mask[i]
			#print(mval)
			#print(int(mval, 2))
			memory[addr] = int(mval, 2)
	#print(memory)

	summ = 0
	for value in memory.values():
		summ += value
	print("Part 1: {}".format(summ))



	

#==============================================================================

main()

#EOF
