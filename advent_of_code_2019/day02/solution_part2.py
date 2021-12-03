#!/usr/bin/env python
# -*- coding:utf-8 -*-
"""
Advent of code - 2B
"""

import argparse
from math import floor

#==============================================================================


def get_args():
	"""
	Cmd line argument parsing (preprocessing)
	"""
	# Assign description to the help doc
	parser = argparse.ArgumentParser(\
		description='Advent of code 2019')

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

def run_elfproc(nums, noun, verb):
	"""
	Run the elf processor
	"""
	nums[1] = noun
	nums[2] = verb
	ptr = 0
	while nums[ptr] != 99:
		#print(ptr, nums[ptr])
		if nums[ptr] == 1:
			# add
			#print("{} -> {}".format(nums[nums[ptr + 3]], nums[nums[ptr + 1]] + nums[nums[ptr + 2]]))
			nums[nums[ptr + 3]] = nums[nums[ptr + 1]] + nums[nums[ptr + 2]]
		elif nums[ptr] == 2:
			# multiply
			#print("{} -> {}".format(nums[nums[ptr + 3]], nums[nums[ptr + 1]] * nums[nums[ptr + 2]]))
			nums[nums[ptr + 3]] = nums[nums[ptr + 1]] * nums[nums[ptr + 2]]
		ptr += 4
	return nums[0]

def main():
	"""
	Main function
	"""

	# process args
	infile = get_args()

	# read data
	data = []
	with open(infile, "r") as fileh:
		data = fileh.read()

	for i in range(0, 99):
		for j in range(0, 99):
			nums = [int(x) for x in data.strip().split(',')]
			res = run_elfproc(nums, i, j)
			if res == 19690720:
				print("Noun: {}, Verb: {}, Result: {}".format(i, j, 100 * i + j))
				break
		if res == 19690720:
			break

#==============================================================================

main()

#EOF
