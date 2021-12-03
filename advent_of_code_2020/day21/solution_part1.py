#!/usr/bin/env python
# -*- coding:utf-8 -*-
"""
Advent of code - 21A
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

	alls = set()
	meals = []
	for line in lines:
		ingredients, alergens = line.split(' (contains ')
		meal = [[], []]
		meal[0] = set(ingredients.split(' '))
		meal[1] = set(alergens.replace(')', '').split(', '))
		meals.append(meal)
		for a in meal[1]:
			alls.add(a)
	#print(alls)
	#print(meals)


	#for each alergen in meal find other meals with the same alergen, but missing ingredients

	test = {}

	for a in alls:
		#print("allergen", a)
		for meal in meals:		
			if a in meal[1]:
				#print("process meal", meal)
				if a not in test:
					# first detection of allergen
					test[a] = copy.deepcopy(meal[0])
					#print("new item", a, test[a])
				else:
					# remove missing igredietns
					rm = []
					for am in test[a]:
						if am not in meal[0]:
							#print("removing {} from {}".format(am, a))
							rm.append(am)
					for r in rm:
						test[a].remove(r)


	susp = set()
	for key, value in test.items():
		susp = susp | value
	#print(susp)

	alli = set()
	for meal in meals:
		alli = alli | meal[0]

	#print(alli)

	safe = alli - susp

	#print(safe)

	count = 0

	for meal in meals:
		count += len(meal[0] & safe)

	print("Part 1:", count)


	#print(test)

	ids = {}
	while True:
		#find first one-item record
		for key, value in test.items():
			if len(value) == 1:
				break
		# remove identified item
		newval = value.pop()
		#print(key, newval)
		ids[key] = newval
		#print("ids:", ids)
		del test[key]
		#print("mytest", newval in test['fish'])
		# shorten other sets
		for k, v in test.items():
			if newval in v:
				test[k].remove(newval)
		#print("ids", ids)
		#print("test", test)
		if len(test) == 0:
			break
	#print(ids)

	toord = list(ids.keys())
	toord.sort()

	canon = ''
	for to in toord:
		canon += "{},".format(ids[to])
	print("Part 2: {}".format(canon[:-1]))
	

#==============================================================================

main()

#EOF
