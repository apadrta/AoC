#!/usr/bin/env python
# -*- coding:utf-8 -*-
"""
Advent of code - 16A
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

	rules = {}
	i = 0
	for line in lines:
		if not line:
			break
		name, values = line.split(':')
		rules[name] = []
		ranges = values.split(' or ')
		for r in ranges:
			rmin, rmax = r.split('-')
			rules[name].append([int(rmin), int(rmax)])
		i += 1

	#print(rules)

	def is_ok(rules, number):
		"""
		check if number is in some rage
		"""
		for rest in rules.values():
			for r in rest:
				if number >= r[0] and number <= r[1]:
					return True
		return False

	validnums = [] 
	badn = 0
	dim = 0
	for line in [lines[i+2]] + lines[i+5:]:
		nums = [int(x) for x in line.split(',')]
		dim = len(nums)
		isvalid = True
		for num in nums:
			if not is_ok(rules, num):
				badn += num
				isvalid = False
		if isvalid:
			validnums.append(nums)

	print("Part 1: {}".format(badn))

	order = {}
	for key in rules.keys():
		order[key] = []
		for j in range(0, len(rules)):
			order[key].append(True)


	for nums in validnums:
		for i in range(0, len(nums)):
			for key, value in rules.items():
				valid = False
				for r in value:
					if nums[i] >= r[0] and nums[i] <= r[1]:
						valid = True
						break
				if not valid:
					order[key][i] = False

	# summarize order
	process = []
	for i in order:
		process.append(i)
	positions = []
	while process:
		#print(process)
		for p in process:
			if order[p].count(True) == 1:
				pos = order[p].index(True)
				positions.append([p, pos])
				process.remove(p)
				for np in process:
					order[np][pos] = False

	#print(positions)

	res = 1
	for p in positions:
		if "departure" in p[0]:
			#print(p[0], p[1])
			res = res * validnums[0][p[1]]

	print("Part 2: {}".format(res))
	

#==============================================================================

main()

#EOF
