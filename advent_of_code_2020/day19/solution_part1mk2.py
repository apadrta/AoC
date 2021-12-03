#!/usr/bin/env python
# -*- coding:utf-8 -*-
"""
Advent of code - 19A
"""

import argparse
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

def check_string(rules, item, finalrule):
	"""
	check string validity
	"""

	done = False
	state = []	#state array of [rule, part, position]
	s = 1
	depth = -1	# tracking depth
	checkpart = -1	# last processed part of rule (or)
	checkpos = -1   # last processed position of part (and)
	stri = 0	# input string char used
	while not done and s < 2:
		s += 1
		if len(state) == 0:
			#init with finalrule
			state.append[0, -1, -1]
			checkpart = 0
			checkpos = 0
			depth = 0
		else:
			#move to next step
			print("todo")

		# check new rule
		print(state)

	return False

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

	rules = {}
	i = 0
	for line in lines:
		if not line:
			break
		name, content = line.split(':')
		rules[name] = []
		values = content.split('|')
		for value in values:
			rules[name].append(value.strip().replace('"','').split(' '))
		i += 1

	#print(rules)


#	exit()

	items = lines[i+1:]
	#print(items)

	finalrule = '0'
	summ = 0

	for item in items:
		res = check_string(rules, item, finalrule)
		#print("{} = {}".format(item, res))
		if res:
			summ += 1
		break

	#print("Part 1: {}".format(summ))


	# print("Part 2: {}".format(res))
	

#==============================================================================

main()

#EOF
