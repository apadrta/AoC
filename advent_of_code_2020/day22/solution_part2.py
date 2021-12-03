#!/usr/bin/env python
# -*- coding:utf-8 -*-
"""
Advent of code - 22A
"""

import argparse
import string
import copy

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

def get_winner(p1, p2, depth):
	"""
	play one game
	"""

	if depth == 40:
		print("===")
		exit(1)
	#print("D =", depth)
	#print(p1)
	#print(p2)
	last1 = []
	last2 = []
	while p1 and p2:
		c1 = p1.pop(0)
		c2 = p2.pop(0)
		if len(p1) >= c1 and len(p2) >= c2:
			#print("recursion")
			res, d1, d2 = get_winner(copy.deepcopy(p1[:c1]), copy.deepcopy(p2[:c2]), depth + 1)
			#print("return")
			if res == 1:
				# player 1 wins subgame
				p1.append(c1)
				p1.append(c2)
			else:				
				p2.append(c2)
				p2.append(c1)
		else:
			#print("classic")
			#classic combat
			if c1 > c2:
				p1.append(c1)
				p1.append(c2)
			else:
				p2.append(c2)
				p2.append(c1)
		#print(" p1", p1)
		#print(" p2", p2)
		if p1 in last1 or p2 in last2:
			#print("repeat -> player 1 wins")
			return 1, p1, p2
		last1.append(copy.deepcopy(p1))
		last2.append(copy.deepcopy(p2))
	if p1:
		return 1, p1, p2
	else:
		return 2, p1, p2

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


	res, p1, p2 = get_winner(p1, p2, 0)
	#print(res)

	p = p1
	if not p:
		p = p2
	
	summ = 0
	#print(p)
	for i in range(1, len(p) +1):
		#print(i, p[-i])
		summ += i * int(p[-i])
	
	print("Part 2:", summ)

#==============================================================================

main()

#EOF
