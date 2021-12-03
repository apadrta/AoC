#!/usr/bin/env python
# -*- coding:utf-8 -*-
"""
Advent of code - 25A
"""

import argparse
import string

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

def get_loops(key, base):
	"""
	compute number of loops
	"""
	val = 1
	i = 0
	while val != key:
		i += 1
		val = (val * base) % 20201227
	return i

#==============================================================================

def get_key(base, loops):
	"""
	compute key
	"""
	key = 1
	i = 0
	while i < loops:
		i += 1
		key = (key * base) % 20201227
	return key

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

	keya = int(lines[0])
	keyb = int(lines[1])

	loopsa = get_loops(keya, 7)
	loopsb = get_loops(keyb, 7)
	#print(keya, loopsa)
	#print(keyb, loopsb)

	#print(get_key(keya, loopsb))
	#print(get_key(keyb, loopsa))
	enckey = get_key(keya, loopsb)
	
	print("Part 1:", enckey)

#==============================================================================

main()

#EOF
