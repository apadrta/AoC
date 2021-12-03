#!/usr/bin/env python
# -*- coding:utf-8 -*-
"""
Advent of code - 22A
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
	lines.append('')

	p1 = []
	p2 = []

	i = 0
	while i < len(lines):
		i += 1
		if not lines[i]:
			break
		p1.append(int(lines[i]))

	i += 1
	while i < len(lines):
		i += 1
		if not lines[i]:
			break
		p2.append(int(lines[i]))

	while p1 and p2:
		c1 = p1.pop(0)
		c2 = p2.pop(0)
		#print("combat: {} vs. {}".format(c1, c2))
		if c1 > c2:
			p1.append(c1)
			p1.append(c2)
		else:
			p2.append(c2)
			p2.append(c1)

	p = p1
	if not p:
		p = p2
	
	summ = 0
	#print(p)
	for i in range(1, len(p) +1):
		#print(i, p[-i])
		summ += i * int(p[-i])

	print("Part 1:", summ)

#==============================================================================

main()

#EOF
