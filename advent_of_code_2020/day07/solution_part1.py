#!/usr/bin/env python
# -*- coding:utf-8 -*-
"""
Advent of code - 7A
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
	rules = {}
	for line in lines:
		root, values = line.replace('bags', 'bag').split(' contain')
		leaves = values.replace('.', '').split(',')
		rules[root] = {}
		for leaf in leaves:
			number, name = leaf.strip().split(' ', 1)
			if leaf != ' no other bag':
				rules[root][name] = int(number)

	# part one
	mybag = 'shiny gold bag'
	bags = set()
	last_size = -1
	while last_size != len(bags):
		last_size = len(bags)
		for bag, content in rules.items():
			for key, val in content.items():
				if key == mybag or key in bags:
					bags.add(bag)

	print("Part 1: {}".format(len(bags)))

	# part two
	mybag = 'shiny gold bag'

	content_sum = 0
	bagprocess = [[mybag, 1]]

	while bagprocess:
		rule = bagprocess.pop()
		proc = rules[rule[0]]
		for key, value in proc.items():
			bagprocess.append([key, rule[1] * value])
			content_sum += rule[1] * value

	print("Part 2: {}".format(content_sum))
	

#==============================================================================

main()

#EOF
