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
	# initialize with tested string
	allchecks = [list(item)]
	#print("========")
	#print(allchecks)
	#print("========")
	done = False
	while not done:
		done = False
		if not allchecks:
			return False
		tocheck = allchecks.pop(0)
		checks = []
		for i in range(0, len(tocheck)):
			checks.append([i, tocheck])
		# try all combinations of rules on given state
		while checks:
			start, check = checks.pop(0)
			print("Checking {} [start={}]".format(check, start))
			for name, rs in rules.items():
				for r in rs:
					#print("  name=={}... {} ?= {}".format(name, r, check[start:len(r)+start]))
					if check[start:len(r)+start] == r:
						#print("    ", check)
						#print("    ", check[:start])
						#print("    ", name)
						#print("    ", check[start + len(r):])
						newcheck = check[:start] + [name] + check[start + len(r):]
						#check = newcheck
						checks.append([start + 1, copy.deepcopy(newcheck)])
						if newcheck not in allchecks:
							allchecks.append(copy.deepcopy(newcheck))
							print("  add {}".format(newcheck))
						else:
							print("  already exists {}".format(newcheck))
						if name == '0' and len(newcheck) == 1:
							done = True
							#print ("  final rule achieved")
							return True	
			#print(checks)	
		# prune inperspective variant
		todel = []
		for ac in allchecks:
			ok = False
			for rs in rules.values():
				for r in rs:
					if (ac[0] not in ('a', 'b') and ac[0] == r[0]) and (ac[-1] not in ('a', 'b') and ac[-1] == r[-1]):
						ok = True
						#break
			if not ok and ac not in todel:
				todel.append(ac)
		#print(todel)
		#print("prune", len(todel))
		print("allcheck ", len(allchecks))
		for td in todel:
			allchecks.remove(td)
		
		#print("========")
		#print(allchecks)
		#print("========")
		print("allcheck pruned", len(allchecks))
		print(allchecks)
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


	items = lines[i+1:]
	#print(items)

	finalrule = '0'
	summ = 0

	for item in items:
		res = check_string(rules, item, finalrule)
		print("{} = {}".format(item, res))
		if res:
			summ += 1

	print("Part 1: {}".format(summ))


	# print("Part 2: {}".format(res))
	

#==============================================================================

main()

#EOF
