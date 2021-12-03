#!/usr/bin/env python
# -*- coding:utf-8 -*-
"""
Advent of code - 23A
"""

import argparse
import string
import numpy as np
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
	parser.add_argument(\
		'-s',
		'--steps',
		type=int,
		help='number of steps',
		required=True)

	# Array for all arguments passed to script
	args = parser.parse_args()

	# Return arg variables
	return args.infile, args.steps


#==============================================================================


def main():
	"""
	Main function
	"""

	# process args
	infile, steps = get_args()

	# read data
	data = []
	with open(infile, "r") as fileh:
		data = fileh.readlines()
	lines = [x.strip() for x in data]

	# init field
	ncups = 1000000
	#ncups = 9
	cups = np.zeros((ncups+1), dtype=int)
	prev = 0
	p_one = 0
	#import data
	for i in range(0, len(lines[0])):
		# add data from file
		cups[prev] = int(lines[0][i])
		if int(lines[0][i]) == 1:
			p_one = prev
		prev = int(lines[0][i])

	for i in range(len(lines[0])+1, ncups + 1):
		#print(cups, prev)
		cups[prev] = int(i)
		prev = i

	# close circle
	cups[prev] = cups[0]
	p_first = int(lines[0][0])

	#print(p_first)
	#print(p_one)
	#print(cups[1:])

	p_c = p_first
	s = 0
	while s < steps:
		#print("Step {}".format(s+1))

		#print("  input:", cups[1:])


		# get pointers
		# pc is current cup
		p_p1 = cups[p_c]	# first of part
		p_p2 = cups[p_p1]	# second of part
		p_p3 = cups[p_p2]	# third of part
		p_n = cups[p_p3]	# first after part

		p_d = p_c - 1
		if p_d == 0:
			p_d = ncups
		while p_d == p_p1 or p_d == p_p2 or p_d == p_p3:
			p_d = p_d - 1
			if p_d == 0:
				p_d = ncups

		#print("  pd val", p_d)
		#print("  pn val", p_n)
		#print("  pp val=", p_p1, p_p2, p_p3)

		# change pointers
		cups[p_c] = p_n
		cups[p_p3] = cups[p_d]
		cups[p_d] = p_p1

		# next step
		p_c = cups[p_c]

		s += 1

		if s % 250000 == 0:
			print("Step =",s)

		#print("  output:", cups[1:])



	#print(cups[1:])

#	one = first
#	while one[0] != 1:
		#print("->", pd[0], pd[1])
#		one = one[1]

#	one1 = one[1]
#	one2 = one1[1]

	# part one
	#i = 1
	#while cups[i] != 1:
	#	i = (i + 1) 
	#	if i > ncups:
	#		i = 1
	#begin = i
	#string = ''
	#while True:
	#	i = cups[i]
	#	string += str(i)
	#	if i == begin:
	#		break
	#print("Part 1:", string[1:])

	star1 = cups[1]
	star2 = cups[star1]
	print(star1, star2)
	print("Part 2:", int(star1) * int(star2))

#==============================================================================

main()

#EOF
